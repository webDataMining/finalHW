# 智能问答系统说明文档

## 作者信息

* 范志康：1300012971，信科微电子系
* 王鹏飞：1300013007，信科电子系
* 温凯：1300063704，心理与认知科学学院
* 曾繁辉：1300062702，信科电子系

## 分工情况

* 范志康：配置服务器及API编写、部署，配置封闭测试搜索引擎，开放测试爬虫开发、信息预处理
* 王鹏飞：维基百科的infobox提取和处理，根据问题和infobox中键值key得匹配程度返回置信度高的推荐答案（基于范志康和温凯给出的部分结果，代码在entry_matching文件夹中）
* 温凯：句子评分及排序，基于TrieTree的维基百科查询词匹配
* 曾繁辉：问题分类，封闭测试答案提取，开放测试答案提取（基于范志康给出的部分结果）
## 编译 & 运行环境

* 问题分类：Java，Win 10
* solr搜索引擎及API：Apache 2.4.6，PHP 5.6.22，CentOS 阿里云服务器
* 开放测试信息处理：Objective-C，Xcode 8.2.1，macOS
* 封闭测试信息处理，结果抽取：Python 3/ Java，Win 10/ macOS

## 系统架构 & 关键技术

* 整个系统包括问句分析、信息检索、句子打分、答案抽取四个主模块。
* 使用[solr](http://lucene.apache.org/solr/)作为封闭测试维基数据的搜索引擎和数据源
* 使用PHP编写爬虫作为开放测试的数据源
* 为了方便协同开发，使用PHP编写了一个API（封闭测试和开放测试均使用此API进行查询），API部署于[search.fanzhikang.cn/api/](http://search.fanzhikang.cn/api/)，API程序和文档在压缩包中`search`文件夹，也可见[GitHub](https://github.com/webDataMining/server)
 * `range=local`时仅使用solr系统返回的数据（来自课程提供的维基百科XML），即封闭测试
 * `range=online`时使用爬虫返回的数据，即开放测试
* 在查询词抽取中，使用了基于TrieTree的正向最大匹配算法，解决了维基百科词条较多（上百万）所带来的效率问题
* 在句子排序中，使用支持python的[pyltp](pyltp.readthedocs.io/zh_CN/latest/)作为分句、分词、词性标注、句法分析、命名实体识别的工具包。通过1-gram，基于命名实体的1-gram，依存句法相似度，问句答案类型相似度来对句子进行打分。
* 在答案抽取中，使用基于Java的[HanLP](http://hanlp.linrunsoft.com/)作为分词、句法分析、命名实体识别的工具包。
* 利用Python对API返回的json形式的数据进行处理，提取出其中的infobox信息并进行处理，通过对焦点词汇的字符串匹配和词义匹配，对查询问题和返回答案的相似度进行排序，返回置信度高的infobox中的内容
 
## 使用的方法 & 资源

 * 根据训练集和测试集的分类情况，针对特定类别写模板。主要包括年份、人名、地名、国家、时间等。
 * 对于无法分类的问题，使用句法依存关系，先找出核心成分，再根据主谓、动宾、介宾、间宾等关系提取主语和宾语，在候选句子中进行检索。
 
### 封闭测试部分

#### 问题分类：

根据对问题训练集和测试集的统计，发现一些特此那个类型的问题出现频率高，包括：

 * 人名
 * 地名
 * 日期
 * 地点
 * 国家
 * 城市
 * 省份
 * 数量
 * 朝代
 * ……

这些问题占所有问题的比例可以达到40%以上。对于这些问题寻求高可靠性的模板，可以有效提高系统性能。
另外，由于维基百科的预料的局限性，一些类别的问题在封闭集上得到正确答案的可能性极低，例如：

 * “下一句”问题
 * 涉及媒体（歌曲、书等）原文的问题
 * ……
 
对于这些问题，在封闭测试中考虑的意义不大，所以在问题分类中也将其单独考虑。具体
具体涉及的部分代码为：

```java
    /*******问题分类********/
    public static String query_classifier(String query){
    	if(query.matches(".*谁.*")||query.matches(".*的人叫.*")||query.matches(".*的人是.*")||query.matches(".*名字.*")||query.matches(".*哪位.*")||query.matches(".*什么人.*")){
    		return "Name";
    	}
    	if(query.matches(".*首都.*")){
    		return "Capital";
    	}
    	if(query.matches(".*什么颜色.*")||query.matches(".*颜色是什么.*")||query.matches(".*哪种颜色.*")){
    		return "Color";
    	}
    	if(query.matches(".*哪里.*")||query.matches(".*哪儿.*")||query.matches(".*什么地方.*")){
    		return "Location";
    	} 	    	
    	if(query.matches(".*下一句.*")){
    		return "Next_Sentence";
    	}
    	if(query.matches(".*朝代.*")){
    		return "Dynasty";
    	}
    	if(query.matches(".*哪年.*")||query.matches(".*哪一年.*")){
    		return "Year_Number";
    	}
    	if(query.matches(".*多少年.*")||query.matches(".*几年.*")){
    		return "Year_Count";
    	}
    	if(query.matches(".*几月几号.*")||query.matches(".*几月几日.*")){
    		return "Month_Day";
    	}    
    	if(query.matches(".*哪个月.*")||query.matches(".*几月.*")){
    		return "Month";
    	}    	
    	if(query.matches(".*几号.*")||query.matches(".*几日.*")||query.matches(".*哪天.*")||query.matches(".*哪一天.*")){
    		return "Day";
    	}
    	if(query.matches(".*什么时间.*")||query.matches(".*什么时候.*")||query.matches(".*何时.*")||query.matches(".*多少时间.*")||query.matches(".*多长时间.*")||query.matches(".*时间是.*")){
    		return "Time";
    	} 	
    	if(query.matches(".*哪国.*")||query.matches(".*哪.*个国家.*")||query.matches(".*哪个.*国家.*")||query.matches(".*国籍.*")){
    		return "Country";
    	}
    	if(query.matches(".*哪个省.*")||query.matches(".*省份.*")){
    		return "Province";
    	}
    	if(query.matches(".*哪.*个.*城市.*")||query.matches(".*哪个市.*")||query.matches(".*哪.*座城市.*")){
    		return "City";
    	}
    	if(query.matches(".*几.*")||query.matches(".*多少.*")){
    		return "Count";
    	}    	
    	return "Unknown";
    }
```

 
#### 词条索引：

使用了solr搜索引擎，配置在阿里云服务器上，查询官方文档，构造XML导入数据：

```xml
<dataConfig>
        <dataSource type="FileDataSource" encoding="UTF-8" />
        <document>
        <entity name="page"
                processor="XPathEntityProcessor"
                stream="true"
                forEach="/mediawiki/page/"
                url="/var/www/html/solr/data/zhwiki-20161101-pages-articles-multistream-simplified.xml"
                transformer="RegexTransformer,DateFormatTransformer"
                >
            <field column="id"        xpath="/mediawiki/page/id" />
            <field column="title"     xpath="/mediawiki/page/title" />
            <field column="revision"  xpath="/mediawiki/page/revision/id" />
            <field column="user"      xpath="/mediawiki/page/revision/contributor/username" />
            <field column="userId"    xpath="/mediawiki/page/revision/contributor/id" />
            <field column="text"      xpath="/mediawiki/page/revision/text" />
            <field column="timestamp" xpath="/mediawiki/page/revision/timestamp" dateTimeFormat="yyyy-MM-dd'T'hh:mm:ss'Z'" />
            <field column="$skipDoc"  regex=".*?\{\{简繁重定向\}\}$" replaceWith="true" sourceColName="text"/>
        </entity>
        </document>
</dataConfig>
```

并配置schema，关键部分是加载并且配置中文分词器`SmartChineseAnalyzer`，下面节选`schema.xml`部分关键代码：

```xml
<schema name="wiki" version="1.6">
	......
    <field name="id"        type="string"  indexed="true" stored="true" required="true"/>
    <field name="title"     type="string"  indexed="true" stored="false"/>
    <field name="revision"  type="int"    indexed="true" stored="true"/>
    <field name="user"      type="string"  indexed="true" stored="true"/>
    <field name="userId"    type="int"     indexed="true" stored="true"/>
    <field name="text"      type="text_cn"    indexed="true" stored="true"/>
    <field name="timestamp" type="date"    indexed="true" stored="true"/>
    <field name="titleText" type="text_cn"    indexed="true" stored="true"/>
    <uniqueKey>id</uniqueKey>
    <copyField source="title" dest="titleText"/>
    ......
    <dynamicField name="*_txt_cn" type="text_cn"  indexed="true"  stored="true"/>
    <fieldType name="text_cn" class="solr.TextField">
      <analyzer class="org.apache.lucene.analysis.cn.smart.SmartChineseAnalyzer" />
    </fieldType>
</schema>
```

完整的一次导入在服务器（CPU：1核，内存：1024 MB）上大约需要8小时，其中有两点需要特殊处理：

* 导入之前将所有文本通过OpenCC转换为简体中文，消除简繁体共存带来的问题
* 因为经过了简繁体转换，因此维基百科中“简繁重定向”词条无需保留，导入过程中抛弃

配置好后的solr服务器运行于[search.fanzhikang.cn](http://search.fanzhikang.cn)，其名为“wiki”的核就是本次试验所使用的核（注意：请勿任意操作，该页面具有操作solr系统的所有权限）。三个需要更改的配置文件`import-wiki-data.xml`，`schema.xml`，`solrconfig.xml`见压缩包`solr`文件夹

使用的第三方库：

* [OpenCC](https://github.com/BYVoid/OpenCC)：用于原始文档简繁体转换


#### 词条查询

尽管solr本身提供了查询的http接口，但是为了方便查询以及清洗掉维基百科的一些特殊格式，我们使用PHP封装了一个更高层次的API。查询时，直接将整个问题作为查询词在solr中查询，我们在建立索引时就已经进行了中文分词，所以直接查询问题也能取得不错的效果。而在进行infobox的检索时，则使用基于TrieTree的最大正向匹配抽取维基词条名，再进行查询。

使用的第三方库：

* [PHP-Wikipedia-Syntax-Parser](https://github.com/donwilson/PHP-Wikipedia-Syntax-Parser)：用于PHP解析wiki正文格式，抽取infobox等
* [requests](http://docs.python-requests.org/en/master/)：用于在Python中调用维基百科查询API并对返回的json数据进行解析。

#### infobox提取与处理
对得到的问题及关键词汇txt文本进行处理，提取出关键词信息，并得到所有关键词对的排列，两个关键词分别作为维基百科查询词search和infobox匹配词obj（参见**loadFocusWord.py**文件）

针对每个问题，依据词条title和查询词的相关程度得到对应text的相关度p1，依据从高到低的相关度在text里面寻找含有infobox的“meta_boxes”模块，总共提取最多3个infobox，找到之后进行infobox的处理

infobox的处理：

* 先进行一轮字符串匹配（中英文同时进行），如果匹配上了，那就直接返回结果，同时infobox置信度p2为1，跳过以后的步骤

* 当第一轮字符串匹配失败时，进行第二轮词义匹配，将infobox里的k-v对中所有的key（去除下划线）值翻译成中文（借助百度翻译的API接口，参见**english_translation.py**，关键代码如下）
```python
appid = '20151113000005349'
secretKey = 'osubCEzlGjzvw8qdQc41'
httpClient = None
myurl = '/api/trans/vip/translate'
q = words
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)
sign = appid+q+str(salt)+secretKey
m1 = hashlib.md5()
m1.update(sign.encode("utf8"))
sign = m1.hexdigest()
myurl=myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
	 
try:
    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)
    #response是HTTPResponse对象
    response = httpClient.getresponse()
    result = eval(response.read().decode())
    return(result["trans_result"][0]['dst'])
```
* 针对每一个处理过的key值，将key与目标词汇进行词义匹配，计算余弦相似度(作为置信度p2)，并将英文key和相似度以字典方式存入vec_cos中（词义向量的导入参见**loadWordVector.py**，其中用到了[中文词义向量库 word_vectors_20161214.dump](https://pan.baidu.com/s/1hrNcmI4)），词义相似度的计算如下
```python
nfo_key_array = np.array(info_key_vec[k]) 
info_key_len = np.sqrt(info_key_array.dot(info_key_array)) #infobox的key的词义向量的模长
cos_angel = obj_array.dot(info_key_array)/(obj_len*info_key_len) #计算两个向量的夹角余弦
vec_cos[k] = cos_angel #将计算得到的余弦相似度连同infobox的条目加入字典
```
* 对vec_cos依据value进行排序，将前五个词条作为这个infobox的推荐答案recommend，置信度为p1*p2

对infobox处理返回的推荐结果依据置信度p1p2进行排序，按置信度从高到低写入文件**result.txt**中，同时筛选出同一词条中置信度前五的答案作为推荐答案，写入文件**result_recommend.txt**中

#### 句子打分(开放测试使用同样的算法)

在对句子进行打分之前，首先对问题进行处理，缺少疑问代词的，补上疑问代词，缺少问号的，补上问号，从而使问题具备较为规整的形式。

按照solr返回结果的顺序，取前N_solr（默认为5）条维基词条进入句子排序阶段，每个词条的权重依次为1，0.9，0.8，0.7，0.6（在在线问答中，每个词条的权重则依次为1, 0.99, 0.98 …）。如果维基词条的词条名在问句中，则该词条的权重会被置为1。

然后对每个词条中所有的句子进行评分，句子的评分为以下4项的和：

##### 1. 句子与问题的n-gram相似度  autoQA.utility.oneGramSimScore()

对问题进行分词，得到词语的集合Qset，维基百科中词条的句子也进行分词，得到词语的集合Sset，然后返回共有词语个数/总词语个数作为1-gram相似度的得分。

##### 2. 句子与问题的命名实体相似度 autoQA.utility.entitySimScore()

类似于上面的1-gram相似度，抽取出问题中的命名实体及其类别，得到集合Qset_entity，同样，抽取出句子中的命名实体及其类别，得到集合Sset_entity，返回共有实体/总实体个数作为命名实体相似度得分。

之所以要将命名实体相似度得分单独列出，主要是为了突出其在问句中的重要地位，因为问题一般来说是针对某个实体的某种属性的，这就使得实体在问句和答案中都具有指明方向的地位。

##### 3. 句子与问题的依存语法相似度 autoQA.utility.flat\_grammar\_dependency\_sim\_score\_ver2()

为了利用句子更深层次的信息对答案进行匹配，在答案句子评分中还使用了依存句法分析的结果，计算的方法参考了文章“基于语义依存关系匹配的汉语句子相似度计算”，具体如下：

依存句法分析可以得到多种词语之间的相互关系，但不少关系对句子的理解作用不大。参照上述文献，使用表示句子总体框架的主谓关系(SBV)、动宾关系(VOB)、介宾关系(POB)，以及 表示修饰关系的并列关系(COO)、定中关系(ATT) 、同位关系(APP）这六种语义关系用于计算依存句法的相似度。

语义依存关系R(w1, w2, T)包括三个元素：词语1 （w1），词语2（w2），依存关系类型（T），实际计算中采取了较为简单的方法，即，比较问句和答案句中所有的依存关系，如果发现三元素完全匹配的依存关系，则相似度得分提高1。最后将相似度得分除以句子中依存关系的数目作为归一化之后的得分。这一得分表示，答案句中有多少依存关系和问句中匹配，从而可以较好地反映答案句与问句的匹配程度。此外，考虑到问句中含有疑问词，在比较依存关系时，疑问词可以和任意词匹配。

为了避免问句形式对语义依存分析的影响，对大部分含有“是”的问题，如“世界第一高峰是我国的什么山峰”，还会生成“我国的什么山峰是世界第一高峰”，对于一个候选句子，可以分别计算与这两个句子的依存语法相似度，取其中较高的作为该句子的依存语法相似度得分。

##### 4. 句子中是否含有问题中所需的实体或词语类型 autoQA.utility.contains\_question\_answer\_type\_sim\_score()

通过一些规则对问句的答案类型进行推断（代码见autoQA.questionAnalysis.infer\_question\_answer\_type()），如，含有疑问代词“谁”的问句，其答案句中应该有人名，含有疑问代词“哪里”的问句，其答案句中应该有地名。如果候选句子中含有相应类型的实体或名词，则会对应地得到0.5 / 0.25的相似性得分。

##### 总得分的计算及句子抽取

对每个词条，将其分句后，对每个句子计算上述四种相似度得分的和，作为该句子的相似度得分sim\_sentence，然后将N\_solr个词条中的每个句子的sim\_sentence乘以前文中提到的权重，得到每个句子最终的得分sim\_sentence\_overall，再依sim\_sentence\_overall将所有句子进行排序，取出排名前五的句子，送入答案抽取阶段。

为封闭测试抽取的句子在autoQA/z\_full\_questions\_recommend\_sentences\_ver3\_part{1,2,3}.txt中
为开放测试抽取的句子在autoQA/online\_questions\_recommend\_sentences.zip中




### 开放测试部分

爬取的数据主要来自以下四个渠道，（谷歌由于服务器访问受限所以没有使用）

* 百度搜索：用于尝试提取最佳答案
* 百度知道：用于返回答案语料
* 搜狗搜索：用于尝试提取最佳答案以及返回答案语料
* bing搜索：用于尝试提取最佳答案以及返回答案语料

#### 尝试提取最佳答案

对于某些特定问题，搜索引擎会直接返回最佳答案或观点作为醒目推荐，这种情况下通过提取特定HTML元素中的内容，可以直接返回，并且将其作为最终答案。下面给出几个例子：

* 百度搜索：[儿童节在哪一天](https://www.baidu.com/s?wd=儿童节在哪天)，[世界上最高的山是什么](https://www.baidu.com/s?wd=世界上最高的山是什么)，[北京大学的邮编是多少](https://www.baidu.com/s?wd=北京大学的邮编是多少)
* 搜狗搜索：[奥巴马是哪国人](https://www.sogou.com/web?query=奥巴马是哪国人)，[苹果公司的客服电话是什么](https://www.sogou.com/web?query=苹果公司的客服电话是什么)，[冬泳下水之前饮用白酒可以御寒吗](https://www.sogou.com/web?query=冬泳下水之前饮用白酒可以御寒吗)
* bing搜索：[意大利的官方语言](http://cn.bing.com/search?q=意大利的官方语言)，[北京大学的地址在哪里](http://cn.bing.com/search?q=北京大学的地址在哪里)，[10的平方是多少](http://cn.bing.com/search?q=10的平方是多少)

其中需要特别注意的是，搜狗有一个“立知”系统（[参考此新闻报道](http://news.163.com/16/1111/16/C5JR8HCD00014AEE.html)），其直接返回推荐答案的频率和效果都是最好的，但是经过大量的测试发现，有些“立知”返回的答案，其在网页上并不可见，但是源代码中是存在的。可能是搜狗认为这些答案置信度不够高因此将其隐藏，但经过测试比对，它们仍然有相当高的正确率，因此这些答案也被采用

* 例如，使用搜狗搜索[哪个海峡沟通了北冰洋与太平洋](https://www.sogou.com/web?query=哪个海峡沟通了北冰洋与太平洋)时，有时候其结果并不会显示出来，但是查看网页源代码会发现有一个`class=txt-box`的`div`元素，其CSS属性为`display:none`，但是其中的内容正是该问题的正确答案“白令海峡”

#### 返回答案语料

除了尝试提取最佳答案外，根据搜索引擎返回的每条信息，提取其中的文本，作为语料交给下一步处理

使用的第三方库：

* [Simple HTML Dom](http://simplehtmldom.sourceforge.net)：用于PHP爬虫快捷操作HTML元素

#### 开放测试批量查询和预处理

使用了一个Objective-C工程，将问题批量查询API并储存结果。项目代码见压缩包`OnlineQA`文件夹，抽取的结果见`OnlineQA/OnlineQA/data`文件夹。在这个过程中做适量的预处理，一是尝试更换问法直接抽取正确答案，二是为后面的结果提取减轻压力：

* 对于特定形式的问题，有的时候过于复杂的问句搜索引擎无法直接返回推荐答案，而如果适当简化则可以。例如百度搜索[李商隐的诗《锦瑟》中“庄生晓梦迷蝴蝶”的下一句是什么](https://www.baidu.com/s?wd=李商隐的诗《锦瑟》中“庄生晓梦迷蝴蝶”的下一句是什么)，但是将问题简化为[“庄生晓梦迷蝴蝶”的下一句是什么](https://www.baidu.com/s?wd=“庄生晓梦迷蝴蝶”的下一句是什么)就可以直接得到答案。因此对于一次查询未得到推荐答案的问题，做适量正则处理再次查询，尝试得到推荐答案。部分规则如下：

```objc
".*?“(.*?)”.*?((下|上|前|后)(一|两|半)?句)" => "$1 的$2",
".*?《(.|[^《]*?)》(是|出自).*?的.*?(歌|曲).*" => "“$1” 是谁唱的",
```

* 对于返回的结果，我们发现有许多问题来自于《一站到底》节目题库，返回的结果也都是与《一站到底》相关的信息。对于这些信息，尝试使用正则直接提取出正确答案
* 运行工程的过程中还遇到了一个问题，就是搜狗搜索对IP的访问频率有限制，超过一定频率则IP会被封禁1~2小时不等。因此设置了每次查询后线程随机休眠一段时间的解决方案，以及多部署几套API于不同IP，发现被封后轮流切换
* 预处理最终结果（见`OnlineQA/OnlineQA/data/answers-final.html`，标绿的为已知答案）：搜索引擎推荐答案：1163个，一站到底题库确信匹配：2910个




## 参考文献

* [solr官方文档](https://wiki.apache.org/solr)
* [HanLP官方文档](http://hanlp.linrunsoft.com/doc/_build/html/index.html)
* [汪卫明, 梁东莺. 基于语义依存关系匹配的汉语句子相似度计算[J]. 深圳信息职业技术学院学报, 2014, 12(1):56-61.](http://mall.cnki.net/magazine/article/SZXZ201401012.htm)
* [百度翻译API使用说明文档](http://api.fanyi.baidu.com/api/trans/product/apidoc)
* [中文词义向量库 word_vectors_20161214.dump](http://pan.baidu.com/s/1hrNcmI4)
