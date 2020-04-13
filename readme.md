# Chinese Language Processor
Current version: **v1.4.0**  
Developed by **Sulley**

## 程序简介
- 支持笔画<->汉字<->编码的转换，并标出单个汉字的读音
- 支持把word/txt文件转换为utf8编码的txt文件 
- 支持统计汉字字频，并按照一定标准排序
- 支持统计文件内的各类（汉字字符、英文字符、标点符号、其他字符）字符数量，并写入单个log文件
- 支持提取中文词表并排序
- 支持打开并管理、检索语料库
- 支持打开并管理、检索词库

## 安装方法

- 本程序基于python实现，直接在命令行输入python main.py稍等即可

- 为了确保程序能够正确进行，请首先在运行之前在命令行输入以下命令：

```shell
pip install --upgrade pip # 更新pip
pip install xlrd pypinyin chardet docx pyqt5 jieba lxml nltk# 安装依赖包

git clone https://github.com/littlesulley/language_project_and_chinese_information_processing 
python main.py # 运行
```

## 使用说明
本项目主要实现如下功能：（1）文件编码转换；（2）汉字编码转换；（3）文件分词及统计；（4）语料库功能；（5）语料库功能；（6）语法分析。各功能介绍及使用说明如下：
- 文件编码功能实现了将文件夹下的所有.txt和.docx文件转换为.txt文件，并且统一编码为utf8。点击第一个菜单“文件”，选择“编码转换”，打开需要转换编码的文件夹即可。注意，本功能只支持打开文件夹而非文件，编码转换结束后会按照**源文件夹的层次结构**将转换后的文件存放到目标文件夹中
- 汉字编码转换实现了给定汉字，输出汉字的各编码、笔画和拼音的功能；同时也支持将编码转换为汉字；支持输入笔画数，输出所有可能的汉字。点击“汉字”菜单选择想要的功能即可
- 文件分词及统计功能完成了下述功能：对文件夹下所有文件分词（请保证**所有文件**均为未分词文件）；对文件夹下**所有文件**统计字符（或词）级别信息，包括频次、编码、拼音、笔画，并对每个文件输出一个.csv文件，若是词级别信息，请保证**所有文件**均已分词；对得到的单个.csv文件排序，排序标准有按频次、按编码、按拼音、按笔画，输出一个排序的.csv文件。点击“统计”菜单选择想要的功能
- 语料库功能包括：打开语料库（暂不支持新建），查看语料库中的每篇语料并显示基本信息，展示每篇语料的用字情况并按照音序和字频序呈现，删除语料与添加语料
- 词库功能包括：打开并显示词库，添加、删除词条，词条检索

## 程序说明
**[utils.py](./utils.py)**
- 定义类`Converter`，用于汉字、编码和笔画之间的转换
- 定义类`Counter`，抽取汉字的频度信息并按照频度、编码、拼音或笔画排序
- 定义类`Extractor`，用于中文分词（暂时使用[jieba](https://github.com/fxsjy/jieba)分词包，之后可能会自己实现多种分词实现方法）
- 定义类`Corpus`，用于语料库的基本管理功能
- 定义类`Lexicon`，用于实现词库的基本功能

**[window.py](./window.py)**
- 定义类`Windows.py`，实现交互界面

**[main.py](./main.py)**
- 用户运行文件

## TODO
- 实现等待进度条
- 优化程序执行时间
- 优化代码结构，减少冗余量

## 更新日志
**v1.4.0**
本版本主要是对语料库进行了较多的更新：
- 对XML文档各种编码的支持（包括GBK字符集、Unicode、UTF-8字符集）
- 串频统计（N-gram），用户可指定N的范围，按照字母序和频次序排序
- 不连续关键字检索功能
- 在线编辑功能

**v1.3.0**
- 实现基本语料库功能
- 新增词库功能

**v1.2.0**
- 优化了主界面
- 优化了代码结构
- 增加了语料库功能

**v1.1.0**  
- 实现了字符频度统计功能
- 实现词表提取，并支持按照频度序、内码旭和音序排序输出

**v1.0.0**  
- 实现了笔画<->汉字<->编码的转换，支持标出单个汉字的读音（包括多音字）
- 支持把word/txt文件转换为utf8编码的txt文件 
- 使用pyqt实现了交互式界面