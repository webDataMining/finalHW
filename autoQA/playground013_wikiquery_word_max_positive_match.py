# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/24/2016   11:41

import loadWikiTitleTrieTreeDump as wttt
import playground_utility as pu

wiki_tree = wttt.wiki_titles_trie_tree
# match = wiki_tree.postive_max_match_root_node('北京')
# print(match)
# print(len(match))
# print('EOF')


def match_wikipedia_title_in_sentence(sentence: str, min_word_len: int=2)->list:
    out = []
    while len(sentence) > 0:
        match = wiki_tree.postive_max_match_root_node(sentence)
        # print(match, len(match))
        if len(match) > 0:
            if len(match) >= min_word_len:
                out.append(match)
            sentence = sentence[len(match):]
        else:
            sentence = sentence[1:]
    return out

if __name__ == '__main__':
    # ques_str = '南水北调工程的“水”主要指的是哪条江河'
    # match_wikipedia_title_in_sentence(ques_str)
    questions = pu.read_full_questions_with_id()
    out_file = open('z_full_questions_wikipedia_title_match.txt', 'w', encoding='utf-8')
    for question in questions:
        wiki_titles = match_wikipedia_title_in_sentence(question.content)
        out_file.write(str(question.id))
        out_file.write('\t')
        out_file.write(question.content)
        out_file.write('\t')
        out_file.write(','.join(wiki_titles))
        out_file.write('\n')




