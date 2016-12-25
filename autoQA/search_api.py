# coding=utf-8
# author: WEN Kai, wenkai123111 AT 126.com
# Dec/19/2016   21:02

import requests
import WikipediaEntry as we
import environmentVar as env
import re
import json

def get_wikipedia_entry(key_word, max_n: int = 5)->list:
    # 对于完全匹配的
    if env.verbose_out_print:
        print("   Getting wikipedia entry", key_word)
    api_url = r'http://search.fanzhikang.cn/api/'
    data = {"range": "local",
            "title": key_word }
    result = requests.get(api_url, params=data)
    json_obj = result.json()
    wiki_entries = json_obj['data']['results']
    out = []
    cnt = 0
    for entry in wiki_entries:
        cnt += 1
        if cnt > max_n:
            break
        entry_tmp = we.Entry(entry['title'], entry['text'])
        if 'meta_boxes' in entry:
            entry_tmp.infobox = entry['meta_boxes']
        cnt += 1
        if entry_tmp.title == key_word:
            out.append((1, entry_tmp))
        else:
            out.append((1 - cnt / 10, entry_tmp))  # 保留原有的排序
    return out

def query_whole_question_local(ques:str, max_n: int = 5, q_id: int = -1, cache_file_name: str = None)->list:
    # 若句子中存在所查到词条的title，则该词条具有高评分 1 分
    # 会移除句子末尾的标点
    # q_id 大于=0可以保存返回的数据
    ques = ques.strip()
    if ques.endswith('？'):
        ques = ques[:-1]
    api_url = r'http://search.fanzhikang.cn/api/'
    data = {"range": "local",
            "text": ques }
    try:
        result = requests.get(api_url, params=data, timeout=100)
    except Exception as e:
        print(str(e))
        return []
    json_obj = result.json()
    if int(q_id) >= 0:
        if not cache_file_name:
            file_name = r'../autoQAData/question_wikipedia_contents_qid_' + str(q_id) + '.txt'
        else:
            file_name = cache_file_name + str(q_id) + '.txt'
        with open(file_name, 'wb') as f:
            for chunk in result.iter_content(chunk_size=128):
                f.write(chunk)
    wiki_entries = json_obj['data']['results']
    out = []
    cnt = 0
    for entry in wiki_entries:
        cnt += 1
        if cnt > max_n:
            break
        cleaned_text = re.sub(r'[#\n\r|\[\]]+', "", entry['text'])
        entry_tmp = we.Entry(entry['title'], cleaned_text)
        if 'meta_boxes' in entry:
            entry_tmp.infobox = entry['meta_boxes']
        cnt += 1
        if entry_tmp.title is None:
            entry_tmp.title = 'NO_TITLE'
        if entry_tmp.title in ques:
            out.append((1, entry_tmp))
        else:
            out.append((1 - cnt / 10, entry_tmp))  # 保留原有的排序
    return out

def read_cache(ques:str, max_n: int = 5, q_id: int = -1, cache_file_name: str = None)->list:
    if not cache_file_name:
        file_name = r'../autoQAData/question_wikipedia_contents_qid_' + str(q_id) + '.txt'
    else:
        file_name = cache_file_name + str(q_id) + '.txt'
    with open(file_name, 'r', encoding='utf-8') as f:
        json_text = f.read()
    json_obj = json.loads(json_text)
    return clean_json_content(ques, json_obj, max_n)


def clean_json_content(ques: str, json_obj, max_n: int = 5)->list:
    wiki_entries = json_obj['data']['results']
    out = []
    cnt = 0
    for entry in wiki_entries:
        cnt += 1
        if cnt > max_n:
            break
        cleaned_text = re.sub(r'[#\n\r|\[\]]+', "", entry['text'])
        entry_tmp = we.Entry(entry['title'], cleaned_text)
        if 'meta_boxes' in entry:
            entry_tmp.infobox = entry['meta_boxes']
        cnt += 1
        if entry_tmp.title is None:
            entry_tmp.title = 'NO_TITLE'
        if entry_tmp.title in ques:
            out.append((1, entry_tmp))
        else:
            out.append((1 - cnt / 10, entry_tmp))  # 保留原有的排序
    return out



def test_2():
    this_str = '国际海洋法法庭总部位于哪个国家？'
    out = query_whole_question_local(this_str)
    tmp_text = out[0][1].text
    print(tmp_text)
    tmp_text = re.sub(r'[\n\r\[\]-]+', "", tmp_text)
    with open('test_ltpcrash.txt', 'w', encoding='utf-8') as f:
        f.write(tmp_text)

if __name__ == '__main__':
    test_2()


