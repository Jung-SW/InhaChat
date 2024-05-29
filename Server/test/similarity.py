from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import difflib
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import json
import os

os.chdir('./InhaChatBot/Server/test')

with open("./everytime2024y.json", "r", encoding="utf-8") as file:
    file_content = json.load(file)

sentence = []
for i in range(len(file_content['everytime'])):
    sentence.append(file_content['everytime'][i]['Question'])

question = "학점 얼마나 들어야 할까?"
sentence.append(question)

# 코사인 유사도
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(sentence)
cosine_similarities = cosine_similarity(x, x)

num = [0]
answer = []
for i in range(len(sentence) - 1):
    similar = cosine_similarities[-1][i]
    if similar > num[-1]:
        if num[0] == 0: num.pop()
        if len(num) > 4:
            del num[0]
            del answer[0]
        num.append(similar)
        answer.append(sentence[i])

print(answer)
# print(num)

# Sequence Matcher를 이용해서 유사도 측정하기
# input_string = "정석도서관 어디임"
input_bytes = bytes(question, 'utf-8')
input_bytes_list = list(input_bytes)
num = [0]
num2 = []
answer = []
for i in range(len(sentence) - 1):
    answer_string = sentence[i]
    answer_bytes = bytes(answer_string, 'utf-8')
    answer_bytes_list = list(answer_bytes)
    sm = difflib.SequenceMatcher(None, answer_bytes_list, input_bytes_list)
    similar = sm.ratio()
    if similar > num[-1]:
        if num[0] == 0: num.pop()
        num2.append(similar)
        if len(num) > 4:
            del num[0]
            del answer[0]
        num.append(similar)
        answer.append(sentence[i])

# print(num)
# print(num2)
print(answer)

# 별로임
# 유클리디안 거리
euclidean_dists = euclidean_distances(x, x)

num = [0]
answer = []
for i in range(len(sentence) - 1):
    similar = euclidean_dists[-1][i]
    if similar > num[-1]:
        if num[0] == 0: num.pop()
        if len(num) > 4:
            del num[0]
            del answer[0]
        num.append(similar)
        answer.append(sentence[i])

print(answer)
# print(num)