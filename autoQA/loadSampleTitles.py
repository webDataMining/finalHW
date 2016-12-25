# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/24/2016   12:45


titles = []
with open('z_wiki_titles_sorted_sample.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        titles.append(line)
