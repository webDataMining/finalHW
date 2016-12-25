# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/13/2016   11:13

# 处理问题
import questionAnalysis as qana

questions = []
q_id = 0

with open('样例数据.txt', encoding='utf-8') as f:
    with open('questions_sample_with_id.txt', 'w', encoding='utf-8') as out:
        with open('questions_sample_answer_with_id.txt', 'w', encoding='utf-8') as out_answers:
            for line in f:
                words = line.split()
                if len(words) < 2:
                    continue
                question = words[0]
                if question not in questions:
                    questions.append(question)
                    q_id += 1
                else:
                    continue
                question = qana.complete_question_string(question)
                answer = words[1]
                out.write(str(q_id))
                out.write('\t')
                out.write(question)
                out.write('\n')
                out_answers.write(str(q_id))
                out_answers.write('\t')
                out_answers.write(answer)
                out_answers.write('\n')
