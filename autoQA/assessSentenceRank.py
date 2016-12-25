# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/25/2016   12:08

import json
import ast
import statistics

class Result:
    def __init__(self, hit_title1: int = 0, hit_content1: int = 0):
        self.hit_title1 = hit_title1
        self.hit_content1 = hit_content1

def rank(file_name, result = Result()):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    cnt = 0
    scores = []
    while cnt < len(lines):
        print("Question", cnt / 2 + 1, end="\t")
        question = ast.literal_eval(lines[cnt].strip())
        sentences = ast.literal_eval(lines[cnt + 1].strip())
        true_answer = question['ture_answer']
        if len(sentences) > 0:
            if true_answer in sentences[0][1]:
                print("HIT!-Sentence", end="\t")
                result.hit_content1 += 1
            if true_answer in sentences[0][2]:
                print("HIT!-Title", end="\t")
                result.hit_title1 += 1
            tmp_score = 0
            for i in range(5):
                if (true_answer in sentences[i][1]) or (true_answer in sentences[i][2]):
                    tmp_score += 1 / (i + 1)
            scores.append(tmp_score)
            print(tmp_score)
        else:
            scores.append(0)
        cnt += 2
    return scores

if __name__ == '__main__':
    file_name = 'z_sample_questions_recommend_sentences_part1.txt'
    file_name_2 = 'question_recommend_sentences_with_question.txt'
    result1 = Result()
    result2 = Result()
    rank1 = rank(file_name, result1)
    rank2 = rank(file_name_2, result2)
    print(statistics.mean(rank1))
    print(result1.hit_content1)
    print(statistics.mean(rank2))
    print(result2.hit_content1)


