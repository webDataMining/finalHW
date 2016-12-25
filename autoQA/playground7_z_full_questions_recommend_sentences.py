# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   09:26

import Question as q
import questionAnalysis as qana
import workflow as wf
import workflow_multi_form as wfmf
import playground_utility as pu


questions = pu.read_full_questions_with_id()

ltp_crash_question_ids = [430,448,449,656,2275,2489,3158,4164,4188,4189,4664,5071,5488,5541,5890]

cache_file_name = '../autoQAData/question_wikipedia_contents_qid_'

with open('z_full_questions_recommend_sentences_ver3_part2.txt', 'w', encoding='utf-8') as fout:
    for ques in questions:
        if int(ques.id) < 1414:
            continue
        if int(ques.id) in ltp_crash_question_ids:
            continue
        print(ques)
        high_scores = wf.workflow_with_cache(ques.content, ques.id, cache_file_name= cache_file_name)
        fout.write(str(ques))
        fout.write('\n')
        fout.write(str(high_scores))
        fout.write('\n')
