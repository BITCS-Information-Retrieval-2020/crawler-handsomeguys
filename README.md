# 爬虫模块

该项目为论文综合搜索引擎的爬虫模块，能够从网络上爬取到文献的元信息、pdf 文件、代码链接以及 oral 视频（如果存在的话），并将数据将存放于 MongoDB 和文件系统中。

## 项目成员

方致远，郑和奇，周啸峰，杨毅哲，刘啸尘，张骁，刘梦歌

## 数据库存储字段

每个网页爬取到的信息均存放于 MongoDB 中，一篇文献存储字段如下：

```json
{
  "_id": 1,
  "title": "...",
  "authors": "author1, author2, ...",
  "abstract": "...",
  "publicationOrg": "CVPR",
  "year": 2020,
  "pdfUrl": "...",
  "pdfPath": "./data/PDFs/xx.pdf",
  "publicationUrl": "https://...",
  "codeUrl": "...",
  "videoUrl": "...",
  "videoPath": "./data/videos/xx.mp4"
}
```

每个字段的含义如下：

- `_id` ：一个自动增长的编号，为了检索模块能够方便调用，这里设定从 1 开始自增长，无需手动设定
- `title`：文献的标题
- `authors`：作者的姓名，从相关网页中直接爬取后填入即可，无需对作者的序列做处理
- `abstract`：文献的摘要
- `publicationOrg`：出版组织，该值为文献投稿的期刊或会议名称
- `year`：文献出版的年份
- `pdfUrl`: pdf 文件的下载地址或 pdf 文件所在的网页（因为某些原因无法直接下载）
- `pdfPath`：pdf 文件下载后保存的路径，其中保存的位置`./data/PDFs/`请勿随意更改
- `publicationUrl`：pdf 文件所在的网页
- `codeUrl`：文献代码所在的地址
- `videoUrl`：视频在网络上的地址
- `videoPath`：视频下载后的保存路径，其中保存的位置`./data/videos/`请勿随意更改

以上字段的某些信息如果未能成功爬取，请设置为`""`

## 注意事项

1. pdf 文件一律存储在`./data/PDFs/`中，视频文件一律存储在`./data/videos/`中，并将这两个路径添加到`.gitignore`文件中
2. 请勿将任何二进制文件提交到 Github 仓库中（相应文件写入到`.gitignore`）
3. 测试代码文件和产生的中间结果请勿上传到 GitHub 仓库中（相应文件写入到`.gitignore`）
4. 为了避免潜在的冲突问题，在修改代码前，请先使用`git fetch origin`和`git merge`从远程仓库中拉取可能存在的更新 (推荐使用 vscode 或 pycharm 的图形界面)
5. 完成自己的模块之后，请自行使用 flake8 检测自己的代码风格是否符合规范

## 项目结构

```
crawler-handsomeguys
├─ .gitignore
├─ Crossminds
│    ├─ Crossminds
│    │    ├─ __init__.py
│    │    ├─ __pycache__
│    │    ├─ items.py
│    │    ├─ middlewares.py
│    │    ├─ pipelines.py
│    │    ├─ settings.py
│    │    └─ spiders
│    └─ scrapy.cfg
├─ Dblp
│    ├─ Dblp
│    │    ├─ __init__.py
│    │    ├─ items.py
│    │    ├─ middlewares.py
│    │    ├─ pipelines.py
│    │    ├─ settings.py
│    │    └─ spiders
│    └─ scrapy.cfg
├─ README.md
├─ crossminds.py
├─ handsomemongo.py
├─ main.py
├─ paperwithcode
│    ├─ config.json
│    └─ paperwithcode
│           ├─ __init__.py
│           ├─ items.py
│           ├─ middlewares.py
│           ├─ paperfromquery.py
│           ├─ pipelines.py
│           ├─ settings.py
│           ├─ spiders
│           └─ titlesearch.py
└─ utils.py
```

## 安装

### 环境要求

以下依赖是该模块运行所必须的：

- [Python](https://www.python.org/downloads/) 3.7 或更新版本
- [FFmpeg](https://github.com/FFmpeg/FFmpeg) 4.3.1 或更新版本
- [you-get](https://github.com/soimort/you-get) 0.4.1500 或更新版本
- [scrapy](https://github.com/scrapy/scrapy) 2.4.1 或更新版本
- [requests](https://github.com/psf/requests) 2.23 或更新版本
- [PyMongo](https://github.com/mongodb/mongo-python-driver) 3.11.2 或更新版本

### FFmpeg 安装

FFmpeg 是一个库和工具的集合，用于处理多媒体内容，如音频、视频、字幕和相关元数据。它可以使用 conda 进行快速安装：

```bash
conda install ffmpeg -c conda-forge -y
```

若您没有安装 Anaconda 环境，则可以通过 FFmpeg 官方提供的[下载页面](https://ffmpeg.org/download.html)下载对应的安装包进行安装。详情请见 [Wiki](https://trac.ffmpeg.org/)。

### you-get 安装

you-get 是一个小巧的命令行工具，用于从网上下载媒体内容（视频、音频、图片），它可以使用 pip 进行安装：

```bash
pip install you-get
```

### scrapy 安装

Scrapy 是一个快速的高级网络爬行和网络抓取框架，用于抓取网站并从其页面中提取结构化数据。它可通过 pip 进行安装：

```bash
pip install scrapy
```

也可以通过 conda 进行安装：

```bash
conda install scrapy -c conda-forge -y
```

### requests 安装

Requests 是一个简单而优雅的 HTTP 库，它可以通过 pip 进行安装：

```bash
python -m pip install requests
```

也可以通过 conda 进行安装：

```bash
conda install requests -c conda-forge -y
```

### PyMongo

PyMongo 允许用户使用 Python 与 MongoDB 数据库进行交互。它可以通过 pip 安装：

```bash
python -m pip install pymongo
```

也可以通过 conda 进行安装：

```bash
conda install -c conda-forge pymongo
```

### handsome-guys 爬虫模块安装

首先从将该仓库克隆到本地：

```bash
git clone https://github.com/BITCS-Information-Retrieval-2020/crawler-handsomeguys.git
```

然后进入到模块根目录

```bash
cd crawler-handsomeguys
```

运行`main.py`即可启动爬虫

```bash
python main.py
```

## 模块组成

本爬虫模块由三个爬虫组成，这三个爬虫能够分别爬取 CrossMinds、Papers with code 和 DBLP 三个网站的数据。

### CrossMinds

CrossMinds 爬虫基于 scrapy 框架进行开发，能够高效率的爬取 CrossMinds 网站上所有学术会议的 oral 视频地址，并从视频所处的网页中挖掘出论文标题、作者、论文 PDF 文件地址、代码地址等信息，并具有下载 PDF 文件的功能。

#### 工作流程

爬虫的工作模式如下：

1. 从`https://api.crossminds.io/content/category/parents/details`中获取到 CrossMinds 中可浏览的所有学术会议
2. 对第 1 步中获取到的每一个学术会议，向`https://api.crossminds.io/web/content/bycategory`发送 POST 请求，该 API 会返回一个 json 字符串，其中包含了该会议所有的 oral 视频信息。
3. 解析每个会议的 json 字符串，从中提取出论文标题、作者、视频链接、PDF 文件链接、代码链接、视频链接等内容，并使用正则表达式对这些数据做一些必要的处理，如格式化标题。
4. 通过 scrapy 的 pipeline 将第 3 步中爬取的数据存储到 MongoDB 数据库中
5. 若 PDF 链接存在，则通过 scrapy 的 FilesPipeline 下载 pdf 文件，存储路径为项目根目录下的 `data/PDFs`

视频的下载使用到了一些第三方工具。CrossMinds 中的视频主要由三个来源，分别为 CrossMinds 自身、Youtube 和 Videmo。不同来源对应的下载方式不同。

- CrossMinds 自身提供的视频为 `m3u8` 格式，因此这里使用 [FFmpeg](https://github.com/FFmpeg/FFmpeg) 进行下载
- Youtube 和 Videmo 上的视频使用 [you-get](https://github.com/soimort/you-get) 进行全自动的解析和下载

由于没有使用 scrapy 的 FilesPipeline 进行下载，为了不影响 scrapy 的性能，视频下载在 CrossMinds 爬虫运行完毕后执行。其工作模式如下：

1. 从 MongoDB 中读取所有的数据，获取其中的视频链接
2. 开启一个进程池，为多个进程并行下载视频做准备
3. 对于每一个视频链接，开启一个进程执行视频下载的函数，在函数中会根据视频的来源自动选择使用 [FFmpeg](https://github.com/FFmpeg/FFmpeg) 还是 [you-get](https://github.com/soimort/you-get) 进行下载。视频下载完成后会存储到项目根目录的 `data/videos` 中
4. 视频下载完毕后，将视频的存储路径更新到数据库中对应的位置

CrossMinds 爬虫的运行受 `main.py` 控制，也可使用如下代码单独运行 CrossMinds 爬虫而不进行视频下载：

```bash
cd Crossminds
scrapy crawl Crossminds
```

#### 小组分工

- 郑和奇：发现了 CrossMinds 网站的工作流程，制定处理标题的正则表达式。
- 方致远：实现从 CrossMinds 爬取数据并从中挖掘 PDF、代码链接以及下载 PDF 和视频的功能
- 周啸峰：编写基于校验值的校验方法，用于实现爬虫的增量更新

### Paper with code

Paper with code 爬虫基于 scrapy 框架进行开发，能够高效率的爬取 paperswithcode 网站上的论文资料，包含论文的标题、论文作者、论文摘要、论文年份、论文发表的会议（如果有的话）以及论文的代码（如果有的话）等信息，并具有下载 PDF 文件的功能。

#### 工作流程

爬虫的工作模式如下：

1. 从 paperswithcode 开放 api`https://paperswithcode.com/api/v1/papers/`中获取到 paperswithcode 中可浏览的所有论文列表（默认以 50 个论文为 1 页）
2. 对第 1 步中获取到的每一个论文列表页，获取每个论文的 id 信息，根据论文的 id 信息，向`papers/{paper_id}`发送 GET 请求，该 API 会返回一个 json 字符串，其中包含了该论文所有的信息，包括论文的标题、论文作者、论文摘要、论文年份、论文发表的会议（如果有的话），以及论文 PDF 文件的 URL 等
3. 同时，根据论文的 id 信息，向`papers/{paper_id}/repositories`发送 GET 请求，该 API 会返回一个 json 字符串，其中包含了该论文的代码信息，包括代码的 url、代码描述、用到的框架等。
4. 根据 3、4 步收集到的信息，将论文信息构建成 json 格式写入到 MongoDB 数据库中，并通过 Scrapy 封装的 Item 类和 Pipline 将论文 PDF 文件下载到本地
5. 为了能够实现增量爬虫，我们为采用配置文件保存的方式将已经爬取到的论文页的 page 进行保存，由于新增的论文会在新的论文页中保存，因此每次运行都会从保存的 page 开始爬取

papers with code 爬虫的运行受 `main.py` 控制，也可使用如下代码单独运行 paperswithcode 爬虫而不进行视频下载：

```bash
cd Paperwithcode
scrapy crawl paperswithcode
```

#### 接口设计

除了设计爬虫之外，本模块还提供了使用论文 title 在网页中进行检索的功能，便于在用户在数据库检索不到论文时即时在网站中进行检索。

工作模式：

1. 利用 paperswithcode 的搜索框，对于用户输入的论文标题，首先转化为 url 编码，再进一步处理成论文搜索结果页面的 url
2. 对论文搜索结果的页面进行解析，获取所有相关论文主页的 url，对每个 url 单独处理，获取每篇论文的主页内容
3. 对单篇论文主页的内容解析，根据是否包含出版方信息采取不同的解析策略，将论文信息保存为字典格式，多个相关的论文结果构成列表

调用方法示例：

```bash
title2content = Title2content()
results = title2content.search(title)
```

#### 小组分工

- 杨毅哲：paperswithcode 的 api 实验，爬虫模块的设计与实现
- 刘啸尘：主动检索接口的设计与实现

### DBLP

Dblp 爬虫基于 scrapy 框架进行开发，能够高效率的根据关键词检索爬取 Dblp 网站可检索到的学术论文信息，从网页提供的 json 格式 api 挖掘出
论文标题、作者、论文 PDF 文件地址等信息，并具有下载 PDF 文件的功能。

#### 工作流程

爬虫的工作模式如下：

1. 使用`https://dblp.uni-trier.de/search/publ/api?q=` 拼接 keyword 和检索参数构造 url。
2. 访问第一步构造的 url 得到检索的返回结果，解析 json 格式的结果，抽取出其中每一篇文献的具体信息：标题、作者、年分、pdf 来源连接、发表机构等。
3. 借助 pdf 来源连接访问原网页爬取对应 pdf，并储存在根目录下。
4. 保存爬取到的 item，储存到 mongoDB 中。
5. 从爬取到的文献中提取关键字词作为下一次检索的关键字词，重新构造 url 进行递归爬取。

Dblp 爬虫的运行受 `main.py` 控制，也可使用如下代码单独运行 Dblp 爬虫：

```bash
cd Dblp
scrapy crawl Dblp
```

#### 小组分工

- 张晓：搭建了 dblp 爬虫整体框架，实现了对 pdf 的抓取下载和 mongoDB 数据库存储；
- 刘梦歌：完成了对 json 文件的 item 解析和关键词递归爬取实现；

### 增量更新实现细节

增量更新的一个要点在于判断数据库是否已有相同的论文。结合论文实际情况，使用论文标题和作者姓名作为特征计算校验值，利用校验值进行判重。

为此，设置与论文 papers collection 相平行的校验值 checksum collection 用于存储校验值。checksum 对于下游的检索模块不是必需的，目前仅用于增量更新判重。

#### 工作流程

1. 计算校验值。为了既能有效区别出相似的论文，又避免条件过于严苛而使元数据略有不同的同一篇论文不同数据来源未被区分，结合论文实际情况，选择论文标题和作者作为判重使用的特征。论文的标题会被去除所有标点符号和潜在的多余空白字符。针对论文作者姓名，以`, `分割各个作者姓名。考虑到外国人名字中可能存在首字母简写或中间名，则以空格分割单人姓名后，取第一部分和最后一部分的首字母。以论文题目《handsomeFang》，作者 Zhiyuan Fang, John Smith 为例，最后用于计算校验值的特征为`handsomefang zf js`。针对得到的特征，计算其 Adler-32 校验值，得到的校验值为 32 bit 的整数。同时，论文的原标题和作者也会被与校验值一同记录，以备后续需求。
2. 插入数据。针对给定的待插入文档，计算其校验值。先将校验值作为主键`_id`插入到 checksum collection 中。若发现已有重复的校验值，则不再继续插入真实的论文数据；反之则存储真实的论文数据。
3. 删除数据。首先根据删除的条件查询待删除的论文数据。然后计算待删除论文数据的校验值，从 checksum collection 中删去校验值后再正式删除论文数据。若没又符合要求的待删除论文，则不进行任何操作，并通知调用者。
4. 查询数据。查询与判重无直接关系，直接复用 pymongo 已有的查询功能。
