from flask import Flask, jsonify, request, render_template, url_for, redirect, session
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import pymysql
from flask_session import Session
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from everytime_data_crawling import everytime_data_crawling

conn, cur = None, None

def connect():
    return pymysql.connect(host='127.0.0.1', user='root', password='0000', db='user_threadDB.sql', charset='utf8')

def updateChatGPT():
    try:
        os.chdir(r'./database')
    except:
        pass
    everytime_data_crawling(1, 1, 3)
    print("update files")

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=API_KEY)

ASSISTANT_ID = os.environ['OPENAI_ASSISTANT_KEY']

app = Flask(__name__)
app.config['SECRET_KEY'] = '0000'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=updateChatGPT, trigger="interval", hours=1)
# scheduler.start()

# atexit.register(lambda: scheduler.shutdown())

# 입장 시
@app.route('/')
def enter():
    session['check_login'] = False
    return redirect(url_for('login'))

# 메인 화면
@app.route('/main')
def main():
    if session['check_login'] == False:
        return redirect(url_for('login'))
    return render_template('index.html')

# 로그인 화면
@app.route('/login')
def login():
    session['check_login'] = False
    return render_template('login.html')

# 로그인 정보 확인
@app.route('/check_login', methods=['POST'])
def login_check():
    data = request.json
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"select thread_ID from chatbotuser where email='{data[0]['email']}' and password='{data[1]['password']}'")
    conn.commit()
    try:
        row = list(cur.fetchall())[0][0]
    except IndexError:
        return jsonify({'error': 'error' })
    session['thread_id'] = row
    session['check_login'] = True
    conn.close()
    return jsonify({'redirect': url_for('main')})

# 회원가입 화면
@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

# 회원가입
@app.route('/sign', methods=['POST'])
def sign():
    data = request.json
    name = data[0]['name']
    email = data[1]['email']
    password = data[2]['password']
    conn = connect()
    cur = conn.cursor()
    cur.execute(f'select * from chatbotuser where userName="{name}"')
    conn.commit()
    temp = list(cur.fetchall())
    for user in temp:
        if user[1] == email and user[2] == password:
            return jsonify({'error': 'another_email_or_password'})
    thread = client.beta.threads.create()
    print(thread)
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"insert into chatbotuser values('{name}', '{email}', '{password}', '{thread.id}')")
    conn.commit()
    conn.close()
    return jsonify({'redirect': url_for('login')})

# 챗봇과 대화
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    
    if question == "안녕":
        time.sleep(3)
        answer = "안녕하세요!"
    elif question == "오늘 날씨는 어때?":
        answer = "오늘은 맑은 날씨예요."
    else:
        THREAD_ID = session.get('thread_id')
        
        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            
            role="user",
            content=question
        )
        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=THREAD_ID,
                run_id=run.id
            )
            time.sleep(0.5)
        messages = client.beta.threads.messages.list(
            thread_id=THREAD_ID,
            order="asc"
        )
        answer = messages.data[-1].content[0].text.value

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)