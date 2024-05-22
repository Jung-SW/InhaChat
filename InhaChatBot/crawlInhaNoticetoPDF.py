import pdfkit
import os
from PyPDF2 import PdfMerger
import requests
from bs4 import BeautifulSoup

# def search_inha_notification():
    
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

os.chdir(r'C:\Users\jungs\OneDrive\JungSW\011_University\021_2학년_1학기\파이썬기반응용프로그래밍\InhaChatBot\crawled_files')

options = {'quiet': ''}
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# merger = PdfMerger()

merge_list = []

# EdgeDriver 인스턴스 생성
driver = webdriver.Edge()

# 웹페이지 로딩
# driver.get('https://www.inha.ac.kr/kr/950/subview.do')

# 웹 요소 조작
# for i in range(8, 20):
#     driver.find_element('xpath', f'//*[@id="menu950_obj2831"]/div[2]/form[2]/table/tbody/tr[{i}]/td[2]/a').click()
#     time.sleep(0.5)
#     print(driver.title)
#     driver.back()
# 33140
for i in range(37010, 37020):
    url = f'https://www.inha.ac.kr/bbs/kr/8/{i}/artclView.do'
    driver.get(url)
    title = driver.title[15:]
    title = title.replace("/", ",")
    title = title.replace("*", "-")
    title = title.replace("?", ".")
    title = title.replace("!", ".")
    title = title.replace("\\", ",")
    title = title.replace("|", ";")
    title = title.replace(":", ";")
    title = title.replace("<", "[")
    title = title.replace(">", "]")
    time.sleep(3)
    if title:
        html_comments = driver.find_elements(By.CLASS_NAME, "artclView")
        with open('crawled_files/'+title+'.txt', 'w', encoding='UTF8') as d:
            for comment in html_comments:
                text = d.write(comment.text)
        title = title + '.pdf'
        try:
            pdfkit.from_url(url, title, options=options, configuration=config)
            merge_list.append(f"crawled_files/{title}")
        except:
            pass
# # 결과 확인
# print(driver.title)
print(merge_list)
# 브라우저 종료
driver.quit()