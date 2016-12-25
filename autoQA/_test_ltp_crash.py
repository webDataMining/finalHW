# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/14/2016   19:22

import Sentence as s
import initializeLTP as ltp
import time

# senlist = list(ltp.SentenceSplitter.split("金庸，大紫荆勋贤，OBE（英语：Louis Cha Leung-yung[注 1]，1924年3月10日－[1]），本名查良镛，浙江海宁人，武侠小说泰斗，1948年移居香港。自1950年代起，以笔名“金庸”创作多部脍炙人口的武侠小说，包括《射雕英雄传》、《神雕侠侣》、《倚天屠龙记》、《天龙八部》、《笑傲江湖》、《鹿鼎记》等，历年来金庸笔下的著作屡次改编为电视剧、电影等，对华人影视文化可谓贡献重大，亦奠定其成为华人知名作家的基础。金庸早年于香港创办《明报》系列报刊，他亦被称为“香港四大才子”之一。亦是已故知名诗人徐志摩之表弟[2]。"))
#
# for sen in senlist:
#     print(sen)
#     s.Sentence(sen)

#
# with open('金庸.txt', encoding='utf-8') as f:
#     for line in f:
#         line.strip()
#         senlist = ltp.SentenceSplitter.split(line)
#         for sen in senlist:
#             print(sen)
#             try:
#                 s.Sentence(sen)
#             except:
#                 print('Exception!')

with open('test_ltpcrash.txt', encoding='utf-8') as f:
    text = f.read()
    # text = text.strip()
print(text)

texts = []
for tt in text.split('。'):
    texts.append(tt + '。')
for text in texts:
    print(text)
    senlist = list(ltp.SentenceSplitter.split(text))
    print('  splitted')
    print(senlist)
    for sen in senlist:
        print(sen)
        try:
            s.Sentence(sen)
            print('  created')
            time.sleep(1)
        except:
            print('Exception!')
