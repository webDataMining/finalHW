# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/12/2016   19:09


import environmentVar as env
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller

# 初始化分词器
segmentor = Segmentor()
segmentor.load(env.PYLTP_SEGMENTOR_MODEL_PATH)
postagger = Postagger()
postagger.load(env.PYLTP_POSTAGGER_MODEL_PATH)
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(env.PYLTP_NAMEENTITY_MODEL_PATH)  # 加载模型
parser = Parser() # 初始化实例
parser.load(env.PYLTP_GRAMMAR_DEPENDENCY_MODEL_PATH)  # 加载模型
labeller = SementicRoleLabeller() # 初始化实例
labeller.load(env.PYLTP_SEMANTIC_ROLE_MODEL_DIR)  # 加载模型
