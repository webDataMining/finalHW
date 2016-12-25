# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/14/2016   20:23
import pickle

word_vectors = dict()

file = r"H:\BaiduYunDownload\vectors.txt\vectors.txt"


line_cnt = 0
with open(file, encoding='utf-8') as f:
    for line in f:
        line_cnt += 1
        if line_cnt % 10000 == 0:
            print('Line: ', line_cnt)
            print(line[:20])
            # break
        if len(line) > 10:
            ss = line.split()
            vector = []
            for i in range(1, len(ss)):
                vector.append(float(ss[i]))
            word_vectors[ss[0]] = vector

dump = open('word_vectors.dump', 'wb')
pickle.dump(word_vectors, dump)
print(word_vectors['日'])