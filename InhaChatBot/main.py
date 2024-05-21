from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

vector_store = client.beta.vector_stores.create(name="")

# asst_IFFNqYkitBBHVAyS1h2VnhNK
# assistant = client.beta.assistants.create(
#    name="인하대 챗봇",
#    instructions="당신은 인하대학교의 정보를 알려주는 챗봇입니다. 필요한 정보를 자세하게 답변해주세요.",
#    model="gpt-4-turbo-preview",
# )
# print(assistant)

# thread_iJJMRWJw8uYsUqY8bN4yVhqL
# thread = client.beta.threads.create()
# print(thread)

# msg_btEf2gQjaTHgr7wto3mNA7Ym
# message = client.beta.threads.messages.create(
#     thread_id="thread_iJJMRWJw8uYsUqY8bN4yVhqL",
#     role="user",
#     content="인하대학교를 가는 방법을 알려줘."
# )
# print(message)

# run_Z7Z7EP60BmWANQ5OkDnceh5F
# run = client.beta.threads.runs.create(
#     thread_id="thread_iJJMRWJw8uYsUqY8bN4yVhqL",
#     assistant_id="asst_IFFNqYkitBBHVAyS1h2VnhNK"
# )
# print(run)

# run = client.beta.threads.runs.retrieve(
#     thread_id="thread_iJJMRWJw8uYsUqY8bN4yVhqL",
#     run_id="run_Z7Z7EP60BmWANQ5OkDnceh5F"
# )
# print(run)

# messages = client.beta.threads.messages.list(
#     thread_id="thread_iJJMRWJw8uYsUqY8bN4yVhqL"
# )
# print(messages)