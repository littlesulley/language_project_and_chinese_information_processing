"""
Author: Sulley
Date: 2020.2.29
"""

import chardet
import codecs
import os
import sys
import csv
import xlrd
import docx
import jieba
import itertools, string
from pypinyin import pinyin, lazy_pinyin, Style
from PyQt5.Qt import *
from utils import Converter, Counter, Extractor, Corpus
from window import Window, EmittingStream



if __name__ == '__main__':
    converter = Converter()
    counter = Counter(converter)
    extractor = Extractor(converter)
    corpus = Corpus(converter)

    app = QApplication(sys.argv)
    exe = Window(converter, counter, extractor, corpus)
    sys.exit(app.exec_())