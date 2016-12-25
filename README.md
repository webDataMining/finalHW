# 智能问答系统说明文档

## 作者信息

* 范志康：1300012971，信科微电子系
* 王鹏飞：1300013007，信科电子系
* 温凯：1300063704，心理学系
* 曾繁辉：1300062702，信科电子系

## 分工情况

* 范志康：配置服务器及API编写、部署，配置封闭测试搜索引擎，开放测试爬虫开发、信息预处理
* 王鹏飞：维基百科的infobox提取和处理，根据问题和infobox中键值key得匹配程度返回置信度高的推荐答案
* 温凯：
* 曾繁辉：

## 编译 & 运行环境

* solr搜索引擎及API：Apache 2.4.6，PHP 5.6.22，CentOS 阿里云服务器
* 开放测试信息处理：Objective-C，Xcode 8.2.1，macOS
* 封闭测试信息处理，结果抽取：Python 3，Win 10/ macOS

## 系统架构 & 关键技术

* 使用[solr](http://lucene.apache.org/solr/)作为封闭测试维基数据的搜索引擎和数据源
* 使用PHP编写爬虫作为开放测试的数据源
* 为了方便协同开发，使用PHP编写了一个API（封闭测试和开放测试均使用此API进行查询），API部署于[search.fanzhikang.cn/api/](http://search.fanzhikang.cn/api/)，API程序和文档在压缩包中`search`文件夹，也可见[GitHub](https://github.com/webDataMining/server)
 * `range=local`时仅使用solr系统返回的数据（来自课程提供的维基百科XML），即封闭测试
 * `range=online`时使用爬虫返回的数据，即开放测试
* 利用Python对API返回的json形式的数据进行处理，提取出其中的infobox信息并进行处理，通过对焦点词汇的字符串匹配和词义匹配，对查询问题和返回答案的相似度进行排序，返回置信度高的infobox中的内容

## 使用的方法 & 资源

### 封闭测试部分

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

尽管solr本身提供了查询的http接口，但是为了方便查询以及清洗掉维基百科的一些特殊格式，我们使用PHP封装了一个更高层次的API

使用的第三方库：

* [PHP-Wikipedia-Syntax-Parser](https://github.com/donwilson/PHP-Wikipedia-Syntax-Parser)：用于PHP解析wiki正文格式，抽取infobox等

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
* 针对每一个处理过的key值，将key与目标词汇进行词义匹配，计算余弦相似度(作为置信度p2)，并将英文key和相似度以字典方式存入vec_cos中（词义向量的导入参见**loadWordVector.py**），词义相似度的计算如下
```python
nfo_key_array = np.array(info_key_vec[k]) 
info_key_len = np.sqrt(info_key_array.dot(info_key_array)) #infobox的key的词义向量的模长
cos_angel = obj_array.dot(info_key_array)/(obj_len*info_key_len) #计算两个向量的夹角余弦
vec_cos[k] = cos_angel #将计算得到的余弦相似度连同infobox的条目加入字典
```
* 对vec_cos依据value进行排序，将前五个词条作为这个infobox的推荐答案recommend，置信度为p1*p2

对infobox处理返回的推荐结果依据置信度p1*p2进行排序，按置信度从高到低写入文件**result.txt**中，同时筛选出同一词条中置信度前五的答案作为推荐答案，写入文件**result_recommend.txt**中

  
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
* [百度翻译API使用说明文档](http://api.fanyi.baidu.com/api/trans/product/apidoc)
