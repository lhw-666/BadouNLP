#!/usr/bin/env python3  
#coding: utf-8

#基于训练好的词向量模型进行聚类
#聚类采用Kmeans算法
import math
import re
import json
import jieba
import numpy as np
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from collections import defaultdict

#输入模型文件路径
#加载训练好的模型
def load_word2vec_model(path):
    model = Word2Vec.load(path)
    return model

def load_sentence(path):
    sentences = set()
    with open(path, encoding="utf8") as f:
        for line in f:
            sentence = line.strip()
            sentences.add(" ".join(jieba.cut(sentence)))
    print("获取句子数量：", len(sentences))
    return sentences

#将文本向量化
def sentences_to_vectors(sentences, model):
    vectors = []
    for sentence in sentences:
        words = sentence.split()  #sentence是分好词的，空格分开
        vector = np.zeros(model.vector_size)
        #所有词的向量相加求平均，作为句子向量
        for word in words:
            try:
                vector += model.wv[word]
            except KeyError:
                #部分词在训练中未出现，用全0向量代替
                vector += np.zeros(model.vector_size)
        vectors.append(vector / len(words))
    return np.array(vectors)


def main():
    model = load_word2vec_model(r"D:\tby\python\AIcode\week5\参考\model.w2v") #加载词向量模型
    sentences = load_sentence(r"D:\tby\python\AIcode\week5\参考\titles.txt")  #加载所有标题
    vectors = sentences_to_vectors(sentences, model)   #将所有标题向量化

    n_clusters = int(math.sqrt(len(sentences)))  #指定聚类数量
    print("指定聚类数量：", n_clusters)
    kmeans = KMeans(n_clusters)  #定义一个kmeans计算类
    kmeans.fit(vectors)          #进行聚类计算

    sentence_label_dict = defaultdict(list)
    euclidean_distance_sum = np.zeros(n_clusters)
    sentences_list = list(sentences)
    for i in range(len(sentences_list)):
        label = kmeans.labels_[i]
        sentence = sentences_list[i]
        sentence_label_dict[label].append(sentence)         #同标签的放到一起
        centers_vector = kmeans.cluster_centers_[label]
        sentence_vector = vectors[i]
        # 求对应标签距离和
        euclidean_distance_sum[label] += np.linalg.norm(centers_vector - sentence_vector)

    # 计算距离平均值
    euclidean_distance_agv = np.zeros(n_clusters)
    for label in kmeans.labels_:
        euclidean_distance_agv[label] = euclidean_distance_sum[label] / len(sentence_label_dict[label])
    
    # 排序
    sorted_id = sorted(range(len(euclidean_distance_agv)), key=lambda k: euclidean_distance_agv[k], reverse=False)
    # 找距离最小的前十个标签，打印出该标签下的全部句子
    for i in range(min(10,len(sorted_id))):
        label = sorted_id[i]
        print("cluster %s: "% label, "distance: %.2f: " %euclidean_distance_agv[label])
        for j in range(len(sentence_label_dict[label])):
            print(sentence_label_dict[label][j].replace(" ", ""))
        print("---------")

if __name__ == "__main__":
    main()

