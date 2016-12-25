# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   11:38


# 支持多种问题形式的workflow
import search_api as sa
import utility as u
import questionAnalysis as qana
import Question as q

def workflow_multi_form(ques: q.Question, max_n: int=10)->list:
    question = ques.content
    q_id = ques.id
    entry_list = sa.query_whole_question_local(question)
    high_score_sentences = []

    for entry in entry_list:
        entry_score = entry[0]
        entry_title = entry[1].title
        print(" ===TITLE : ", entry_title)
        sentences = u.extract_sentences(question, entry[1].text)
        print("  ===alter===")
        sentences.extend(u.extract_sentences(ques.alter_form1, entry[1].text))
        for sentence in sentences:
            sentence_score = sentence[2] * entry_score
            sentence_text = sentence[1]
            high_score_sentences.append((sentence_score, sentence_text, entry_title))
    high_score_sentences.sort(key=lambda x:x[0], reverse=True)
    return high_score_sentences[:max_n]

