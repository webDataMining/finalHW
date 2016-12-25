# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/14/2016   13:49

# extract sentences from article

import utility as u

with open('国际海洋法法庭.txt', encoding='utf-8') as f:
    text = f.read()

ques_str = "国际海洋法法庭的总部位于哪个国家？"

l = u.extract_sentences(ques_str, text)

for ss in l:
    print(ss)

