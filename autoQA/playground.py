# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/10/2016   01:17





# 分词
import unittest
from utility import *

import environmentVar as env
import utility as u


question_test1 = "百度公司的两位创始人是？"
sentence_test1 = "百度公司是一家主要经营搜索引擎服务的互联网公司，于2000年1月1日由李彦宏、徐勇两人创立于北京中关村。"
segmentor = Segmentor()
segmentor.load('H:\BaiduYunDownload\ltp-data-v3.3.1\ltp_data\cws.model')
q_words = segmentor.segment(question_test1)
q_pos_tags = u.postagger.postag(q_words)
s_words = segmentor.segment(sentence_test1)
q_arcs = u.parser.parse(q_words, q_pos_tags)
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in q_arcs))
print(q_arcs[0])

