# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/13/2016   11:34

import questionAnalysis as qana
import Sentence as s


line_cnt = 0
unknown_cnt = 0

with open('questions_sample.txt', 'r', encoding='utf-8') as f:
    with open('questions_sample_type.txt', 'w', encoding='utf-8') as out:
        for line in f:
            line_cnt += 1
            line = line.strip()
            line = qana.complete_question_string(line)
            question = s.Sentence(line)
            type = qana.infer_question_answer_type(question)
            out.write(line)
            out.write('\t')
            out.write(type.direct_name)
            if type.direct_name == 'unknown': unknown_cnt += 1
            out.write('\t')
            out.write(s.Sentence.word_list_to_str(question.get_root_grammar_dep_with_hed()))
            out.write('\t')
            out.write(qana.infer_question_focus_word_str(question))
            out.write('\n')

print('There are', unknown_cnt,'unknowns in', line_cnt, 'questions')