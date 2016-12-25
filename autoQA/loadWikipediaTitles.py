# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com


# load titles from wiki_pedia

titles = []
with open('wiki_titles_sorted.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        titles.append(line)