from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from transformers import B
import numpy as np
import matplotlib.pyplot as plt
import json
import os

os.chdir('./InhaChatBot/Server/test')

with open("./everytime2024y.json", "r", encoding="utf-8") as file:
    file_content = json.load(file)

sentence = []
for i in range(len(file_content['everytime'])):
    sentence.append(file_content['everytime'][i]['Question'])
    
sentence = np.array(sentence)

# vectorizer = TfidfVectorizer()
# x = vectorizer.fit_transform(sentence)

# print(x)
# # Step 2: K-means 클러스터링
# num_clusters = 3
# kmeans = KMeans(n_clusters=num_clusters, random_state=42)
# kmeans.fit(x)
# labels = kmeans.labels_

# # 결과 출력
# for i, sentenc in enumerate(sentence):
#     print(f"Sentence: {sentenc} - Cluster: {labels[i]}")
    
# # Step 3: 차원 축소 (PCA 사용)
# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(x.toarray())

# # Step 4: 시각화
# plt.figure(figsize=(12, 8))
# for i in range(num_clusters):
#     cluster_points = X_pca[labels == i]
#     plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {i}')

# plt.title('K-means Clustering of Sentences (PCA)')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')
# plt.legend()
# plt.show()