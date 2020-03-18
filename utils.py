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
import time
import shutil
from lxml import etree
from tqdm import tqdm
from pypinyin import lazy_pinyin
from PyQt5.Qt import *

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
        print("*********************Complete**********************")

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
            QApplication.processEvents()

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

                print("*******Start Processing File: " + file_path + "*******")

                for i in tqdm(range(textLength)):
                    if i % (textLength // 100) == 0:
                        time.sleep(0.00001)
                        QApplication.processEvents()

                    char = text[i]
                    if char < u'\u4e00' or char > u'\u9fa5': continue
                    if char not in stats.keys(): 
                        stats[char] = 1
                    else: 
                        stats[char] += 1
                

                stats = [[item[0], int(item[1])] for item in stats.items()]

                for i, row in enumerate(stats):
                    if i % (len(stats) // 100) == 0:
                        time.sleep(0.00001)
                        QApplication.processEvents()

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

                tgt_file_path = os.path.join(tgtPath, 'stats_'+file)
                with codecs.open(tgt_file_path, 'w', encoding='utf_8_sig') as fopen:
                    f_csv = csv.writer(fopen)
                    f_csv.writerow(['character', 'frequency', 'unicode', 'utf8', 'gbk', 'big5', 'pinyin', 'stroke'])
                    f_csv.writerows(stats)
                
                print("*********************Complete!*********************")
    
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

        print("*********************Complete!*********************")
        
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

                print("*******Start Processing File: " + file_path + "*******")

                for i in tqdm(range(textLength)):
                    char = text[i]
                    
                    if i % (textLength // 100) == 0:
                        time.sleep(0.00001)
                        QApplication.processEvents()

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
                
                print("*********************Complete!*********************")

class Extractor(object):
    def __init__(self, converter):
        self.converter = converter

    def segment(self, srcPath, tgtPath):
        if not os.path.isdir(tgtPath):
            os.mkdir(tgtPath)
        
        for file in os.listdir(srcPath):
            file_path = os.path.join(srcPath, file)
            
            if os.path.isdir(file_path):
                self.segment(file_path, os.path.join(tgtPath, file))
            else:
                f = open(file_path, 'rb')
                encode_data = chardet.detect(f.read(1000))
                if encode_data["encoding"] in ["GBK", "GB2312", "ascii", "EUC-JP"]:
                    encode_data["encoding"] = "GBK"
                encoding = encode_data["encoding"]
                f.close()

                with open(file_path, 'r', encoding=encoding) as fopen:
                    textLines = fopen.readlines()

                newLines = []

                print("*******Start Processing File: " + file_path + "*******")
                for i, line in enumerate(tqdm(textLines)):
                    newLine = ' '.join(jieba.cut(line.strip()))
                    newLines.append(newLine+'\n')
                    if i % (len(textLines) // 100) == 0:
                        time.sleep(0.00001)
                        QApplication.processEvents()
                

                tgtPath = os.path.join(tgtPath, 'segmented_' + file)

                with codecs.open(tgtPath, 'w', encoding='utf_8') as fopen:
                    fopen.writelines(newLines)
                
                print("*********************Complete**********************")

    def countSegmentedFile(self, srcPath, tgtPath):
        if not os.path.isdir(tgtPath):
            os.mkdir(tgtPath)
        
        for file in os.listdir(srcPath):
            file_path = os.path.join(srcPath, file)

            if os.path.isdir(file_path):
                self.countSegmentedFile(file_path, os.path.join(tgtPath, file))
            else:
                f = open(file_path, 'rb')
                encode_data = chardet.detect(f.read(1000))
                if encode_data["encoding"] in ["GBK", "GB2312", "ascii", "EUC-JP"]:
                    encode_data["encoding"] = "GBK"
                encoding = encode_data["encoding"]
                f.close()

                with open(file_path, 'r', encoding=encoding) as fopen:
                    text = fopen.readlines()

                stats = {}

                print("*******Start Processing File: " + file_path + "*******")

                for i, line in tqdm(enumerate(text)):
                    if i % (len(text) // 100 + 1) == 0:
                        time.sleep(0.00001)
                        QApplication.processEvents()
                    words = line.strip().split(' ')
                    for word in words:
                        if word not in stats.keys(): 
                            stats[word] = 1
                        else: 
                            stats[word] += 1

                stats = [[item[0], int(item[1])] for item in stats.items()] # [word, frequency]

                for i, row in tqdm(enumerate(stats)):
                    if i % (len(stats) // 100) == 0:
                        time.sleep(0.00001)
                        QApplication.processEvents()
                    word = row[0]
                    wordUnicode = ''
                    wordUtf8 = ''
                    wordGBK = ''
                    wordBig5 = ''
                    wordStroke = 0
                    for character in word:
                        characterUnicode = str(self.converter.dict_char_to_unicode.get(character, "-1"))
                        characterUtf8 = str(self.converter.dict_char_to_utf8.get(character, "-1"))
                        characterGBK = str(self.converter.dict_char_to_gbk.get(character, "-1"))
                        characterBig5 = str(self.converter.dict_char_to_big5.get(character, "-1"))
                        characterStroke = self.converter.dict_char_to_stroke.get(character, 0)
                        wordUnicode += characterUnicode
                        wordUtf8 += characterUtf8
                        wordBig5 += characterBig5
                        wordGBK += characterGBK
                        wordStroke += int(characterStroke)
                    wordPinyin = ''.join(lazy_pinyin(word))
                        
                    row.append(wordUnicode)
                    row.append(wordUtf8)
                    row.append(wordGBK)
                    row.append(wordBig5)
                    row.append(wordPinyin)
                    row.append(int(wordStroke))

                file = file.split('.')
                file.pop(-1)
                file.append('csv')
                file = '.'.join(file)

                tgt_file_path = os.path.join(tgtPath, 'stats_'+file)
                with codecs.open(tgt_file_path, 'w', encoding='utf_8_sig') as fopen:
                    f_csv = csv.writer(fopen)
                    f_csv.writerow(['word', 'frequency', 'unicode', 'utf8', 'gbk', 'big5', 'pinyin', 'stroke'])
                    f_csv.writerows(stats)           

                print("*********************Complete**********************")
    
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
        
        print("*********************Complete**********************")

class Corpus(object):
    def __init__(self, converter):
        self.converter = converter

    def addCorpusPath(self, path):
        self.path = path

    def listFile(self, path):
        dirs = os.listdir(path)
        fileDir = []
        for file in dirs:
            if os.path.isfile(os.path.join(path, file)):
                fileDir.append(file)
            else:
                fileDir.append(self.listFile((os.path.join(path, file))))

        return fileDir

    def getChar(self, file):
        text = self.getRawText(file)
        charFreqDict = {}
        for char in text:
            if char not in charFreqDict.keys():
                charFreqDict[char] = 0
            charFreqDict[char] += 1
        
        # 按照字频排序
        charFreqDict = dict(sorted(charFreqDict.items(), key = lambda item: item[1], reverse=True))
        return charFreqDict

    def getId(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//id/text()')
        return result[0] if result != [] else ''

    def getNationality(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//nationality/text()')
        return result[0] if result != [] else ''

    def getSex(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//sex/text()')
        return result[0] if result != [] else ''

    def getAge(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//age/text()')
        return result[0] if result != [] else ''

    def getLanguage(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//first_language/text()') + ['-'] + \
            parsed.xpath('//major/text()')
        return result[0] if result != [] else ''
    
    def getYear(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//school_year/text()')
        return result[0] if result != [] else ''

    def getMonthStudy(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//month_of_study/text()')
        return result[0] if result != [] else ''

    def getEduLanguage(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//educational_language/text()')
        return result[0] if result != [] else ''

    def getChuken(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        result = parsed.xpath('//chuken/text()')
        return result[0] if result != [] else ''

    def getRawText(self, file):
        #parsed = etree.parse(file, etree.HTMLParser())
        #rawText = ''.join(parsed.xpath('//text//*/text()'))
        parsed = etree.parse(file, etree.HTMLParser())
        # 找出所有段落
        paragraphs = parsed.xpath('//paragraph')
        # 找到所有error结点

        rawText = []

        # 把每个段落里的error结点都打上标记
        for paragraph in paragraphs:
            if paragraph.text:
                rawText.append(paragraph.text)
            
            #遍历子节点
            for sub in paragraph.iterchildren():
                rawText.append(sub.text if sub.text != None else '')
                # tail是当前结点到下个邻居结点之间的文本内容，如果没有文本则返回None
                if sub.tail: 
                    rawText.append(sub.tail)
            rawText.append('\n')

        rawText = ''.join(rawText).strip()
        return rawText

    def getModifiedText(self, file):
        parsed = etree.parse(file, etree.HTMLParser())
        # 找出所有段落
        paragraphs = parsed.xpath('//paragraph')
        # 找到所有error结点
        errors = parsed.xpath('//error')
        errorNum = len(errors) 

        texts = []

        # 把每个段落里的error结点都打上标记
        for paragraph in paragraphs:
            if paragraph.text:
                texts.append(paragraph.text)
            
            #遍历子节点
            for sub in paragraph.iterchildren():
                texts.append('#%s#' % sub.get('id', ''))
                # tail是当前结点到下个邻居结点之间的文本内容，如果没有文本则返回None
                if sub.tail: 
                    texts.append(sub.tail)
            texts.append('<br>')

        texts = ''.join(texts).strip()

        # 把每个error标记替换
        for i in range(1, errorNum+1):
            errorTag = '#'+str(i)+'#'
            _type = errors[i-1].attrib['type']
            if _type == 'delete':
                revised = '[DELETED]'
            else:
                revised = errors[i-1].attrib['revised']
            texts = texts.replace(errorTag, '<font color="red">'+revised+'</font>')
        
        return texts

    def getErrorStat(self, file):
        parsed = etree.parse(file, etree.HTMLParser())

        errorList = []
        errors = parsed.xpath('//error')

        for error in errors:
            attrib = error.attrib
            raw = error.text
            _id = attrib['id']
            _type = attrib['type']
            category = attrib['category']
            revised = attrib['revised']
            errorList.append([_id, raw, revised, _type, category])

        return errorList

    def getModifyStat(self, file):
        parsed = etree.parse(file, etree.HTMLParser())

        modifyTypeDict = {}
        errors = parsed.xpath('//error')

        for error in errors:
            attrib = error.attrib
            _type = attrib['type']
            if _type not in modifyTypeDict.keys():
                modifyTypeDict[_type] = 0
            modifyTypeDict[_type] += 1
        
        return modifyTypeDict

    def getErrorTypeStat(self, file):
        parsed = etree.parse(file, etree.HTMLParser())

        errorTypeDict = {}
        errors = parsed.xpath('//error')

        for error in errors:
            attrib = error.attrib
            category = attrib['category']
            if category not in errorTypeDict.keys():
                errorTypeDict[category] = 0
            errorTypeDict[category] += 1
        
        return errorTypeDict
    
    def addFile(self, files):
        if type(files) == list:
            for file in files:
                shutil.copy(file, self.path)
        else:
            shutil.copy(files, self.path)

    def delFile(self, files):
        if type(files) == list:
            for file in files:
                os.remove(file)
        else:
            os.remove(files)

    def retrieve(self, _id, age, text, nationality, sex):
        dirs = os.listdir(self.path)
        fileDir = []
        for f in dirs:
            file = os.path.join(self.path, f)
            if os.path.isfile(file):
                fileId = self.getId(file)
                fileAge = self.getAge(file)
                fileText = self.getRawText(file)
                fileNationality = self.getNationality(file)
                fileSex = self.getSex(file)

                if _id != '' and fileId.find(_id) == -1: continue
                if age != '' and fileAge != age: continue 
                if text != '' and fileText.find(text) == -1: continue
                if nationality != '不限' and nationality != fileNationality: continue
                if sex != '不限' and sex != fileSex: continue

                fileDir.append(f)

        return fileDir