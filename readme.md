# Chinese Language Processor
Current version: **v1.2.0**  
Developed by **Sulley**

## 程序简介
- 支持笔画<->汉字<->编码的转换，并标出单个汉字的读音
- 支持把word/txt文件转换为utf8编码的txt文件 
- 支持统计汉字字频，并按照一定标准排序
- 支持统计文件内的各类（汉字字符、英文字符、标点符号、其他字符）字符数量，并写入单个log文件
- 支持提取中文词表并排序

## 使用方法

- 本程序基于python实现，直接在命令行输入python main.py稍等即可

- 为了确保程序能够正确进行，请首先在运行之前在命令行输入以下命令：

```shell
pip install --upgrade pip # 更新pip
pip install xlrd pypinyin chardet docx pyqt5 jieba # 安装依赖包
```

## 程序说明
**[utils.py](./utils.py)**
- 定义类`Converter`，用于汉字、编码和笔画之间的转换
- 定义类`Counter`，抽取汉字的频度信息并按照频度、编码、拼音或笔画排序
- 定义类`Extractor`，用于中文分词（暂时使用[jieba](https://github.com/fxsjy/jieba)分词包，之后可能会自己实现一个基于神经网络的分词器）

**[window.py](./window.py)**
- 定义类`Windows.py`，实现交互界面

**[main.py](./main.py)**
- 用户运行文件

## TODO
- 实现等待进度条
- 优化程序执行时间
- 实现user-friendly的菜单
- 优化代码结构，减少冗余量

## 更新日志
**v1.1.0**  
- 实现了字符频度统计功能
- 实现词表提取，并支持按照频度序、内码旭和音序排序输出

**v1.0.0**  
- 实现了笔画<->汉字<->编码的转换，支持标出单个汉字的读音（包括多音字）
- 支持把word/txt文件转换为utf8编码的txt文件 
- 使用pyqt实现了交互式界面