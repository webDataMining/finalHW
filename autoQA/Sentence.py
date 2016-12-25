# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/11/2016   09:48

import requests
import commonVar as c
import environmentVar as env
import initializeLTP as u
import interrogativePronoun as ipron
from Word import Word


class Sentence:
    def __init__(self, s: str):
        self.content = s
        self.words = []
        self.pos_tags = []
        self.entities = []
        self.grammarDependencyTree = None
        self.grammarDependencyFlat = []
        self.semanticRoles = []
        self.semanticDependencyTree = None
        self.semanticDependencyFlat = []
        self.word_len = -1
        self.word_len = -1
        self.window_after = ""
        self.analyze()

    def analyze(self):
        '''
        准备好句子中的各种分析
        :return:
        '''
        self.words = u.segmentor.segment(self.content)
        self.word_len = len(self.words)
        self.pos_tags = u.postagger.postag(self.words)
        self.entities = u.recognizer.recognize(self.words, self.pos_tags)
        self.grammarDependencyFlat = u.parser.parse(self.words, self.pos_tags)
        self.semanticRoles = u.labeller.label(self.words, self.pos_tags, self.entities, self.grammarDependencyFlat)
        # self.entities = [-1 for i in  range(len(self.words))]


    def analyze_grammar_dependency(self):
        pass


    def get_compact_entities(self)->list:
        # 可以将结果缓存以优化性能
        out = []
        for i in range(self.word_len):
            if self.entities[i] != 'O':
                out.append(self.words[i] + "\\" + self.entities[i])
        return out

    def __str__(self):
        outputstr = ''
        outputstr += 'Content: ' + self.content + '\n'
        for i in range(len(self.words)):
            outputstr += str(i) + ' {0}, {1}, {2}, {3}:{4}\n'.format(self.words[i], self.pos_tags[i], self.entities[i],
                                                                     self.grammarDependencyFlat[i].head, self.grammarDependencyFlat[i].relation)
        return outputstr

    def get_semantic_dependency(self)-> list:
        # 一开始就做得尽量简单，不要想那么复杂
        if len(self.semanticDependencyTree) <= 0:
            pay_load = {'api_key': env.ltp_api_key,
                        'pattern': 'sdp',
                        'format': 'plain',
                        'text': self.content}
            r = requests.get(env.ltp_url, params=pay_load)
            relationships = r.text.split('\n')
            for relationship in relationships:
                self.semanticDependencyTree.append(relationship.split())
        return self.semanticDependencyTree

    def getSemanticDependencyFlat(self)->list:
        if len(self.semanticDependencyFlat) > 0:
            return self.semanticDependencyFlat
        # 通过api获取语义角色
        pass

    def getWordAt(self, index: int):
        if index == -1:
            return Word(self, 'Root', index, 'Null', 'Null', None)
        else:
            return Word(self, self.words[index], index, self.pos_tags[index], self.entities[index], self.grammarDependencyFlat[index])

    def find_word(self, word: str, start_ind: int = 0)-> Word:
        # 对词语进行精确匹配
        for i in range(start_ind, self.word_len):
            if word == self.words[i]:
                return self.getWordAt(i)
        return None

    # def get_root_gammar_dep(self):
    #     # 返回第一层的句子关系，也即主干句子
    #     for i in range(self.word_len):
    #         arc = self.getGrammarDependencyFlat()[i]
    #         if arc.relation == 'HED':
    #             hed_ind = i
    #     # 找到所有从HED直接出发的箭头
    #     hed_word = self.getWordAt(hed_ind)
    #     return hed_word.get_grammar_dep_child_words()

    def get_root_grammar_dep_with_hed(self):
        # 返回第一层的句子关系，也即主干句子
        for i in range(self.word_len):
            arc = self.getGrammarDependencyFlat()[i]
            if arc.relation == 'HED':
                hed_ind = i
        # 找到所有从HED直接出发的箭头
        hed_word = self.getWordAt(hed_ind)
        l = hed_word.get_grammar_dep_child_words()
        l.append(hed_word)
        l.sort(key=lambda x: x.index)
        return l

    @classmethod
    def word_list_to_str(cls, l: list, verbose=False)->str:
        out = ''
        simple = ''
        for word in l:
            simple += word.content
            out += str(word) + '   '
        if verbose:
            return simple + '   ' + out
        else:
            return simple

    def get_root_grammar_dep_str(self):
        l = self.get_root_grammar_dep_with_hed()
        out = ''
        simple = ''
        for word in l:
            simple += word.content
            out += str(word) + '   '
        return simple + '   ' + out

    def get_root_grammar_dep_with_more(self):
        # 包括对句中名词的修饰关系的基本句意
        root_l = self.get_root_grammar_dep_with_hed()
        for word in root_l:
            if word.is_noun():
                root_l.extend(word.get_grammar_dep_child_words())
        root_l.sort(key=lambda x: x.index)
        return root_l

    def get_nouns(self)->list:
        out = []
        for i in range(self.word_len):
            if self.get_pos_tags()[i] in c.noun_pos_tags:
                out.append(self.getWordAt(i))
        return out


    def contains_interrogative_pronoun(self)-> Word:
        # 如果有，返回疑问代词，如果没有，返回None
        for i in range(self.word_len):
            if ipron.is_interrogative_pronoun(self.getWordAt(i)):
                return self.getWordAt(i)
        return None

    def get_interrogative_pronoun(self)->Word:
        return self.contains_interrogative_pronoun()

    def get_named_entities(self)->list:
        out = []
        cur_entity = ''
        i = 0
        while i < self.word_len:
            if self.entities[i].startswith('B'):
                cur_entity += self.words[i]
                while True:
                    i += 1
                    if i >= self.word_len:
                        print("ERROR in get_named_entities: ", self.content)
                        return out
                    cur_entity += self.words[i]
                    if self.entities[i].startswith('E'):
                        out.append((cur_entity, self.entities[i][2:]))
                        cur_entity = ''
                        break
            if self.entities[i].startswith('S'):
                out.append((self.words[i], self.entities[i][2:]))
            i += 1
        return out



    ## simple getters
    def getGrammarDependencyFlat(self)->list: return self.grammarDependencyFlat
    def getWords(self)->list: return self.words
    def getSemanticRoles(self)->list: return self.semanticRoles
    def getContent(self)->str: return self.content
    def get_pos_tags(self)->list: return self.pos_tags


class SenNode:
    def __init__(self, content: str):
        self.content = content
        self.parentNode = None
        self.childNodes = []


class SenRoot(SenNode):
    def __init__(self, content: str):
        SenNode(content)





if __name__ == '__main__':
    question_test1 = "百度公司的两位创始人是谁？"
    # question_test1 = "最后宣布废除奴隶制度的行政地区是哪里？"
    s = Sentence(question_test1)
    print(s)
    print(s.get_named_entities())
    # for word in s.get_root_gammar_dep_str(): print(word)
    # print(s.get_root_grammar_dep_str())
