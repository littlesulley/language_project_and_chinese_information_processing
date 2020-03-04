# Chinese Language Processor
**Current version: v1.0.0**  
**Developed by Sulley**

## 程序简介
- 实现了笔画<->汉字<->编码的转换，支持标出单个汉字的读音（包括多音字）
- 支持把word/txt文件转换为utf8编码的txt文件 

## 使用方法

- 本程序基于python实现，直接在命令行输入python main.py稍等即可

- 为了确保程序能够正确进行，请首先在运行之前在命令行输入以下命令：

```python
pip install --upgrade pip # 更新pip
pip install xlrd pypinyin chardet docx pyqt5 # 安装依赖包
```

## 程序说明
**[utils.py](./utils.py)**
- 定义类`Converter`，用于汉字、编码和笔画之间的转换；

**[window.py](./window.py)**
- 定义类`Windows.py`，实现交互界面

**[main.py](./main.py)**
- 用户运行文件



## 更新日志
**v1.1.0**  


**v1.0.0**  
- 实现了笔画<->汉字<->编码的转换，支持标出单个汉字的读音（包括多音字）
- 支持把word/txt文件转换为utf8编码的txt文件 
- 使用pyqt实现了交互式界面