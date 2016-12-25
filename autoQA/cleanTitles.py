# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/13/2016   20:20

import re

title = open('wiki_title.txt', encoding='utf-8')
out = open('wiki_titles_cleaned.txt', 'w', encoding='utf-8')

invalid_pattern = re.compile(r'Wiki|Cate|Topi|Help|File|Medi')
invalid_pattern2 = re.compile(r':')

for line in title:
    if invalid_pattern2.search(line):
        continue
    out.write(line)