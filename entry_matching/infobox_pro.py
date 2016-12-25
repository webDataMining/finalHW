# -*- coding: utf-8 -*-
#author: Pengfei WANG
#time: 2016.12.23

#from english_translation import *
from test import *
from loadWordVector import *
import requests  
import json
import numpy as np

def infobox_process(infobox,findit,obj_en,obj,recommend,p1,info_key_vec,title):
    info_key_ch = {}

    #第一轮匹配:中英文直接匹配
    for (k,v) in infobox.items():
        info_key = str(k.replace('_',' '))
        info_key_ch[k] = str(translate(info_key))
        #print(info_key)
        if (info_key in obj_en) or (obj_en in info_key) or (obj in info_key_ch[k]) or (info_key_ch[k] in obj):
            findit = True
            recommend[p1] = [title,k,v]
            print(v)
            break

    #判断：是否已经匹配到结果,如果匹配到了，就直接结束，不再继续
    if findit == True:
        return

    #第二轮匹配：词义向量余弦相似度
    if obj in word_vectors.keys():
        obj_vec = word_vectors[obj]                 # 目标词义向量
    else:
        obj_vec = [0]*len(word_vectors['名字'])
    obj_array = np.array(obj_vec)               # 转化成可计算的矩阵形式
    obj_len = np.sqrt(obj_array.dot(obj_array)) # 目标词义向量的模长
    vec_cos = {}

    for (k,v) in infobox.items():
        if info_key_ch[k] in word_vectors.keys():
            if k in info_key_vec.keys():
                info_key_vec[k] = info_key_vec[k]
            else:
                info_key_vec[k] = word_vectors[info_key_ch[k]]
            # 计算两个词义向量的余弦相似度
            info_key_array = np.array(info_key_vec[k]) 
            info_key_len = np.sqrt(info_key_array.dot(info_key_array)) # infobox的key的词义向量的模长
            cos_angel = obj_array.dot(info_key_array)/(obj_len*info_key_len) #计算两个向量的夹角余弦值
            vec_cos[k] = cos_angel # 将计算得到的余弦相似度连同infobox的条目加入字典
        else:
            vec_cos[k] = -1

    cos_sorted = sorted(vec_cos.items(), key=lambda d: d[1]) # 对得到的vec_cos依据value(相似度)进行排序，返回的cos_sorted是一个list
    for i in range(min(5,len(cos_sorted))):
        result_key = cos_sorted[-1-i][0]
        result = infobox[result_key]
        if type(result) == list:
            result = ''.join(result)
        recommend[vec_cos[result_key] * p1] = [title,result_key,result] # 将推荐的result及对应的置信度加入recommend之中返回，传回上级函数
        #print(result_key, result, vec_cos[result_key])
    return
