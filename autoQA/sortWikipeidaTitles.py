# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/17/2016   15:28



with open('wiki_titles_zhs.txt', 'r', encoding='utf-8') as f:
    titles = f.readlines()
titles.sort()
with open('wiki_titles_sorted.txt', 'w', encoding='utf-8') as f:
    f.writelines(titles)