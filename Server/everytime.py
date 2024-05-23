from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
import time
from appendtojson import write_json
from dotenv import load_dotenv
import os

os.chdir(r'./InhaChatBot/everytime')
# 사용하는 브라우저의 드라이버
driver = webdriver.Edge()

# 에브리타임 아이디랑 비밀번호
load_dotenv()
ID = os.environ['ID']
PW = os.environ['PW']

# 웹사이트
# driver.get('https://everytime.kr')
page = 1
driver.get(f'https://everytime.kr/374912/p/{page}')

# 모바일 웹 이용하기 버튼이 있으면 사용
# driver.find_element(By.XPATH, "/html/body/div/main/header/button").click()

# 로그인하기
# driver.find_element(By.CLASS_NAME, "signin").click()

# 5초 동안 값을 입력할 수 있을 때까지 대기
driver.implicitly_wait(5)

# 아이디, 비번 입력 후 로그인
driver.find_element(By.XPATH, "/html/body/div[1]/div/form/div[1]/input[1]").send_keys(ID)
driver.find_element(By.XPATH, "/html/body/div[1]/div/form/div[1]/input[2]").send_keys(PW)
driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input").click()

titles = []
for repeat in range(10):
    for i in range(1, 21):
        try:
            # 댓글이 있는 글 중에서 ?가 포함된 글
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
                    for k in range(3):
                        try:
                            answer[f"answer{k}"] = driver.find_element(By.XPATH, f'//*[@id="container"]/div[4]/article/div/article[{k + 1}]/p').text
                        except:
                            break
                    everytime["Answer"] = answer
                    everytime["url"] = url
                    print(os.getcwd())
                    write_json(everytime)
                    driver.back()
        except NoSuchElementException:
            pass
    url = driver.current_url[30:]
    # 다음 페이지로 넘어가기
    if url == '1':
        driver.find_element(By.XPATH, '//*[@id="container"]/div[4]/div[2]/a').click()
    elif url == '2':
        driver.find_element(By.XPATH, '//*[@id="container"]/div[4]/div[2]/a[2]').click()
    else:
        driver.find_element(By.XPATH, '//*[@id="container"]/div[4]/div[2]/a[3]').click()
# 조건에 맞는 데이터 출력
for title in titles:
    print(title)

# 셀레니움 종료
driver.quit()