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
- 周啸峰：编写基于哈希的校验方法，用于实现爬虫的增量更新

### Paper with code

Paper with code 爬虫基于 scrapy 框架进行开发，能够高效率的爬取 paperswithcode网站上的论文资料，包含论文的标题、论文作者、论文摘要、论文年份、论文发表的会议（如果有的话）以及论文的代码（如果有的话）等信息，并具有下载 PDF 文件的功能。

#### 工作流程

爬虫的工作模式如下：

1. 从paperswithcode开放api`https://paperswithcode.com/api/v1/papers/`中获取到 paperswithcode中可浏览的所有论文列表（默认以50个论文为1页）
2. 对第 1 步中获取到的每一个论文列表页，获取每个论文的id信息，根据论文的id信息，向`papers/{paper_id}`发送 GET 请求，该 API 会返回一个 json 字符串，其中包含了该论文所有的信息，包括论文的标题、论文作者、论文摘要、论文年份、论文发表的会议（如果有的话），以及论文PDF文件的URL等
3. 同时，根据论文的id信息，向`papers/{paper_id}/repositories`发送 GET 请求，该 API 会返回一个 json 字符串，其中包含了该论文的代码信息，包括代码的url、代码描述、用到的框架等。
4. 根据3、4步收集到的信息，将论文信息构建成json格式写入到MongoDB数据库中，并通过Scrapy封装的Item类和Pipline将论文PDF文件下载到本地
5. 为了能够实现增量爬虫，我们为采用配置文件保存的方式将已经爬取到的论文页的page进行保存，由于新增的论文会在新的论文页中保存，因此每次运行都会从保存的page开始爬取

papers with code爬虫的运行受 `main.py` 控制，也可使用如下代码单独运行 paperswithcode爬虫而不进行视频下载：

```bash
cd Paperwithcode
scrapy crawl paperswithcode
```

#### 接口设计

除了设计爬虫之外，本模块还提供了实用论文title在网页中进行检索的功能，便于在用户在数据库检索不到论文时即使在网站中进行检索。

#### 小组分工

- 杨毅哲：paperswithcode的api实验，爬虫模块的设计与实现
- 刘啸尘：主动检索接口的设计与实现

### DBLP

待填写
