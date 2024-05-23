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


scheduler = BackgroundScheduler()
scheduler.add_job(func=updateChatGPT, trigger="interval", hours=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

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
    
    if question == "안녕" or question == "hi":
        time.sleep(3)
        answer = "안녕하세요!"
    elif question == "학사일정":
        answer = """
        인하대학교 2024학년도 1학기 5~6월 학사일정에 대해 알려드릴게요 🦆 <br><br>
        05.24(금) (수업일수 3/4선)<br>
        05.27(월) ~ 05.28(화) 2024학년도 하계 계절학기 수강신청<br>
        05.27(월) ~ 05.28(화) 2024-1학기 우수인재인증 신청<br>
        06.10(월) ~ 06.14(금) 2024-1학기 기말고사<br>
        06.17(월) ~ 06.21(금) 2024-1학기 보강주간<br>
        06.24(월) ~ 07.17(수) 2024학년도 하계 계절학기 수업<br>
        """
    elif question == "캠퍼스맵":
        answer = """
        인하대학교 캠퍼스맵 사진을 보여드릴게요 🦆<br>
        더 자세한 정보가 필요하시다면 아래 링크에서 확인하실 수 있어요<br><br>
        <a href="https://www.inha.ac.kr/kr/1121/subview.do" target="_blank">인하대학교 캠퍼스맵</a><br>
        <img src="static/images/inha_made_bg.jpg" class="inha" style="width: 100%; overflow-x: auto;"> 
        """
    elif question == "수강신청":
        answer = """
        인하대학교 수강신청 홈페이지를 알려드릴게요 🦆<br>
        올클 성공하세요 :D<br><br>
        <a href="https://sugang.inha.ac.kr/sugang/" target="_blank">인하대학교 수강신청 사이트</a><br>
        """
    elif question == "교내연락처":
        answer = """
        교내 연락처를 검색할 수 있는 사이트를 알려드릴게요 🦆<br>
        부정확한 정보가 있을 수 있으므로 주의해주세요<br><br>
        <a href="https://www.inha.ac.kr/kr/966/subview.do" target="_blank">인하대학교 교내연락처</a><br>
        """
    elif question == "I-Class":
        answer = """
        인하대학교 I-Class 사이트를 알려드릴게요 🦆<br>
        빡공하세요 :D<br><br>
        <a href="https://learn.inha.ac.kr/login.php" target="_blank">인하대학교 I-Class</a><br>
        """
    elif question == "생활관":
        answer = """
        인하대학교 생활관 사이트를 알려드릴게요 🦆<br><br>
        <a href="https://dorm.inha.ac.kr/dorm/index.do" target="_blank">인하대학교 생활관</a><br>
        """
    elif question == "인하 포털":
        answer = """
        인하대학교 포털사이트를 알려드릴게요 🦆<br><br>
        <a href="https://portal.inha.ac.kr/login.jsp?idpchked=false">인하대학교 포털사이트</a><br>
        """
    elif question == "정석학술정보관":
        answer = """
        인하대학교 정석학술정보관 온라인 사이트를 알려드릴게요 🦆<br><br>
        <a href="https://lib.inha.ac.kr/" target="_blank">인하대학교 정석학술정보관</a><br>
        """
    elif question == "증명서 발급 시스템":
        answer = """
        인하대학교 증명발급시스템 사이트를 알려드릴게요 🦆<br><br>
        <a href="https://cert.inha.ac.kr/icerti/index_internet.jsp?t=8222">인하대학교 증명발급시스템</a><br>
        """
    elif question == "국제처":
        answer = """
        인하대학교 국제처 사이트를 알려드릴게요 🦆<br><br>
        <a href="https://internationalcenter.inha.ac.kr/internationalcenter/index.do">인하대학교 국제처</a><br>
        """
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