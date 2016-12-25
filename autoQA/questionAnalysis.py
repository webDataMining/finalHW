# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/12/2016   19:59

# 问题补全 -》 答案类型推断  -》   答案抽取

import Sentence as s
import re
import commonVar as c
import Question as q


class AnswerType:
    # 表示答案类型
    # 问题分类参考硕士学位论文：中文自动问答系统中问题理解技术的研究_吕德新
    # 没有约束的话，用None表示
    def __init__(self, direct_name:str, pos_tag_rules: list, name_entity_rules: list=None, semantic_dep_rules: list=None):
        self.direct_name = direct_name
        self.pos_tag_rules = pos_tag_rules
        self.name_entity_rules = name_entity_rules
        self.semantic_dep_rules = semantic_dep_rules

    def sentence_match_score(self, sentence: s.Sentence)->float:
        # 搜索句子中匹配的词
        # 不使用语义依存
        # 如果存在命名实体匹配，则返回1，如果存在pos_tag匹配，则返回0.5
        for entity in list(sentence.get_named_entities()):
            if self.match_entity_rules(entity):
                return 0.5
        for pos_tag in sentence.get_pos_tags():
            if self.match_pos_tag_rules(pos_tag):
                return 0.25
        return 0

    def match_entity_rules(self, entity_tag: str):
        if self.name_entity_rules is None:
            return False
        for rule in self.name_entity_rules:
            if entity_tag[1] == rule:
                return True
        return False

    def match_pos_tag_rules(self, pos_tag: str):
        if self.pos_tag_rules is None:
            return False
        for rule in self.pos_tag_rules:
            if pos_tag == rule:
                return True
        return False



    def sentence_match_words(self, sentence: s.Sentence):
        pass




location_name_1 = re.compile(r'(地点|地区)是？')
def location_name_1_replacement(matchobj):
    return matchobj.group(1) + '是哪里？'
# TODO 可以从问题中学习这个提取模板，比如，查找问题中 XXX 是 谁？的问题，从而扩展模板
# 进一步地，可以用已经分好类的问句进行学习
person_name_1 = re.compile(r'(作者|女性|男性|化学家|诗人|扮演者|导演|创始人|校长)是？')
def person_name_1_replacement(matchobj):
    return matchobj.group(1) + '是谁？'
other_1 = re.compile(r'是？')

time_point_1 = re.compile(r'哪年|哪一年|几月几号|几月几日|哪个月|哪天|什么时间|什么时候|何时')

def complete_question_string(question: str)->str:
    # 在字符串意义上补全问题
    if question.endswith('?'):
        question = question[:-1]
    if not question.endswith('？'):
        question += "？"
    question = _complete_question_string_interrogative_pronoun(question)
    return question

def _complete_question_string_interrogative_pronoun(question: str)->str:
    # 一些简单的补全疑问词的规则
    question = location_name_1.sub(location_name_1_replacement, question)
    question = person_name_1.sub(person_name_1_replacement, question)
    question = other_1.sub('是什么？', question)
    return question


# def complete_question_obj(question: s.Sentence):
#
#     pass

def _complete_question_interrogative_pronoun(question: s.Sentence)->s.Sentence:
    if not question.contains_interrogative_pronoun():
        # 如果不含疑问词
        main_sen = question

    return question

location_q_rule_1 = re.compile(r'哪个(国家|地区|城市)')

def infer_question_answer_type(question: s.Sentence):
    interrogative_pronouns = ['谁', '哪', '几', '什么', '怎么', '哪里']  # 疑问代词可以匹配特定类型的词
    interrogative_pronouns_answer_type = ['']
    question_answer_type = {'human_person_name': AnswerType('human_person_name', ['nh'], ['Nh']),  # 人物名称
                            'organization_name': AnswerType('organization_name', ['ni'], ['Ni']),  # 组织名称
                            'location_name': AnswerType('location_name', ['nl', 'ns'], ['Ns']),   # 地点名称
                            'time_point': AnswerType('time_point', ['nt'], None, ['Time']),   # 询问时间点  百度成立于1995年
                            'obj_name': AnswerType('obj_name', ['n', 'nh', 'ni', 'nl', 'ns', 'nz'], None),  # 其它实体名称
                            'number_quantity': AnswerType('number_quantity', ['m'], None, ['Quan']),  # 询问数目
                            'unknown': AnswerType('unknown', None)  # 未能分类的类型
                            }
    if question.find_word('谁') or question.find_word('哪位') or ('什么人' in question.content):
        return question_answer_type['human_person_name']
    if question.find_word('哪里') or question.find_word('哪儿'):
        return question_answer_type['location_name']
    if location_q_rule_1.search(question.getContent()):
        return question_answer_type['location_name']
    if question.find_word('多少') or question.find_word('几个'):
        return question_answer_type['number_quantity']
    if time_point_1.search(question.content):
        return question_answer_type['time_point']
    return question_answer_type['unknown']

def infer_question_focus_word(question: s.Sentence)->list:
    # 提取焦点词。
    # 找到疑问词，提取疑问词所在的短语，提取关键词
    interrogative_pronoun = question.get_interrogative_pronoun()
    if interrogative_pronoun:
        # 提取出 疑问代词的父节点，以及该父节点所有的子节点
        grammar_parent_word = interrogative_pronoun.get_grammar_parent_word()
        siblings = grammar_parent_word.get_grammar_dep_child_words()
        siblings.append(grammar_parent_word)
        siblings.sort(key=lambda x: x.index)
        siblings = remove_interrogative_pronouns_and_be_verb(siblings)
        return siblings
    else:
        return None

def remove_interrogative_pronouns_and_be_verb(word_list: list)->list:
    forbidden = ['是', '？']
    forbidden.extend(c.interrogative_pronouns)
    out = []
    for word in word_list:
        if word.content not in forbidden:
            out.append(word)
    return out


is_verb_pattern = re.compile(r'(是)')
sub_sentence_punctuations_pattern = re.compile(r'(，)')

def is_different_alter_form_exist(question:str)->bool:
    if is_verb_pattern.search(question):
        return True
    else:
        return False


def gen_question_alter_form_str(question:str)->str:
    # 将句子转换为陈述句，在进行匹配：
    # 如：中国历史上最杰出的浪漫主义诗人是谁-》 谁是XXXXX
    # 需要考虑“，”的问题

    # 移除句尾的问号
    if question.endswith('？'):
        question = question[:-1]
    if sub_sentence_punctuations_pattern.search(question) is None:
        # 没有小句子
        return _convert_sub_sentence(question) + "？"
    # 有标点分开的小句子
    # sub_sentences = sub_sentence_punctuations_pattern.split(question)
    sub_sentences = re.split(r'，', question)
    for sub in sub_sentences:
        sub = _convert_sub_sentence(sub)
    return '，'.join(sub_sentences) + "?"

def test_gen_question_alter_form_str():
    question = '“世界上最远的距离，不是生与死，而是我站在你的面前，你却不知道我爱你。”出自哪位著名印度大诗人的诗集？'
    print(gen_question_alter_form_str(question))

def _convert_sub_sentence(sentence: str)->str:
    # 传入的句子应不含"？"
    match = is_verb_pattern.search(sentence)
    if match:
        matched_is_verb = match.group(1)
        start_ind = match.start(1)
        end_ind = match.end(1)
        l1 = sentence[:start_ind]
        l2 = sentence[end_ind:]
        return l2 + matched_is_verb + l1
    else:
        # 没匹配上
        return sentence





def test_infer_question_focus_word():
    ques = s.Sentence("最后宣布废除奴隶制度的行政地区是哪里？")
    print(infer_question_focus_word_str(ques))

def infer_question_focus_word_str(question: s.Sentence)->str:
    wl = infer_question_focus_word(question)
    if wl:
        return s.Sentence.word_list_to_str(wl, verbose=True)
    else:
        return "No inter prons found."

def infer_wikipedia_query_word(question: q.Question)->list:
    # 返回wordlist
    return question.get_sentence_obj().get_nouns()




if __name__ == "__main__":
    # ques = s.Sentence("百度总部位于哪里？")
    # type = infer_question_answer_type(ques)
    # print(type.direct_name)
    #
    # ques_2_str = "百度总部的地点是？"
    # ques_2 = s.Sentence(ques_2_str)
    # print(complete_question_string(ques_2_str))
    # test_infer_question_focus_word()
    test_gen_question_alter_form_str()







