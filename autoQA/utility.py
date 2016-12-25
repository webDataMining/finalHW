# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/09/2016   20:35



import pyltp
import pprint
import Sentence as smodule
import questionAnalysis as qana
import Question as q
import re

pp = pprint.PrettyPrinter()



#

sentence_splitter = re.compile(r'。|？|\?|!|…')


def test_extract_sentences_ver2():
    article = " 这是因为空气里哪种蓝色气体的含量增加了？臭氧 38、历史事件戚继光抗倭发生在哪个朝代？明朝 39、历史事件王莽篡夺王位改国号为新，是篡夺的哪个朝代的王权？汉朝"
    extract_sentences_ver2(None, article)


def extract_sentences_ver2(question:str, article:str, n:int = 5, version: int=0, window_after: int = 10)->list:
    # 自行实现句子切分
    match_iter = sentence_splitter.finditer(article)
    sentences = []
    sentences_after_window = []

    cur_sentence_start_ind = 0
    cur_sentence_end_ind = 0
    cnt = 0
    for match in match_iter:
        cnt += 1
        cur_sentence_end_ind = match.end()
        cur_sentence = article[cur_sentence_start_ind:cur_sentence_end_ind]
        after_window_ind = cur_sentence_end_ind + window_after
        if after_window_ind >= len(article):
            pad_space = ''
            for i in range(after_window_ind - len(article) + 1):
                pad_space += ' '
            article += pad_space
        cur_sentence_after_window = article[cur_sentence_end_ind: after_window_ind]
        sentences.append(cur_sentence)
        sentences_after_window.append(cur_sentence_after_window)
        cur_sentence_start_ind = match.end()
    if cnt == 0:
        sentences.append(article)
        pad_space = ''
        for i in range(window_after):
            pad_space += ' '
        sentences_after_window.append(pad_space)

    # print(sentences)
    # print(sentences_after_window)
    scores = []
    ind = 0
    question = smodule.Sentence(question)
    question_obj = q.Question('-1', question.content)
    question_obj.set_sentence_obj(question)
    question_obj.alter_form1 = qana.gen_question_alter_form_str(question.content)
    question_obj.has_different_alter_form = qana.is_different_alter_form_exist(question.content)
    sentence_ind = -1
    for i in range(len(sentences)):
        sentence_obj = smodule.Sentence(sentences[i])
        sentence_obj.window_after = sentences_after_window[i]
        # if True:
        #     print("  Now processing", sentence)
        sentence_ind += 1
        if version == 0:
            scores.append((sentence_ind,
                           sentence_obj.content,
                           calcSentenceSimScore(question, sentence_obj),
                           sentence_obj.window_after))  # (index, setence-str, score)
        if version == 2:
            scores.append((sentence_ind,
                           sentence_obj.content,
                           calcSentenceSimScore_ver2(question_obj, sentence_obj),
                           sentence_obj.window_after))
    for i in range(5):
        scores.append((-1, 'no enough sentences', -100, 'no enough sentences'))  #
    scores.sort(key=lambda x: x[2], reverse=True)
    return scores[:n]  # top n of









def extract_sentences(question:str, article:str, n:int = 5, version: int=0)->list:
    # 从article中抽取出5个最相关的句子
    # TODO 不考虑跨句的信息。
    sentences = pyltp.SentenceSplitter.split(article)
    scores = []
    ind = 0
    question = smodule.Sentence(question)
    question_obj = q.Question('-1', question.content)
    question_obj.set_sentence_obj(question)
    question_obj.alter_form1 = qana.gen_question_alter_form_str(question.content)
    question_obj.has_different_alter_form = qana.is_different_alter_form_exist(question.content)
    sentence_ind = -1
    for sentence in sentences:
        # if True:
        #     print("  Now processing", sentence)
        sentence_ind += 1
        if version == 0:
            scores.append((sentence_ind,
                           sentence,
                           calcSentenceSimScore(question, smodule.Sentence(sentence))))  # (index, setence-str, score)
        if version == 2:

            scores.append((sentence_ind,
                           sentence,
                           calcSentenceSimScore_ver2(question_obj, smodule.Sentence(sentence))))
    for i in range(5):
        scores.append((-1, 'no enough sentences', -100))  #
    scores.sort(key=lambda x:x[2], reverse=True)
    return scores[:n]  # top n of


def calcSentenceSimScore(question: smodule.Sentence, sentence: smodule.Sentence)->float:
    return oneGramSimScore(question, sentence)\
           + entitySimScore(question, sentence)\
           + flatGrammarDependencySimScore(question, sentence) / sentence.word_len


def calcSentenceSimScore_ver2(question_obj, sentence: smodule.Sentence)->float:
    # question_obj : q.Question
    question = question_obj.get_sentence_obj()
    if sentence.word_len == 0:
        return 0
    return oneGramSimScore(question, sentence)\
           + entitySimScore(question, sentence)\
           + flat_grammar_dependency_sim_score_ver2(question_obj, sentence) / len(sentence.grammarDependencyFlat) \
           + contains_question_answer_type_sim_score(question, sentence) \
           + interrogative_sentence_penalty(question, sentence)


def contains_question_answer_type_sim_score(question: smodule.Sentence, sentence: smodule.Sentence)->float:
    question_answer_type = qana.infer_question_answer_type(question)
    score =  question_answer_type.sentence_match_score(sentence)
    # if score > 0:
    #     print("   ", question_answer_type.direct_name)
    #     print("   ", score)
    return score

def interrogative_sentence_penalty(question: smodule.Sentence, sentence: smodule.Sentence)->float:
    if sentence.content.endswith('?') or sentence.content.endswith('？'):
        return 0
    else:
        return 0


def oneGramSimScore(question: smodule.Sentence, sentence: smodule.Sentence)->float:
    # 问题：偏向短句子，没有去除停用词
    # 其它的特征，如实体，句法依存树，语法依存树
    return _one_gram_sim_score_general(question.getWords(), sentence.getWords())

def _one_gram_sim_score_general(question_list: list, sentence_list: list):
    q_set = set(question_list)
    s_set = set(sentence_list)
    u_set = q_set.union(s_set)
    intersection_set = q_set.intersection(s_set)
    if len(u_set) == 0:
        return 0
    return len(intersection_set) / len(u_set)

def entitySimScore(question, sentence)->float:
    '''
    实体相似性得分。
    将两个句子中的实体抽取出来，计算相似度
    :param question: Sentence
    :param sentence:
    :return:
    '''
    q_entities = question.get_compact_entities()
    s_entities = sentence.get_compact_entities()
    return _one_gram_sim_score_general(q_entities, s_entities)

# def similarity



def grammerDependencySimScore(question: smodule.Sentence, sentence: smodule.Sentence)->float:
    '''
    语法依存相似度得分
    如果和问句有着相似的语法依存结构，那么很可能含有答案
    参考文章：
    :param question:
    :param sentence:
    :return:
    '''
    pass


def flat_grammar_dependency_sim_score_ver2(question, sentence: smodule.Sentence)->float:
    # 取两种形式的问句中的最高分
    # question :q.Question
    if question.has_different_alter_form:
        score1 = flatGrammarDependencySimScore(question.get_sentence_obj(), sentence)
        score2 = flatGrammarDependencySimScore(question.get_sentence_obj_alter_form(), sentence)
        return max(score1, score2)
    else:
        return flatGrammarDependencySimScore(question.get_sentence_obj(), sentence)

def flatGrammarDependencySimScore(question: smodule.Sentence, sentence: smodule.Sentence)->float:
    '''
    不太考虑树结构的语法依存关系
    参考文章：基于语义依存关系匹配的汉语句子相似度计算
    算法：简单匹配    依存关系一样 且 论元一样的句子
    升级：可以考虑使用word embedding进行词义相似度的计算
    注意：疑问词当做通配符处理
    注意：得分没有经过标准化
    TODO    仅仅考虑句子中的主要成分呢： 主 谓 宾
    :param question:
    :param sentence:
    :return:
    '''
    targetRelations = ['SBV', 'VOB', 'POB', 'COO', 'ATT', 'APP']
    # for arc in targetRelations:
    #     q_arcs = []
    #     s_arcs = []
    #     for q_arc in question.getGrammarDependencyFlat():
    #         if q_arc.relation == arc:
    #             q_arcs.append([q_arc, qu])
    score = 0
    for i in range(question.word_len):
        for j in range(sentence.word_len):
            if question.getGrammarDependencyFlat()[i].relation == sentence.getGrammarDependencyFlat()[j].relation and (question.getGrammarDependencyFlat()[i].relation in targetRelations):
                # 关系类型匹配
                score += flatGrammarRelationSimScore(i, question, j, sentence)
    return score



wild_words = ['谁', 	'哪',	'几',	'什么',	'怎么',	'哪里']  # 疑问代词可以匹配特定类型的词
def flatGrammarRelationSimScore(q_index:int, question: smodule.Sentence, s_index: int, sentence: smodule.Sentence)->float:
    '''
    仅匹配关系和论元都相同的关系
    :param q_index:
    :param question:
    :param s_index:
    :param sentence:
    :return:
    '''
    if question.getGrammarDependencyFlat()[q_index].relation != sentence.getGrammarDependencyFlat()[s_index].relation:
        return 0  # 如果类型不匹配，返回0
    q_arg1 = question.getWords()[q_index]
    q_arg2_ind = question.getGrammarDependencyFlat()[q_index].head
    q_arg2 = question.getWords()[q_arg2_ind]
    s_arg1 = sentence.getWords()[s_index]
    s_arg2_ind = sentence.getGrammarDependencyFlat()[s_index].head
    s_arg2 = sentence.getWords()[s_arg2_ind]
    if q_arg1 in wild_words and q_arg2 == s_arg2:
        # print("  Recommend answer: " + s_arg1 + "  Sentence:" + sentence.content)
        return 1
    if q_arg2 in wild_words and q_arg1 == s_arg1:
        # print("  Recommend answer: " + s_arg2 + "  Sentence:" + sentence.content)
        return 1
    if q_arg1 == s_arg1 and q_arg2 == s_arg2:
        return 1
    return 0


def flatSemanticDependencySimScore(question: smodule.Sentence, sentence: smodule.Sentence)->float:
    targetRelations = ['SBV', 'VOB', 'POB', 'COO', 'ATT', 'APP']
    score = 0
    for i in range(question.word_len):
        for j in range(sentence.word_len):
            if question.getGrammarDependencyFlat()[i].relation == sentence.getGrammarDependencyFlat()[j].relation and (question.getGrammarDependencyFlat()[i].relation in targetRelations):
                # 关系类型匹配
                score += flatGrammarRelationSimScore(i, question, j, sentence)
    return score



# def questionAnswerType():
#
#     pass
#
#
# def sentenceTreeSimScore(question, sentence):
#     '''
#     各种句子树的相似度得分
#     :return:
#     '''
#     pass



if __name__ == "__main__":
    # with open('toyTextBaidu.txt', encoding='utf-8') as file:
    #     text = file.read()
    #     question_test = "百度公司的两位创始人是谁？"
    #     sen2 = "百度公司的创始人是李彦宏和徐勇。"
    #     sentence_test1 = "百度公司是一家主要经营搜索引擎服务的互联网公司，于2000年1月1日由李彦宏、徐勇两人创立于北京中关村。"
    #     # print(entitySimScore(smodule.Sentence(question), smodule.Sentence(sentence_test1)))
    #     print(flatGrammarDependencySimScore(smodule.Sentence(question_test), smodule.Sentence(sen2)))
    test_extract_sentences_ver2()