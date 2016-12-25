# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   08:40

import search_api as sa
import utility as u


def workflow(question:str, q_id:int, max_n:int = 5, cache_file_name: str = None)->list:
    entry_list = sa.query_whole_question_local(question, q_id=q_id, cache_file_name = cache_file_name)
    high_score_sentences = []
    for entry in entry_list:
        entry_score = entry[0]
        entry_title = entry[1].title
        sentences = u.extract_sentences(question, entry[1].text)
        for sentence in sentences:
            sentence_score = sentence[2] * entry_score
            sentence_text = sentence[1]
            high_score_sentences.append((sentence_score, sentence_text, entry_title))
    high_score_sentences.sort(key=lambda x:x[0], reverse=True)
    return high_score_sentences[:max_n]


def workflow_with_cache(question:str, q_id:int, max_n:int = 5, cache_file_name: str = None)->list:
    entry_list = sa.read_cache(question, q_id=q_id, cache_file_name = cache_file_name)
    high_score_sentences = []
    for entry in entry_list:
        entry_score = entry[0]
        entry_title = entry[1].title
        sentences = u.extract_sentences(question, entry[1].text, version=2)
        for sentence in sentences:
            sentence_score = sentence[2] * entry_score
            sentence_text = sentence[1]
            high_score_sentences.append((sentence_score, sentence_text, entry_title))
    high_score_sentences.sort(key=lambda x:x[0], reverse=True)
    return high_score_sentences[:max_n]


def workflow_with_entries(question: str, entries: list, q_id:int, max_n:int = 5):
    high_score_sentences = []
    for entry in entries:
        entry_score = entry[0]
        entry_title = entry[1].title
        sentences = u.extract_sentences(question, entry[1].text, version=2)
        for sentence in sentences:
            sentence_score = sentence[2] * entry_score
            sentence_text = sentence[1]
            high_score_sentences.append((sentence_score, sentence_text, entry_title))
    high_score_sentences.sort(key=lambda x: x[0], reverse=True)
    return high_score_sentences[:max_n]

def workflow_with_entries_with_window(question: str, entries: list, q_id:int, max_n:int = 5):
    high_score_sentences = []
    for entry in entries:
        entry_score = entry[0]
        entry_title = entry[1].title
        sentences = u.extract_sentences_ver2(question, entry[1].text, version=2)
        for sentence in sentences:
            sentence_score = sentence[2] * entry_score
            sentence_text = sentence[1]
            sentence_after_window = sentence[3]
            high_score_sentences.append((sentence_score, sentence_text, entry_title, sentence_after_window))
    high_score_sentences.sort(key=lambda x: x[0], reverse=True)
    return high_score_sentences[:max_n]



def __test_workflow1():
    ques = '国际海洋法法庭总部位于哪个国家？'
    print(workflow(ques,1))

if __name__ == '__main__':
    __test_workflow1()