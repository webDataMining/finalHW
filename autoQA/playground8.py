# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   09:50

# import Question as q
# import questionAnalysis as qana
# import workflow as wf
import playground_utility as pu



questions = pu.read_question_with_id()

# with open('questions_sample_with_id.txt', 'r', encoding='utf-8') as f:
#     for line in f:
#         id, content = line.split()
#         content = qana.complete_question_string(content)
#         questions.append(q.Question(id, content))

recommends = []
with open('question_recommend_sentences.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if len(line)>1:
            recommends.append(line)


with open('question_recommend_sentences_with_question.txt', 'w', encoding='utf-8') as f:
    for i in range(len(questions)):
        f.write(str(questions[i]))
        f.write('\n')
        f.write(recommends[i])
