# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/25/2016   13:28

import Question as q
import questionAnalysis as qana
import workflow as wf
import WikipediaEntry as we
import re


ltp_crash_questions = [52, 431, 631, 1006, 1053, 2047, 2963, 3037, 3379]
def run_work_flow():
    file_name = 'z_online_answers_final.txt'
    with open(file_name, 'r', encoding='utf-8') as f:
        with open('z_online_questions_recommend_sentences_part4.txt', 'w', encoding='utf-8') as fout:
            for line in f:
                line = line.strip()
                id, question_str, content = line.split('\t')
                if int(id) < 3380:
                    continue
                question_str = qana.complete_question_string(question_str)
                question = q.Question(id, question_str)
                if not (content.startswith('[[') or content.startswith('{{')):
                    recommend_sentences = content.strip()
                else:
                    if int(question.id) in ltp_crash_questions:
                        continue
                    entries = text_to_entries(content)
                    print(str(question))
                    recommend_sentences = wf.workflow_with_entries_with_window(question.content, entries, question.id)
                fout.write(str(question))
                fout.write('\n')
                fout.write(str(recommend_sentences))
                fout.write('\n')

def text_to_entries(content: str)->list:
    if not (content.startswith('[[') or content.startswith('{{')):
        raise Exception("Format error! must start with [[ or {{")
    content = content.strip('\n\t[{}] ')
    entries = []
    entries_str = content.split(sep=';')
    cnt = -1
    for entry_str in entries_str:
        cnt += 1
        entry_str = entry_str.strip()
        try:
            title, text = entry_str.split(':', maxsplit=1)
            tmp_entry_score = 1 - (cnt/100)
            if tmp_entry_score < 0.1:
                tmp_entry_score = 0.1
            tmp_entry = we.Entry(title, text)
            entries.append((tmp_entry_score, tmp_entry))
        except Exception as e:
            print(entry_str)
            print(e.__cause__)
    return entries


if __name__ == '__main__':
    run_work_flow()






