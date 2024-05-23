import pymysql

conn, cur = None, None

conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='user_threadDB.sql', charset='utf8')
cur = conn.cursor()

userName = input("userName: ")
email = input("email: ")
password = input("password: ")
thread_ID = input("thread_ID: ")
sql = f"insert into chatbotuser values('{userName}', '{email}', '{password}', '{thread_ID}')"
cur.execute(sql)

conn.commit()
conn.close()