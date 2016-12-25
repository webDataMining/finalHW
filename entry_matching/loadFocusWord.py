# coding=utf-8
# author: Pengfei WANG
# Dec/23/2016

from itertools import product

find_focus = [] # 定义得到的‘查询词-焦点词’对的list
string = []
question = []

#file = open('question_wikipedia_query_word.txt', 'r')
with open('z_full_questions_wikipedia_title_match.txt', 'r') as f:
    string = f.readlines()    
    for i in range(len(string)):
        s = string[i]
        s_data = s.split()
        question.append(s_data[1])
        focus = s_data[-1]
        focus_word = focus.split(',')
        find_focus.append(list(product(focus_word,focus_word)))
    #print(type(question[0]))

