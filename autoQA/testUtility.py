# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/10/2016   01:15
from utility import *
import unittest


# from pyltp import Segmentor

import logging
loglevel = logging.DEBUG
logging.basicConfig(level=loglevel)
logger = logging.getLogger(__name__)



question_test1 = "百度公司的两位创始人是？"
sentence_test1 = "百度公司是一家主要经营搜索引擎服务的互联网公司，于2000年1月1日由李彦宏、徐勇两人创立于北京中关村。"
# segmentor = Segmentor()
# segmentor.load('H:\BaiduYunDownload\ltp-data-v3.3.1\ltp_data\cws.model')
q_words = segmentor.segment(question_test1)

s_words = segmentor.segment(sentence_test1)
pos_q_words = postagger.postag(q_words)
for word in pos_q_words:
    print(word)


class TestUtiliy():
    def test_oneGramSim(self):
        logger.debug(oneGramSimScore(q_words, s_words))


if __name__ == "__main__":
    test = TestUtiliy()
    test.test_oneGramSim()