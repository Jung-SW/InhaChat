from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from appendtojson_new import write_json_everytime
from appendtojson_new import write_json_inha_notice
from appendtojson_new import write_json_re_menu
from appendtojson_new import write_json_recent_notice
from dotenv import load_dotenv
import os
from tqdm import tqdm
import json
#현재시간 계산용
from datetime import datetime

# 에타 크롤링
def everytime_data_crawling(start, repeat, comments):
    load_dotenv()
    ID=os.environ['ID']
    PW=os.environ['PW']
    options = webdriver.EdgeOptions()
    options.add_argument('log-level=3')
    
    # 사용하는 브라우저의 드라이버
    driver = webdriver.Edge(options=options)

    # 웹사이트
    driver.get(f'https://everytime.kr/374912/p/{start}')
    
    # 5초 동안 값을 입력할 수 있을 때까지 대기
    driver.implicitly_wait(5)

    # 아이디, 비번 입력 후 로그인
    driver.find_element(By.XPATH, "/html/body/div[1]/div/form/div[1]/input[1]").send_keys(ID)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/form/div[1]/input[2]").send_keys(PW)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input").click()

    titles = []
    for _ in range(repeat):
        for i in tqdm(range(1, 21)):
            try:
                # 댓글이 있는 글 중에서 ?가 제목과 본문에 포함된 글
                if driver.find_element(By.XPATH, f'//*[@id="container"]/div[4]/article[{i}]/a/div/div/ul'):
                    temp = driver.find_element(By.XPATH, f'//*[@id="container"]/div[4]/article[{i}]/a/div/h2').text
                    temp2 = driver.find_element(By.XPATH, f'//*[@id="container"]/div[4]/article[{i}]/a/div/p').text
                    if '?' in temp and '?' in temp2:
                        titles.append(temp)
                        driver.find_element(By.XPATH, f'//*[@id="container"]/div[4]/article[{i}]/a').click()
                        url = driver.current_url
                        everytime = {}
                        everytime["Question"] = driver.find_element(By.XPATH, f'//*[@id="container"]/div[4]/article/a/h2').text
                        answer = {}
                        # 상위 n개의 댓글만 추출
                        for k in range(comments):
                            try:
                                answer[f"answer{k}"] = driver.find_element(By.XPATH, f'//*[@id="container"]/div[4]/article/div/article[{k + 1}]/p').text
                            except:
                                break
                        everytime["Answer"] = answer
                        everytime["url"] = url
                        write_json_everytime(everytime)
                        driver.back()
            except NoSuchElementException:
                pass
        url = driver.current_url[30:]
        # 다음 페이지로 넘어가기
        if url == '1':
            driver.find_element(By.XPATH, '//*[@id="container"]/div[5]/div[2]/a').click()
        elif url == '2':
            driver.find_element(By.XPATH, '//*[@id="container"]/div[5]/div[2]/a[2]').click()
        else:
            driver.find_element(By.XPATH, '//*[@id="container"]/div[5]/div[2]/a[3]').click()
    
    # 셀레니움 종료
    driver.quit()
    print("Finish update everytime")

# 공지사항 크롤링
def Inha_crawling():
    url_for_inha_crawling=f'https://www.inha.ac.kr/kr/950/subview.do?&enc=Zm5jdDF8QEB8JTJGYmJzJTJGa3IlMkY4JTJGYXJ0Y2xMaXN0LmRvJTNGcGFnZSUzRDElMjZzcmNoQ29sdW1uJTNEJTI2c3JjaFdyZCUzRCUyNmJic0NsU2VxJTNEJTI2YmJzT3BlbldyZFNlcSUzRCUyNnJnc0JnbmRlU3RyJTNEJTI2cmdzRW5kZGVTdHIlM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjY='
    old_head=""
    old_date=""

    인하 = {}
    driver = webdriver.Edge()
    driver.get(url_for_inha_crawling)
    # 파일을 열어서 거를 데이터 찾기
    with open("./database/인하대학교 공지사항.json", "r", encoding="utf-8") as f:
        content = json.load(f)
        old_head = content["인하대학교 공지사항"][-1]["Question"]
        old_date = content["인하대학교 공지사항"][-1]["작성일"]

    # === 신규 공지사항 확인 ===
    for i in range(20,8,-1):
        
        try:
            driver.find_element('xpath', f'//*[@id="menu950_obj2831"]/div[2]/form[2]/table/tbody/tr[{i}]/td[2]/a').click()
        except:
            continue
        head = driver.find_element(By.XPATH, f'//*[@id="_contentBuilder"]/div[1]/div[2]/div[2]/h2').text
        
        date = driver.find_element(By.XPATH, f'//*[@id="_contentBuilder"]/div[1]/div[2]/div[1]/div[1]/dl[2]/dd').text
        contents = driver.find_element(By.XPATH, f'//*[@id="_contentBuilder"]/div[1]/div[2]/div[3]').text
        인하["Question"] = head
        인하["Answer"] = contents
        인하["작성일"] = date
        
        if old_head != head and old_date <= date:
            write_json_inha_notice(인하)
        driver.back()
    driver.quit()
    print("Finish update InhaUniv.Notice")

# 학식 크롤링
def re_menu_crawling():
    today = datetime.today()
    today = today.strftime("%Y-%m-%d")

    boundary = {
        "이번주 학생식당 메뉴": [
            {
            "Question" :"오늘 날짜",
            "Answer": today
            }
        ]
    }
    with open("./database/인하대학교 학생식당.json", "w", encoding="utf-8") as file:
        json.dump(boundary, file, ensure_ascii=False, indent=4)

    url_for_re_menu = f'https://www.inha.ac.kr/kr/1072/subview.do?&enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtyJTJGMiUyRnZpZXcuZG8lM0Ztb25kYXklM0QyMDI0LjA2LjAzJTI2d2VlayUzRHByZSUyNg=='

    driver = webdriver.Edge()
    driver.get(url_for_re_menu)


    학생식당_메뉴 = {}
    # 이번주 학식 수집
    for i in range(1, 16, 1):
        Monday_breakfast = driver.find_element(By.XPATH, f'//*[@id="_contentBuilder"]/div[1]/div[2]/form[1]/h2[{i}]').text
        #Monday_breakfast_content = driver.find_element(By.XPATH, f'//*[@id="_contentBuilder"]/div[1]/div[2]/form[1]/div[{i}]/div[1]/div[1]').text
        Monday_breakfast_content = driver.find_element(By.XPATH, f'//*[@id="_contentBuilder"]/div[1]/div[2]/form[1]/div[{i}]/div[1]/div[1]/table').text
        if i % 3 == 1:
            학생식당_메뉴["Qustion"] = Monday_breakfast + " 아침 학식"
            학생식당_메뉴["Answer"] = Monday_breakfast_content + " 아침 학식"
        elif i % 3 == 2:
            학생식당_메뉴["Qustion"] = Monday_breakfast + " 점심 학식"
            학생식당_메뉴["Answer"] = Monday_breakfast_content + " 점심 학식"
        else:
            학생식당_메뉴["Qustion"] = Monday_breakfast + " 저녁 학식"
            학생식당_메뉴["Answer"] = Monday_breakfast_content + " 저녁 학식"
        write_json_re_menu(학생식당_메뉴)

    driver.quit()
    print("Finish update menu")

# 최근 공지사항
def recent_update():
    recent_notice_head = []
    recent_notice_date = ""
    recent_notice = {}
    # 공지사항 파일 열어서 작성일 기준 최근 공지사항 가져오기
    with open("./database/인하대학교 공지사항.json", "r", encoding="utf-8") as f:
        content = json.load(f)
        recent_notice_head = []
        recent_notice_date = content["인하대학교 공지사항"][-1]["작성일"]
        for line in reversed(content["인하대학교 공지사항"]):
            if line["작성일"] == recent_notice_date:
                recent_notice_head.append(line["Question"])
            else:
                break
        recent_notice["Question"] = "인하대학교 최근 공지사항"
        recent_notice["작성일"] = recent_notice_date
        recent_notice["Answer"] = recent_notice_head
    write_json_recent_notice(recent_notice)
    print("Finish update recent_notice")