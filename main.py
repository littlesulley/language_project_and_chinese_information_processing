import chardet
import codecs
import os
import sys
import csv
import xlrd
import docx
import jieba
from pypinyin import pinyin, lazy_pinyin, Style
from PyQt5.Qt import *
from utils import Converter
from window import Window



if __name__ == '__main__':
    converter = Converter()
    app = QApplication(sys.argv)
    exe = Window(converter)
    sys.exit(app.exec_())