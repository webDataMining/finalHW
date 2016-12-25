#!/usr/bin/env python  
# Python 3.5
# -*- coding: utf-8 -*-
#author: Pengfei WANG
#time: 2016.12.17

#from english_translation import *
from english_translation import *
from infobox_pro import *
from loadFocusWord import *
from loadWordVector import *
import requests  
import json

# 将‘查询词-焦点词’对导入，进行查询
'''
for iteration in range(len(find_focus)):
	ques_item = find_focus[iteration]
	for j in range(len(ques_item)):
		obj = ques_item[j][0]
		search_word = ques_item[j][1]
		if obj == search_word:
			continue
'''
ans_recommend = {}
iteration = 0
while iteration < 7000:
# iteration = 2
#if iteration == 8:
	ques_item = find_focus[iteration]
	print(string[iteration]) # 打印问题
	result_f = open('result.txt', 'r+')
	result_f.read()
	result_f.write("\n"+string[iteration])
	result_f.close()

	iteration = iteration+1
	ans_list = {}

	for j in range(len(ques_item)):
		obj = ques_item[j][0]
		search_word = ques_item[j][1]
		if obj == search_word:
			continue

		# 初始化
		findit = False
		findinfobox = 0
		infobox = []
		recommend = {}
		info_key_vec = {}

		obj_en = str(translate(obj))

		web = requests.get("http://search.fanzhikang.cn/api/?range=local&title="+search_word)  
		#web = requests.get("http://search.fanzhikang.cn/api/?range=local&title=约翰·福布斯·纳什")  
		info = json.loads(web.text)
#		with open('wiki.txt', 'r+') as f:
#			f.read()
#			f.write(str(info))

		data = info['data']['results']
		blocknum = len(data)#表示这里针对需要的词条查询得到了blocknum条结果，每个block对应一个title和一个text

		#下面的思路是：1.针对每个title进行对问题的匹配，得到置信度p1（如果title中的文字在查询项中出现，那么置信度高，否则按照词义匹配进行置信度的计算）
		#			2.按置信度对词条进行排序（list形式排序）从前到后进行text中的infobox查询，总共提取最多3个infobox，针对每个infobox：(另一个函数)
		#				2.1 先进行一轮字符串匹配（中英文同时进行），如果匹配上了，那就直接返回结果，跳过以后的步骤
		#				2.2 当第一轮字符串匹配失败时，进行第二轮词义匹配，将infobox里的k-v对中所有的key（去除下划线）值翻译成中文(利用replace命令去掉“的”)
		#				2.3 针对每一个处理过的key值，将key与目标词汇进行词义匹配，计算余弦相似度(作为置信度p2)，并将英文key和相似度以字典方式存入vec_cos中
		#				2.4 对vec_cos依据value进行排序，将前五个词条作为这个infobox的推荐答案，置信度为p1*p2

		for i in range(blocknum):
		    if findit == True:
		    	break
		    if findinfobox == 3:
		        break			

		    # 如果这个模块中有meta_boxes，那么匹配关键词
		    if 'meta_boxes' in data[i].keys():
		        if findinfobox == 0:
		            p1 = 1.0
		        elif findinfobox == 1:
		            p1 = 0.75
		        else:
		            p1 = 0.5

		        title = data[i]['title']

		        meta = data[i]['meta_boxes']
		        infobox = list(meta.values())[0]
		        if type(infobox) != dict:
		        	continue

		        findinfobox = findinfobox + 1

		        infobox_process(infobox,findit,obj_en,obj,recommend,p1,info_key_vec,title) # 现在得到了recommend的5条推荐答案及置信度（recommend之中存储的是不针对单一一个title的数据）

		# 当得到每种“obj-search_word”组合的3个title的15条recommend答案之后，将所有组合找到的答案排序并输出
		#print(blocknum,i)
		ans_list.update(recommend)
		recommend_final = sorted(recommend.items(), key=lambda d: d[0]) # 正序，就是现在从小到大排列的
		recommend_final.reverse() # 倒序
		
		print(search_word,obj)
		print(recommend_final[0:min(10,len(recommend_final))]) # 输出置信度排名前10的答案 

		with open('result.txt', 'r+') as f:
			f.read()
			f.write("\n查询词："+search_word+" 匹配词："+obj+"\n")
			f.write(recommend_final[0:min(10,len(recommend_final))].__str__())

	ans_sort = sorted(ans_list.items(), key=lambda d: d[0])
	ans_sort.reverse()
	recom_value = []
	for q in range(len(ans_sort)):
		if q < 5:
			recom_value.append((ans_sort[q][1][2],ans_sort[q][0]))
		else:
			break
	ans_recommend[question[iteration-1]] = recom_value
	with open('result_recommend.txt', 'r+') as f:
		f.read()
		f.write(str(iteration)+" "+question[iteration-1]+"\n")
		f.write(ans_recommend[question[iteration-1]].__str__()+"\n")

