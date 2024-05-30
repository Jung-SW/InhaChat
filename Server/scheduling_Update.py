from openai import OpenAI
import os
from dotenv import load_dotenv
from all_of_data_crawling import everytime_data_crawling
from all_of_data_crawling import Inha_crawling
from all_of_data_crawling import re_menu_crawling
from all_of_data_crawling import recent_update

# 크롤링 - 저장 - 모든 업데이트
def update():
    # === 순서대로 실행 ===
    everytime_data_crawling(1,1,3)
    Inha_crawling()
    recent_update()
    re_menu_crawling()

    # === 파일 업데이트
    load_dotenv()
    key=os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=key)

    # Assuming you have the assistant_id for the existing assistant
    assistant_id = os.environ['OPENAI_ASSISTANT_KEY']

    #이름은 상관 없음. -- Inha_ChatBot
    vector_store = client.beta.vector_stores.create(name="Inha_ChatBot")

    # 파일저장경로 확인
    file_paths = ["./database/인하대학교 공지사항.json","./database/인하대학교_최근공지사항.json","./database/everytime2024y.json","./database/인하대학교 정보.json","./database/인하대학교 학생식당.json"]
    file_streams = [open(path, "rb") for path in file_paths]

    
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    # You can print the status and the file counts of the batch to see the result of this operation.
    print(file_batch.status)
    print(file_batch.file_counts)

    # 파일 업데이트
    client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

if __name__=="__main__":
    update()