#infobox的提取与处理
*作者：王鹏飞*


----------


>  此部分实现的功能主要是利用Python对API返回的json形式的数据进行处理，提取出其中的infobox信息并进行处理，通过对焦点词汇的字符串匹配和词义匹配，对查询问题和返回答案的相似度进行排序，返回置信度高的infobox中的内容
>  其中用到了[中文词义向量库 word_vectors_20161214.dump](http://pan.baidu.com/s/1hrNcmI4)

开发环境：Python3.5.1 + requests

文件说明：

 - **matching_main.py**： 程序的核心代码，用于串联各个代码文件，并实现主要逻辑
 - **loadFocusWord.py**： 负责从 z_full_questions_wikipedia_title_match.txt 文件导入之前处理过的问题关键词，并得到查询词-匹配焦点词对
 - **infobox_pro.py**： 负责从之前的API中返回的数据中提取出的 infobox 进行处理，包括焦点词的匹配、答案置信度的计算、返回答案的排序，产生最终的推荐答案
 - **english_translation.py**： 负责调用百度翻译的 API 进行英文关键词的翻译
 - **loadWordVector.py**： 导入词义向量库，提供词义向量查询功能函数
 - **question_wikipedia_query_word.txt**： 训练集问题及关键词
 - **result_test.txt**： 训练集返回结果
 - **z_full_questions_wikipedia_title_match.txt**： 测试集问题及关键词
 - **result.txt**： 测试集返回查询结果
 - **result_recommend.txt**： 测试集返回的推荐答案列表

