import json

def deduplication(file_name):
    with open(file_name, 'r+', encoding='utf-8') as file:
        file_contents = json.load(file)
        file_contents_list = file_contents["everytime"]
        
        x = list({file_content['Question']: file_content for file_content in file_contents_list}.values())
        file_contents["everytime"] = x
        file.seek(0)
        json.dump(file_contents, file, ensure_ascii=False, indent=4)

deduplication('./InhaChatBot/everytime/everytime2022.json')

# 실행 한 후에 해당 파일을 보면 중간에 json파일이 끊어져 있는 부분이 있음
# 그 뒤 부분을 다 지우면 됨