# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/20/2016   10:41

import Question as q
import questionAnalysis as qana


def read_question_with_id()->list:
    out = []
    with open('questions_sample_with_id.txt', 'r', encoding='utf-8') as f:
        for line in f:
            id, content = line.split()
            content = qana.complete_question_string(content)
            tmp_q = q.Question(id, content)
            tmp_q.alter_form1 = qana.gen_question_alter_form_str(tmp_q.content)
            out.append(tmp_q)
    answers = []
    with open('questions_sample_answer_with_id.txt', 'r', encoding='utf-8') as f:
        for line in f:
            id, answer = line.split()
            answers.append(answer)

    for i in range(len(out)):
        out[i].true_answer = answers[i]
        out[i].ture_answer = answers[i]
    return out


def read_full_questions_with_id()->list:
    out = []
    with open('z_full_questions_with_id.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if len(line) < 3:
                continue
            id, content = line.split('\t')
            # print(id)
            content = qana.complete_question_string(content)
            tmp_q = q.Question(id, content)
            tmp_q.alter_form1 = qana.gen_question_alter_form_str(tmp_q.content)
            out.append(tmp_q)
    answers = []
    with open('z_full_questions_answer_with_id.txt', 'r', encoding='utf-8') as f:
        for line in f:
            id, answer = line.split()
            answers.append(answer)

    # with open('z_full_questions_wikipedia_title_match.txt', )

    for i in range(len(out)):
        out[i].true_answer = answers[i]
        out[i].ture_answer = answers[i]
    print("There are", len(out), "questions.")
    return out

def write_questions_to_file(questions: list, file_name):
    # 也适用于full questions
    with open(file_name, 'w', encoding='UTF-8') as f:
        for ques in questions:
            f.write(str(ques))
            f.write('\n')