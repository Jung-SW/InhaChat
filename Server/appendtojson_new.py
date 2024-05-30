import json
import os

def write_json(filename, content_name, page):
    with open(filename, "r+", encoding="utf-8") as file:
        file_content = json.load(file)
        file_content[content_name].append(page)
        file.seek(0)
        json.dump(file_content, file, ensure_ascii=False, indent=4)

def write_json_everytime(page, filename="./database/everytime2024y.json",):
    write_json(filename, "everytime", page)

# 가급적 파일 이름이랑 딕셔너리 명 바꾸지 말 것
def write_json_inha_notice(page, filename="./database/인하대학교 공지사항.json",):
    write_json(filename, "인하대학교 공지사항", page)

def write_json_recent_notice(recent_notice, filename="./database/인하대학교_최근공지사항.json",):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(recent_notice, file, ensure_ascii=False, indent=4)

def write_json_re_menu(page, filename="./database/인하대학교 학생식당.json",):
    write_json(filename, "이번주 학생식당 메뉴", page)
