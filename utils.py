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
import string
from pypinyin import lazy_pinyin
from tqdm import tqdm

class Converter(object):
    def __init__(self):
        print("*************Constructing dictionaries*************")
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
        print("*************Complete*************")   

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
    def __init__(self, converter):
        self.converter = converter

    def countFile(self, srcPath, tgtPath):
        if not os.path.isdir(tgtPath):
            os.mkdir(tgtPath)
        
        for file in os.listdir(srcPath):
            file_path = os.path.join(srcPath, file)

            if os.path.isdir(file_path):
                self.countFile(file_path, os.path.join(tgtPath, file))
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
                    if char < u'\u4e00' or char > u'\u9fa5': continue
                    if char not in stats.keys(): 
                        stats[char] = 1
                    else: 
                        stats[char] += 1

                stats = [[item[0], int(item[1])] for item in stats.items()]

                for row in stats:
                    char = row[0]
                    row.append(str(self.converter.dict_char_to_unicode.get(char, "-1")))
                    row.append(str(self.converter.dict_char_to_utf8.get(char, "-1")))
                    row.append(str(self.converter.dict_char_to_gbk.get(char, "-1")))
                    row.append(str(self.converter.dict_char_to_big5.get(char, "-1")))
                    row.append(lazy_pinyin(char)[0])
                    row.append(self.converter.dict_char_to_stroke.get(char, -1))

                file = file.split('.')
                file.pop(-1)
                file.append('csv')
                file = '.'.join(file)

                tgt_file_path = os.path.join(tgtPath, 'stats_'+file, )
                with codecs.open(tgt_file_path, 'w', encoding='utf_8_sig') as fopen:
                    f_csv = csv.writer(fopen)
                    f_csv.writerow(['character', 'frequency', 'unicode', 'utf8', 'gbk', 'big5', 'pinyin', 'stroke'])
                    f_csv.writerows(stats)
    
    def sortBy(self, statsFile, mode="frequency", reverse=False):
        with codecs.open(statsFile, 'r', encoding='utf_8_sig') as fopen:
            f_csv = csv.reader(fopen)
            headings = next(f_csv)
            stats = [row for row in f_csv]
        
        if mode == 'frequency':
            stats.sort(key=lambda item: int(item[1]), reverse=reverse)
        elif mode == 'unicode':
            stats.sort(key=lambda item: str(item[2]), reverse=reverse)
        elif mode == 'utf8':
            stats.sort(key=lambda item: str(item[3]), reverse=reverse)
        elif mode == 'gbk':
            stats.sort(key=lambda item: str(item[4]), reverse=reverse)
        elif mode == 'big5':
            stats.sort(key=lambda item: str(item[5]), reverse=reverse)
        elif mode == 'pinyin':
            stats.sort(key=lambda item: str(item[6]), reverse=reverse)
        else:
            stats.sort(key=lambda item: int(item[7]), reverse=reverse)

        statsFile = statsFile.split('/')
        file = statsFile[-1]
        file = 'sorted_'+file
        statsFile.pop(-1)
        statsFile.append(file)
        filePath = '/'.join(statsFile)

        with codecs.open(filePath, 'w', encoding='utf_8_sig') as fopen:
            f_csv = csv.writer(fopen)
            f_csv.writerow(headings)
            f_csv.writerows(stats)

    def groupBy(self, srcPath, tgtPath):
        if not os.path.isdir(tgtPath):
            os.mkdir(tgtPath)

        for file in os.listdir(srcPath):
            file_path = os.path.join(srcPath, file)

            if os.path.isdir(file_path):
                self.groupBy(file_path, tgtPath)
            else:
                f = open(file_path, 'rb')
                encode_data = chardet.detect(f.read(1000))
                if encode_data["encoding"] in ["GBK", "GB2312", "ascii", "EUC-JP"]:
                    encode_data["encoding"] = "GBK"
                encoding = encode_data["encoding"]
                f.close()

                with open(file_path, 'r', encoding=encoding) as fopen:
                    text = fopen.read()

                puncs = string.punctuation + '！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝｢｣、〃《》【】'
                textLength = len(text)

                charNum = 0
                alphaNum = 0
                digitNum = 0
                puncNum = 0
                otherNum = 0

                for i in tqdm(range(textLength)):
                    char = text[i]
                    if char >= u'\u4e00' and char <= u'\u9fa5':
                        charNum += 1
                    elif char.isalpha() or (char >= u'\uff21' and char <= u'\uff3a') or (char >= u'\uff41' and char <= u'\uff5a'):
                        alphaNum += 1
                    elif char.isdigit() or (char >= u'\uff10' and char <= u'\uff19'):
                        digitNum += 1
                    elif char in puncs:
                        puncNum += 1
                    else: otherNum += 1
                
                tgtPathFile = os.path.join(tgtPath, 'log.txt')
                with codecs.open(tgtPathFile, 'a', encoding='utf_8') as fopen:
                    fopen.write('File Path: ' + file_path + '\n')
                    fopen.write('    ****The number of Chinese characters is ' + str(charNum) + '\n')
                    fopen.write('    ****The number of English characters is ' + str(alphaNum) + '\n')
                    fopen.write('    ****The number of digits is ' + str(digitNum) + '\n')
                    fopen.write('    ****The number of punctuations is ' + str(puncNum) + '\n')
                    fopen.write('    ****The number of other characters is ' + str(otherNum) + '\n\n')

class Extractor(object):
    def __init__(self):
        pass

