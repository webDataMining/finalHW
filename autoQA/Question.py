# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   09:28

import Sentence as s


class Question:
    def __init__(self, id: int, content:str, true_answer = None, alter_form1 = None, focus_words: list = None):
        self.id = id
        self.content = content
        self.alter_form1 = alter_form1
        self.true_answer = true_answer
        self.focus_words = focus_words
        self.__wikipedia_query_words = None
        self.__sentence_obj_ori = None  # 原始句子的sentence obj
        self.__sentence_obj_alter_form = None
        self.has_different_alter_form = False
        # self.focus_words_str = []

    def __str__(self):
        return str(self.__dict__)

    def get_focus_words_str(self):
        if self.focus_words is None:
            return ''
        out = ''
        for word in self.focus_words:
            out += word.content
            out += ','
        out = out[:-1]
        return out

    def get_sentence_obj(self):  # ->s.Sentence:
        if self.__sentence_obj_ori is None:
            self.__sentence_obj_ori = s.Sentence(self.content)
        return self.__sentence_obj_ori

    def get_sentence_obj_alter_form(self):
        if self.__sentence_obj_alter_form is None:
            self.__sentence_obj_alter_form = s.Sentence(self.alter_form1)
        return self.__sentence_obj_alter_form

    def set_sentence_obj(self, s):
        self.__sentence_obj_ori = s

    def get_wikipedia_query_word(self):
        return self.__wikipedia_query_words

    def set_wikipedia_query_word(self, query_words: list):
        self.__wikipedia_query_words = query_words







