# 句子抽取及排序

开发环境：Python 3.5.1 + Anaconda 2.4.1 + pyltp 3.3.1 + requests

文件说明：
* `playground7_process_all_questions.py`    处理所有封闭问题的脚本，将推荐句子及其相似度得分保存到文件中。
* `playground015_online_all_questions_recommend_sentence.py`   处理所有开放问题的脚本，将推荐句子及其相似度得分保存到文件中。
* `assessSentenceRank.py`  评估句子评分机制在样例数据上的表现
* `cleanTitles.py`   清洗维基百科的词条名
* `commonVar.py`  包括疑问代词和名词pos_tag两个通用变量
* `environmentVar.py`  pyltp及查询API的路径配置
* `getTitlesFromWikiDB.py`  从维基百科中提取词条名以建立词典
* `initializeLTP.py`  初始化pyltp
* `playgroundXXX.py`  在处理数据时使用的一些脚本
* `Question.py`  问题类，用于建立表示问题的示例。
* `questionAnalysis.py`  分析问题的一些函数。包括问题形式补全，问题答案类型推断等。
* `search_api.py`  查询solr搜索
* `Sentence.py` 表示一个句子的类。根据ltp的分析对句子进行处理，可以提取句子主干，分析关系等。
* `Word.py`  表示一个词的类
* `workflow.py`  处理一个问题的流程



