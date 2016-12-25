# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   15:34

# 查出所有词的维基百科查询词

import questionAnalysis as qana
import playground_utility as pu
import Word as w


questions = pu.read_full_questions_with_id()

# out_file = open('question_wikipedia_query_word.txt', 'w', encoding='utf-8')
out_file = open('z_full_questions_wikipedia_query_word.txt', 'w', encoding='utf-8')


for question in questions:
    question.set_wikipedia_query_word(qana.infer_wikipedia_query_word(question))
    out_file.write(question.id)
    out_file.write('\t')
    out_file.write(question.content)
    out_file.write('\t')
    out_file.write(','.join(w.Word.word_list_to_word_content_str_list(question.get_wikipedia_query_word())))
    out_file.write('\n')






