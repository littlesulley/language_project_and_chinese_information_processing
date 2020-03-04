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
from tqdm import tqdm

class Converter(object):
    def __init__(self):

        self.dict_char_to_unicode, self.dict_unicode_to_char = \
            self.dictCharUnicode()
        self.dict_char_to_utf8, self.dict_utf8_to_char = \
            self.dictCharUTF8()
        self.dict_char_to_gbk, self.dict_gbk_to_char = \
            self.dictCharGBK()
        self.dict_char_to_big5, self.dict_big5_to_char = \
            self.dictCharBig5()
        self.dict_char_to_stroke, self.dict_stroke_to_char = \
            self.dictCharStroke()

    def dictCharUnicode(self):
        codeset = xlrd.open_workbook(filename = 'codeset.xls')
        stats = codeset.sheet_by_index(0)
    
        chars = stats.col_values(0)
        chars = chars[1:]
        codes = stats.col_values(2)
        codes = codes[1:]

        self.dict_char_to_unicode, self.dict_unicode_to_char = {}, {}
        for char, code in zip(chars, codes):
            self.dict_char_to_unicode[char] = code
            self.dict_unicode_to_char[code] = char

        return self.dict_char_to_unicode, self.dict_unicode_to_char

    def dictCharUTF8(self):
        codeset = xlrd.open_workbook(filename = 'codeset.xls')
        stats = codeset.sheet_by_index(0)
    
        chars = stats.col_values(0)
        chars = chars[1:]
        codes = stats.col_values(4)
        codes = codes[1:]

        self.dict_char_to_utf8, self.dict_utf8_to_char = {}, {}
        for char, code in zip(chars, codes):
            self.dict_char_to_utf8[char] = code
            self.dict_utf8_to_char[code] = char

        return self.dict_char_to_utf8, self.dict_utf8_to_char

    def dictCharGBK(self):
        codeset = xlrd.open_workbook(filename = 'codeset.xls')
        stats = codeset.sheet_by_index(0)
    
        chars = stats.col_values(0)
        chars = chars[1:]
        codes = stats.col_values(1)
        codes = codes[1:]

        self.dict_char_to_gbk, self.dict_gbk_to_char = {}, {}
        for char, code in zip(chars, codes):
            self.dict_char_to_gbk[char] = code
            self.dict_gbk_to_char[code] = char

        return self.dict_char_to_gbk, self.dict_gbk_to_char

    def dictCharBig5(self):
        codeset = xlrd.open_workbook(filename = 'codeset.xls')
        stats = codeset.sheet_by_index(0)
    
        chars = stats.col_values(0)
        chars = chars[1:]
        codes = stats.col_values(6)
        codes = codes[1:]

        self.dict_char_to_big5, self.dict_big5_to_char = {}, {}
        for char, code in zip(chars, codes):
            self.dict_char_to_big5[char] = code
            self.dict_big5_to_char[code] = char

        return self.dict_char_to_big5, self.dict_big5_to_char

    def dictCharStroke(self):

        with open('Chinese.csv', 'r', encoding='gbk') as fChinese:
            chinese = csv.reader(fChinese)
            char_to_id = {}
            for row in chinese:
                char_to_id[row[1]] = row[0]
            
        with open('ChineseStroke.csv', 'r', encoding='utf-8') as fStroke:
            strokes = csv.reader(fStroke)
            id_to_stroke = {}
            for row in strokes:
                id_to_stroke[row[0]] = row[1]
        
        self.dict_char_to_stroke = {}
        self.dict_stroke_to_char = {}

        for key in char_to_id.keys():
            value = id_to_stroke[char_to_id[key]]
            self.dict_char_to_stroke[key] = value
            if value not in self.dict_stroke_to_char:
                self.dict_stroke_to_char[value] = []
            self.dict_stroke_to_char[value].append(key)

        return self.dict_char_to_stroke, self.dict_stroke_to_char
    
    
    def decodeFile(self, srcPath, tgtPath):
        if not os.path.isdir(tgtPath):
            os.mkdir(tgtPath)
        
        for file in os.listdir(srcPath):
            file_path = os.path.join(srcPath, file)
            
            # 首先需要判断是文件夹还是文件
            if os.path.isdir(file_path):
                self.decodeFile(file_path, os.path.join(tgtPath, file))
            else:
                f = open(file_path, 'rb')
                encode_data = chardet.detect(f.read(1000))
                if encode_data["encoding"] in ["GBK", "GB2312", "ascii", "EUC-JP"]:
                    encode_data["encoding"] = "GBK"
                encoding = encode_data["encoding"]
                f.close()

                if file_path.endswith('txt') or file_path.endswith('TXT'):
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()

                # 因为python下没有很好的支持CJK文字的pdf提取包，故暂时不支持pdf内容的提取
                # elif file_path.endswith('pdf'):

                else:
                    docFile = docx.Document(file_path)
                    text = '\n'.join([paragraph.text for paragraph in docFile.paragraphs])
                

                file = file.split('.')
                file.pop(-1)
                file.append('txt')
                file = '.'.join(file)
                
                tgt_file_path = os.path.join(tgtPath, file)
                with open(tgt_file_path, 'w', encoding='utf-8') as fout:
                    fout.write(text)

class Counter(object):  
    def __init__(self):
        pass

    def countFile(self, srcPath, tgtPath, mode = 'character'):
        if not os.path.isdir(tgtPath):
            os.mkdir(tgtPath)
        
        for file in os.listdir(srcPath):
            file_path = os.path.join(srcPath, file)

            if os.path.isdir(file_path):
                self.countFile(file_path, os.path.join(tgtPath, file), mode=mode)
            else:
                f = open(file_path, 'rb')
                encode_data = chardet.detect(f.read(1000))
                if encode_data["encoding"] in ["GBK", "GB2312", "ascii", "EUC-JP"]:
                    encode_data["encoding"] = "GBK"
                encoding = encode_data["encoding"]
                f.close()

                with open(file_path, 'r', encoding=encoding) as fopen:
                    text = fopen.read()

                stats = {}
                textLength = len(text)

                for i in tqdm(range(textLength)):
                    char = text[i]
                    if mode == 'any': pass      # 所有字符
                    elif mode == 'character':   # 汉字
                        if char < u'\u4e00' or char > u'\u9fa5': continue
                    elif mode == 'digit':       # 数字
                        if not char.isdigit(): continue
                    elif mode == 'alpha':       # 字母
                        if not char.isalpha(): continue
                    else:
                        print("Mode Wrong!")
                        exit()

                    if char not in stats.keys(): 
                        stats[char] = 1
                    else: 
                        stats[char] += 1

                stats = [[item[0], item[1]] for item in stats.items()]

                file = file.split('.')
                file.pop(-1)
                file.append('csv')
                file = '.'.join(file)

                tgt_file_path = os.path.join(tgtPath, 'stats_'+file, )
                with codecs.open(tgt_file_path, 'w', encoding='utf_8_sig') as fopen:
                    f_csv = csv.writer(fopen)
                    f_csv.writerows(stats)

class Extractor(object):
    def __init__(self):
        pass


counter = Counter()
counter.countFile('./03_test/GBK', './03_test/GBK')