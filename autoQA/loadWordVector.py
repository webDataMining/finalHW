# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/14/2016   21:02

import pickle

file = open('word_vectors_20161214.dump', 'rb')

word_vectors = pickle.load(file)

print(word_vectors['中国'])

