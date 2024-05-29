import json
import os
from konlpy.tag import Kkma
from konlpy.tag import Okt
import re
import pandas as pd
from hanspell import spell_checker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 텍스트 전처리 함수
def preprocess_text(text):
    text = text.strip()
    text = ''.join([word for word in text.split() if word not in stopword])
    return text

def recommend_questions(new_question, tfidf_matrix, data, vectorizer, top_n=5):
    # 새로운 질문 전처리
    new_question_cleaned = preprocess_text(new_question)
    # 새로운 질문 벡터화
    new_question_vec = vectorizer.transform([new_question_cleaned])
    # 유사도 계산
    cosine_sim = cosine_similarity(new_question_vec, tfidf_matrix).flatten()
    # 유사도에 따른 상위 인덱스 추출
    similar_indices = cosine_sim.argsort()[-top_n:][::-1]
    recommended_questions = data.iloc[similar_indices]['question'].tolist()
    return recommended_questions

# def text_clean(text):
#     pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
#     text = re.sub(pattern, '', text)
#     pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
#     text = re.sub(pattern, '', text)
#     pattern = '[a-zA-Z0-9]'    # 숫자와 알파벳 제거
#     text = re.sub(pattern, '', text)
#     pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
#     text = re.sub(pattern, '', text)
#     pattern = '<[^>]*>'         # HTML 태그 제거
#     text = re.sub(pattern, '', text)
#     pattern = '[^\w\s]'         # 특수기호제거
#     text = re.sub(pattern, '', text)
#     return text

with open("./everytime2024y.json", "r", encoding="utf-8") as file:
    file_content = json.load(file)

with open("./stopword.txt", "r", encoding="utf-8") as file:
    stopword = file.readlines()
for i in range(len(stopword)):
    stopword[i] = stopword[i].replace('\n', '')

answer = []
answer2 = ""
for i in range(len(file_content['everytime'])):
    answer.append(file_content['everytime'][i]['Question'])
    answer2 += file_content['everytime'][i]['Question']

data = pd.DataFrame(answer, columns=['question'])
data['cleaned_question'] = data['question'].apply(preprocess_text)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data['cleaned_question'])

new_question = "정석도서관"
recommend_question = recommend_questions(new_question, tfidf_matrix, data, vectorizer)
print(recommend_question)

# compile = re.compile("[^ ㄱ-ㅣ가-힣]+")
# for i in range(len(answer)):
#     a = compile.sub("",answer[i])
#     answer[i]=a

# okt = Okt()
# result=[]
# result = [okt.nouns(i) for i in answer]
# final_result = [r for i in result for r in i]
# # print(final_result)

# stop_word = ["건가", "는거", "함", "사람", "임", "거", "왜", "혹시"]
# final_result = [i for i in final_result if i not in (stop_word or stopword)]

# korean = pd.Series(final_result).value_counts().head(10)
# print(korean)

# kkma=Kkma()

# k = kkma.nouns(answer2)
# kk = pd.Series(k).value_counts().head(10)
# print(kk)