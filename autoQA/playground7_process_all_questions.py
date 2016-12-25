# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   09:26

import Question as q
import questionAnalysis as qana
import workflow as wf
import workflow_multi_form as wfmf
import playground_utility as pu


questions = pu.read_question_with_id()
# with open('questions_sample_with_id.txt', 'r', encoding='utf-8') as f:
#     for line in f:
#         id, content = line.split()
#         content = qana.complete_question_string(content)
#         questions.append(q.Question(id, content))

with open('question_recommend_sentences_multi_form.txt', 'w', encoding='utf-8') as fout:
    for ques in questions:
        print(ques)
        high_scores = wfmf.workflow_multi_form(ques)
        fout.write(str(ques))
        fout.write('\n')
        fout.write(str(high_scores))
        fout.write('\n')
