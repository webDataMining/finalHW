# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/13/2016   20:04
import re

wikidb = open(r"H:\tdownload2\zhwiki-20161101-pages-articles-multistream.xml",encoding='utf-8')

wiki_title = open('wiki_title.txt', 'w', encoding='utf-8')

patt = re.compile(r'<title>([^<].*)</title>')

match = patt.search(r'<title>数学</title>')

line_cnt = 0
title_cnt = 0
titles = []
for line in wikidb:
    line_cnt += 1
    if line_cnt % 10000000 == 0:
        print('Line:', line_cnt)
        print('Title_cnt:', title_cnt)
    match = patt.search(line)
    if match:
        title_cnt += 1
        titles.append(match.group(1) + '\n')
        # wiki_title.write(match.group(1))
        # wiki_title.write('\n')

wiki_title.writelines(titles)

