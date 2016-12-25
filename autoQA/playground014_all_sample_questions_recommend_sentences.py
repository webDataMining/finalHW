# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/25/2016   11:36

import playground_utility as pu
import workflow as wf


questions = pu.read_question_with_id()
cache_file_name = r'../autoQADataSample/question_wikipedia_contents_qid_'

true_answer_cnt = 0

# ffout = open('z_sample_questions_recommend_sentences_answer_in_first.txt', 'w', encoding='utf-8')

with open('z_sample_questions_recommend_sentences_part1.txt', 'w', encoding='utf-8') as fout:
    for question in questions:
        print(str(question))
        high_scores = wf.workflow_with_cache(question.content, question.id, cache_file_name = cache_file_name)
        fout.write(str(question))
        fout.write('\n')
        fout.write(str(high_scores))
        fout.write('\n')
        if len(high_scores) > 0:
            if (question.true_answer in high_scores[0][1]) or (question.true_answer in high_scores[0][2]):
                true_answer_cnt += 1
                print("HIT!")
                # ffout.write(str(question))
                # ffout.write('\n')
                # ffout.write(str(high_scores))
                # ffout.write('\n')

print(true_answer_cnt)

