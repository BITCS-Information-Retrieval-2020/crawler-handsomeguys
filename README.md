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
