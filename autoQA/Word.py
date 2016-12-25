# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/13/2016   13:43

import commonVar as c

class Word:
    def __init__(self, source, content: str, index: int,
                 pos_tag: str, entity_tag: str, grammarDepArc):
        self.source = source  # a sentence obj
        self.content = content
        self.index = index
        self.pos_tag = pos_tag
        self.entity_tag = entity_tag
        self.grammarDepArc = grammarDepArc

    def get_grammar_dep_child_words(self)->list:
        # 语法依存树中的子节点
        l = []
        for i in range(self.source.word_len):
            if self.source.getGrammarDependencyFlat()[i].head == self.index:
                l.append(self.source.getWordAt(i))
        return l

    def is_noun(self):
        return self.pos_tag in c.noun_pos_tags

    def get_grammar_parent_word(self):
        parent_ind = self.source.getGrammarDependencyFlat()[self.index].head
        return self.source.getWordAt(parent_ind)

    @classmethod
    def remove_word_list_duplicates(cls, word_list)->list:
        out = []
        word_strs = []
        for word in word_list:
            if word.content not in word_strs:
                word_strs.append(word.content)
                out.append(word)
        return out


    @classmethod
    def word_list_to_word_content_str_list(cls, word_list: list)->list:
        out = []
        for word in word_list:
            out.append(word.content)
        return out


    def __str__(self):
        return str(self.index) + ' ' + self.content + ', ' + self.pos_tag + ', ' + self.entity_tag + ', ' + '{0}:{1}'.format(self.grammarDepArc.head, self.grammarDepArc.relation)