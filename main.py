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
from utils import Converter, Counter, Extractor
from window import Window



if __name__ == '__main__':
    converter = Converter()
    counter = Counter(converter)
    extractor = Extractor(converter)
    app = QApplication(sys.argv)
    exe = Window(converter, counter, extractor)
    sys.exit(app.exec_())