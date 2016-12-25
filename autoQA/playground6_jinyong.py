# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/14/2016   19:19

# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/14/2016   13:49

# extract sentences from article

import utility as u

with open('金庸.txt', encoding='utf-8') as f:
    text = f.read()

ques_str = "金庸的封笔之作是？"

l = u.extract_sentences(ques_str, text)

for ss in l:
    print(ss)

