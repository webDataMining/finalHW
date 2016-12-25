# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   14:31

import playground_utility as pu
import  questionAnalysis as qana
import Sentence as s

questions = pu.read_full_questions_with_id()

for ques in questions:
    ques.focus_words = qana.infer_question_focus_word(s.Sentence(ques.content))

filename = 'z_full_questions_focus_words_ver1.txt'

with open(filename, 'w', encoding='utf-8') as f:
    for ques in questions:
        q_str = '{0}\t{1}\t{2}\n'.format(ques.id, ques.content, ques.get_focus_words_str())
        f.write(q_str)
# pu.write_questions_to_file(questions, file_name= filename)
