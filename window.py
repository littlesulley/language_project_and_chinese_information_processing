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
import string
import jieba
from pypinyin import pinyin, lazy_pinyin, Style
from PyQt5.Qt import *


class Window(QMainWindow):
    def __init__(self, converter, counter, extractor):
        super().__init__()
        self.init()
        self.windowCenter()
        self.converter = converter
        self.counter = counter 
        self.extractor = extractor
    
    def init(self):
        self.setFixedSize(900, 1200)
        self.setWindowTitle('Chinese Language Processor')
        self.setWindowIcon(QIcon('./resource/emiya.jpg'))

        # 汉字转编码
        self.label4 = QLabel(self)
        self.label4.setText('***汉字转编码***')
        self.label4.resize(300, 20)
        self.label4.move(250, 20)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setStyleSheet('font-size:15px;font-weight:bold;font-family:Source Code Pro;')

        
        self.charInputButton = QPushButton('输入汉字', self)
        self.charInputButton.setToolTip('请输入<b>一个</b>汉字')
        self.charInputButton.move(100, 50)
        self.charInputButton.resize(100, 30)
        self.charInputButton.clicked.connect(self.inputDialog)

        self.charShowLabel = QLabel('', self)
        self.charShowLabel.move(210, 50)

        self.charUTFLabel = QLabel('UTF8:', self)
        self.charUTFLabel.move(350, 50)
        self.charUTFShowLabel = QLabel('', self)
        self.charUTFShowLabel.move(400, 50)
        self.charUTFShowLabel.resize(90,30)

        self.charUnicodeLabel = QLabel('Unicode:', self)
        self.charUnicodeLabel.move(500, 50)
        self.charUnicodeShowLabel = QLabel('', self)
        self.charUnicodeShowLabel.move(580, 50)
        self.charUnicodeShowLabel.resize(90,30)

        self.charBig5Label = QLabel('Big5:', self)
        self.charBig5Label.move(680, 50)
        self.charBig5ShowLabel = QLabel('', self)
        self.charBig5ShowLabel.move(750, 50)
        self.charBig5ShowLabel.resize(90,30)

        self.charGBKLabel = QLabel('GBK:', self)
        self.charGBKLabel.move(350, 100)
        self.charGBKShowLabel = QLabel('', self)
        self.charGBKShowLabel.move(400, 100)
        self.charGBKShowLabel.resize(90,30)


        self.charPinyinLabel = QLabel('pinyin:', self)
        self.charPinyinLabel.move(500, 100)
        self.charPinyinShowLabel = QLabel('', self)
        self.charPinyinShowLabel.resize(90,60)
        self.charPinyinShowLabel.move(580, 105)
        self.charPinyinShowLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.charStrokeLabel = QLabel('Stroke:', self)
        self.charStrokeLabel.move(680, 100)
        self.charStrokeShowLabel = QLabel('', self)
        self.charStrokeShowLabel.move(750, 100)
        self.charStrokeShowLabel.resize(90,30)

        # 编码转汉字
        self.label4 = QLabel(self)
        self.label4.setText('***编码转汉字***')
        self.label4.resize(300, 20)
        self.label4.move(250, 170)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setStyleSheet('font-size:15px;font-weight:bold;font-family:Source Code Pro;')

        self.codeInputButton = QPushButton('输入编码', self)
        self.codeInputButton.setToolTip('请输入编码，大小写均可')
        self.codeInputButton.move(100, 200)
        self.codeInputButton.resize(100, 30)
        self.codeInputButton.clicked.connect(self.inputDialog)

        self.codeShowLabel = QLabel('', self)
        self.codeShowLabel.move(210, 200)

        self.codeTypeLabel = QLabel('Code Type:', self)
        self.codeTypeLabel.move(350, 200)

        choices = ['UTF-8', 'Unicode', 'Big5', 'GBK']
        self.codeTypeBox = QComboBox(self)
        self.codeTypeBox.move(460, 200)
        self.codeTypeBox.addItems(choices)
        
        self.codeConfirmButton = QPushButton('Confirm', self)
        self.codeConfirmButton.move(600, 200)
        self.codeConfirmButton.clicked.connect(self.codeConfirm)

        self.codeCharLable = QLabel('',self)
        self.codeCharLable.move(720, 200)

        # 笔画转汉字
        self.label4 = QLabel(self)
        self.label4.setText('***笔画转汉字***')
        self.label4.resize(300, 20)
        self.label4.move(250, 260)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setStyleSheet('font-size:15px;font-weight:bold;font-family:Source Code Pro;')

        self.strokeInputButton = QPushButton('输入笔画', self)
        self.strokeInputButton.setToolTip('请输入一个正整数')
        self.strokeInputButton.move(100, 300)
        self.strokeInputButton.resize(100, 30)
        self.strokeInputButton.clicked.connect(self.inputDialog)

        self.strokeShowLabel = QLabel('', self)
        self.strokeShowLabel.move(210, 300)

        self.strokeCharShowLabel = QLabel('Characters:', self)
        self.strokeCharShowLabel.move(350, 300)

        self.strokeCharBox = QComboBox(self)
        self.strokeCharBox.move(460, 300)

        # 文件转换
        self.label4 = QLabel(self)
        self.label4.setText('***转换文件夹下的文件编码***')
        self.label4.resize(300, 20)
        self.label4.move(250, 350)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setStyleSheet('font-size:15px;font-weight:bold;font-family:Source Code Pro;')

        self.srcPath = ""
        self.tgtPath = ""

        self.openSrcFile = QPushButton('Open Source Folder', self)
        self.openSrcFile.setToolTip('输入待转换的文件夹目录')
        self.openSrcFile.clicked.connect(self.inputDialog)
        self.openSrcFile.move(100, 400)
        self.openSrcFile.resize(200, 30)

        self.srcPathLineEdit = QLineEdit(self)
        self.srcPathLineEdit.setObjectName("filePathlineEdit")
        self.srcPathLineEdit.setPlaceholderText('Source folder path')
        self.srcPathLineEdit.move(310, 400)
        self.srcPathLineEdit.resize(260, 30)

        self.openTgtFile = QPushButton('Open Target Folder', self)
        self.openTgtFile.setToolTip('输入转换后的文件夹目录')
        self.openTgtFile.clicked.connect(self.inputDialog)
        self.openTgtFile.move(100, 440)
        self.openTgtFile.resize(200, 30)

        self.tgtPathLineEdit = QLineEdit(self)
        self.tgtPathLineEdit.setObjectName("filePathlineEdit")
        self.tgtPathLineEdit.setPlaceholderText('Target folder path')
        self.tgtPathLineEdit.move(310, 440)
        self.tgtPathLineEdit.resize(260, 30)

        self.pathButton = QPushButton('Confirm', self)
        self.pathButton.move(600, 400)
        self.pathButton.resize(100, 30)
        self.pathButton.clicked.connect(self.pathConfirm)

        self.pathLabel = QLabel(self)
        self.pathLabel.setAlignment(Qt.AlignCenter)
        self.pathLabel.move(600, 440)
        self.pathLabel.resize(100, 30)
        self.pathLabel.setStyleSheet("color:red;font-weight:bold;")


        # 字频统计及分类统计
        self.label5 = QLabel(self)
        self.label5.setText('***统计文件夹下的文件信息并排序***')
        self.label5.resize(300, 20) 
        self.label5.move(250, 500)
        self.label5.setAlignment(Qt.AlignCenter)
        self.label5.setStyleSheet('font-size:15px;font-weight:bold;font-family:Source Code Pro;')

        self.statsSrcPath = ''
        self.statsTgtPath = ''

        self.openStatsSrcFile = QPushButton('Open Source Folder', self)
        self.openStatsSrcFile.setToolTip('输入源文件夹目录')
        self.openStatsSrcFile.clicked.connect(self.inputDialog)
        self.openStatsSrcFile.move(100, 550)
        self.openStatsSrcFile.resize(200, 30)

        self.statsSrcPathLineEdit = QLineEdit(self)
        self.statsSrcPathLineEdit.setObjectName('filePathlineEdit')
        self.statsSrcPathLineEdit.setPlaceholderText('Source folder path')
        self.statsSrcPathLineEdit.move(310, 550)
        self.statsSrcPathLineEdit.resize(260, 30)

        self.openStatsTgtFile = QPushButton('Open Target Folder', self)
        self.openStatsTgtFile.setToolTip('输入目标文件夹目录')
        self.openStatsTgtFile.clicked.connect(self.inputDialog)
        self.openStatsTgtFile.move(100, 590)
        self.openStatsTgtFile.resize(200, 30)

        self.statsTgtPathLineEdit = QLineEdit(self)
        self.statsTgtPathLineEdit.setObjectName('filePathlineEdit')
        self.statsTgtPathLineEdit.setPlaceholderText('Target folder path')
        self.statsTgtPathLineEdit.move(310, 590)
        self.statsTgtPathLineEdit.resize(260, 30)

        self.statsPathButton = QPushButton('Confirm', self)
        self.statsPathButton.move(600, 550)
        self.statsPathButton.resize(100, 30)
        self.statsPathButton.clicked.connect(self.pathConfirm)

        self.statsPathLabel = QLabel(self)
        self.statsPathLabel.setAlignment(Qt.AlignCenter)
        self.statsPathLabel.move(600, 590)
        self.statsPathLabel.resize(100, 30)
        self.statsPathLabel.setStyleSheet("color:red;font-weight:bold;")

        # 排序文件

        self.sortPathButton = QPushButton('Open .csv File', self)
        self.sortPathButton.setToolTip('输入已统计的.csv文件目录')
        self.sortPathButton.clicked.connect(self.inputDialog)
        self.sortPathButton.move(100, 630)
        self.sortPathButton.resize(200, 30)

        self.sortPathLineEdit = QLineEdit(self)
        self.sortPathLineEdit.setObjectName('filePathlineEdit')
        self.sortPathLineEdit.setPlaceholderText('Open a .csv file to sort')
        self.sortPathLineEdit.move(310, 630)
        self.sortPathLineEdit.resize(260, 30)

        self.sortPath = ''

        self.sortTypeLabel = QLabel('Sort By: ', self)
        self.sortTypeLabel.resize(100, 30)
        self.sortTypeLabel.move(100, 675)
        self.sortTypeLabel.setAlignment(Qt.AlignRight)

        self.sortTypeComboBox = QComboBox(self)
        self.sortTypeComboBox.move(210, 670)
        sortChoices = ['frequency', 'unicode', 'utf8', 'gbk', 'big5', 'pinyin', 'stroke']
        self.sortTypeComboBox.addItems(sortChoices)
        self.sortTypeComboBox.resize(150, 30)

        self.sortTypeLabel = QLabel('Reverse: ', self)
        self.sortTypeLabel.resize(100, 30)
        self.sortTypeLabel.move(400, 675)
        self.sortTypeLabel.setAlignment(Qt.AlignRight)

        self.reverseCheckBox = QCheckBox('Yes', self)
        self.reverseCheckBox.move(510, 670)

        self.sortConfirmButton = QPushButton('Confirm', self)
        self.sortConfirmButton.move(600, 670)
        self.sortConfirmButton.resize(100, 30)
        self.sortConfirmButton.clicked.connect(self.pathConfirm)

        self.sortConfirmLabel = QLabel(self)
        self.sortConfirmLabel.setAlignment(Qt.AlignCenter)
        self.sortConfirmLabel.move(710, 670)
        self.sortConfirmLabel.resize(100, 30)
        self.sortConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        # 分类统计字符写入log.txt
        self.label6 = QLabel(self)
        self.label6.setText('***统计字符并写入日志***')
        self.label6.resize(300, 20) 
        self.label6.move(250, 720)
        self.label6.setAlignment(Qt.AlignCenter)
        self.label6.setStyleSheet('font-size:15px;font-weight:bold;font-family:Source Code Pro;')

        self.groupSrcPath = ''
        self.groupTgtPath = ''

        self.groupSrcButton = QPushButton('Open Source Folder', self)
        self.groupSrcButton.setToolTip('输入源文件夹目录')
        self.groupSrcButton.clicked.connect(self.inputDialog)
        self.groupSrcButton.move(100, 750)
        self.groupSrcButton.resize(200, 30)

        self.groupSrcLineEdit = QLineEdit(self)
        self.groupSrcLineEdit.setObjectName('filePathlineEdit')
        self.groupSrcLineEdit.setPlaceholderText('Source folder path')
        self.groupSrcLineEdit.move(310, 750)
        self.groupSrcLineEdit.resize(260, 30)

        self.groupTgtButton = QPushButton('Open Target Folder', self)
        self.groupTgtButton.setToolTip('输入目标文件夹目录，将在该目录下创建一个log.txt文件存放统计信息')
        self.groupTgtButton.clicked.connect(self.inputDialog)
        self.groupTgtButton.move(100, 790)
        self.groupTgtButton.resize(200, 30)

        self.groupTgtLineEdit = QLineEdit(self)
        self.groupTgtLineEdit.setObjectName('filePathlineEdit')
        self.groupTgtLineEdit.setPlaceholderText('Target folder path')
        self.groupTgtLineEdit.move(310, 790)
        self.groupTgtLineEdit.resize(260, 30)

        self.groupConfirmButton = QPushButton('Confirm', self)
        self.groupConfirmButton.move(600, 750)
        self.groupConfirmButton.resize(100, 30)
        self.groupConfirmButton.clicked.connect(self.pathConfirm)

        self.groupConfirmLabel = QLabel(self)
        self.groupConfirmLabel.setAlignment(Qt.AlignCenter)
        self.groupConfirmLabel.move(600, 790)
        self.groupConfirmLabel.resize(100, 30)
        self.groupConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        # 分词及统计词频
        self.label7 = QLabel(self)
        self.label7.setText('***分词并统计词频***')
        self.label7.resize(300, 20) 
        self.label7.move(250, 840)
        self.label7.setAlignment(Qt.AlignCenter)
        self.label7.setStyleSheet('font-size:15px;font-weight:bold;font-family:Source Code Pro;')

        ## 分词
        self.segmentSrcPath = ''
        self.segmentTgtPath = ''

        self.segmentSrcButton = QPushButton('Open Source Folder', self)
        self.segmentSrcButton.setToolTip('输入待分词源文件夹目录')
        self.segmentSrcButton.clicked.connect(self.inputDialog)
        self.segmentSrcButton.move(100, 860)
        self.segmentSrcButton.resize(200, 30)

        self.segmentSrcLineEdit = QLineEdit(self)
        self.segmentSrcLineEdit.setObjectName('filePathlineEdit')
        self.segmentSrcLineEdit.setPlaceholderText('Source folder path')
        self.segmentSrcLineEdit.move(310, 860)
        self.segmentSrcLineEdit.resize(260, 30)

        self.segmentTgtButton = QPushButton('Open Target Folder', self)
        self.segmentTgtButton.setToolTip('输入分词后目标文件夹目录')
        self.segmentTgtButton.clicked.connect(self.inputDialog)
        self.segmentTgtButton.move(100, 900)
        self.segmentTgtButton.resize(200, 30)

        self.segmentTgtLineEdit = QLineEdit(self)
        self.segmentTgtLineEdit.setObjectName('filePathlineEdit')
        self.segmentTgtLineEdit.setPlaceholderText('Target folder path')
        self.segmentTgtLineEdit.move(310, 900)
        self.segmentTgtLineEdit.resize(260, 30)

        self.segmentConfirmButton = QPushButton('Confirm', self)
        self.segmentConfirmButton.move(600, 860)
        self.segmentConfirmButton.resize(100, 30)
        self.segmentConfirmButton.clicked.connect(self.pathConfirm)

        self.segmentConfirmLabel = QLabel(self)
        self.segmentConfirmLabel.setAlignment(Qt.AlignCenter)
        self.segmentConfirmLabel.move(600, 900)
        self.segmentConfirmLabel.resize(100, 30)
        self.segmentConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        ## 统计词频等信息
        self.wordStatsSrcPath = ''
        self.wordStatsTgtPath = ''

        self.wordStatsSrcButton = QPushButton('Open Source Folder', self)
        self.wordStatsSrcButton.setToolTip('输入待统计已分词源文件夹目录')
        self.wordStatsSrcButton.clicked.connect(self.inputDialog)
        self.wordStatsSrcButton.move(100, 940)
        self.wordStatsSrcButton.resize(200, 30)

        self.wordStatsSrcLineEdit = QLineEdit(self)
        self.wordStatsSrcLineEdit.setObjectName('filePathlineEdit')
        self.wordStatsSrcLineEdit.setPlaceholderText('Source folder path')
        self.wordStatsSrcLineEdit.move(310, 940)
        self.wordStatsSrcLineEdit.resize(260, 30)

        self.wordStatsTgtButton = QPushButton('Open Target Folder', self)
        self.wordStatsTgtButton.setToolTip('输入统计后目标文件夹目录')
        self.wordStatsTgtButton.clicked.connect(self.inputDialog)
        self.wordStatsTgtButton.move(100, 980)
        self.wordStatsTgtButton.resize(200, 30)

        self.wordStatsTgtLineEdit = QLineEdit(self)
        self.wordStatsTgtLineEdit.setObjectName('filePathlineEdit')
        self.wordStatsTgtLineEdit.setPlaceholderText('Target folder path')
        self.wordStatsTgtLineEdit.move(310, 980)
        self.wordStatsTgtLineEdit.resize(260, 30)

        self.wordStatsConfirmButton = QPushButton('Confirm', self)
        self.wordStatsConfirmButton.move(600, 940)
        self.wordStatsConfirmButton.resize(100, 30)
        self.wordStatsConfirmButton.clicked.connect(self.pathConfirm)

        self.wordStatsConfirmLabel = QLabel(self)
        self.wordStatsConfirmLabel.setAlignment(Qt.AlignCenter)
        self.wordStatsConfirmLabel.move(600, 980)
        self.wordStatsConfirmLabel.resize(100, 30)
        self.wordStatsConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        ## 排序
        self.sortWordPathButton = QPushButton('Open .csv File', self)
        self.sortWordPathButton.setToolTip('输入已统计分词的.csv文件目录')
        self.sortWordPathButton.clicked.connect(self.inputDialog)
        self.sortWordPathButton.move(100, 1020)
        self.sortWordPathButton.resize(200, 30)

        self.sortWordPathLineEdit = QLineEdit(self)
        self.sortWordPathLineEdit.setObjectName('filePathlineEdit')
        self.sortWordPathLineEdit.setPlaceholderText('Open a .csv file to sort')
        self.sortWordPathLineEdit.move(310, 1020)
        self.sortWordPathLineEdit.resize(260, 30)

        self.sortWordPath = ''

        self.sortWordTypeLabel = QLabel('Sort By: ', self)
        self.sortWordTypeLabel.resize(100, 30)
        self.sortWordTypeLabel.move(100, 1065)
        self.sortWordTypeLabel.setAlignment(Qt.AlignRight)

        self.sortWordTypeComboBox = QComboBox(self)
        self.sortWordTypeComboBox.move(210, 1060)
        sortChoices = ['frequency', 'unicode', 'utf8', 'gbk', 'big5', 'pinyin', 'stroke']
        self.sortWordTypeComboBox.addItems(sortChoices)
        self.sortWordTypeComboBox.resize(150, 30)

        self.sortWordTypeLabel = QLabel('Reverse: ', self)
        self.sortWordTypeLabel.resize(100, 30)
        self.sortWordTypeLabel.move(400, 1065)
        self.sortWordTypeLabel.setAlignment(Qt.AlignRight)

        self.reverseWordCheckBox = QCheckBox('Yes', self)
        self.reverseWordCheckBox.move(510, 1060)

        self.sortWordConfirmButton = QPushButton('Confirm', self)
        self.sortWordConfirmButton.move(600, 1060)
        self.sortWordConfirmButton.resize(100, 30)
        self.sortWordConfirmButton.clicked.connect(self.pathConfirm)

        self.sortWordConfirmLabel = QLabel(self)
        self.sortWordConfirmLabel.setAlignment(Qt.AlignCenter)
        self.sortWordConfirmLabel.move(710, 1060)
        self.sortWordConfirmLabel.resize(100, 30)
        self.sortWordConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        self.show()
    
    def windowCenter(self):
        screenSize = QDesktopWidget().screenGeometry()
        windowSize = self.geometry()
        newLeft = (screenSize.width() - windowSize.width()) / 2
        newTop = (screenSize.height() - windowSize.height()) / 2
        self.move(newLeft, newTop)
        
    def inputDialog(self):
        sender = self.sender()
        if sender == self.charInputButton:
            char, ok = QInputDialog.getText(self, '输入汉字', '请输入一个汉字：')
            if ok:
                if len(char) != 1:
                    self.charShowLabel.setText('Error')
                    self.charShowLabel.setStyleSheet('color:red;font-weight:bold;')
                else:
                    self.charShowLabel.setText(char)
                    self.charShowLabel.setStyleSheet('font-weight:bold;')

                    self.charUTFShowLabel.setText(self.converter.dict_char_to_utf8.get(char, "-1"))
                    self.charUnicodeShowLabel.setText(self.converter.dict_char_to_unicode.get(char, "-1"))
                    self.charBig5ShowLabel.setText(self.converter.dict_char_to_big5.get(char, "-1"))
                    self.charGBKShowLabel.setText(self.converter.dict_char_to_gbk.get(char, "-1"))
                    self.charStrokeShowLabel.setText(self.converter.dict_char_to_stroke.get(char, "-1"))
                    self.charPinyinShowLabel.setText('\n'.join(pinyin(char, style=Style.TONE, heteronym=True)[0]))

        elif sender == self.codeInputButton:
            code, ok = QInputDialog.getText(self, '输入编码', '请输入编码：')
            if ok:
                self.codeShowLabel.setText(code)
                self.codeShowLabel.setStyleSheet('font-weight:bold;')
        elif sender ==  self.strokeInputButton:
            stroke, ok = QInputDialog.getInt(self, '输入笔画数', '请输入笔画数：')
            if ok:
                if stroke <= 0:
                    self.strokeShowLabel.setText('Error')
                    self.strokeShowLabel.setStyleSheet('color:red;font-weight:bold;')
                else:
                    self.strokeShowLabel.setText(str(stroke))
                    self.strokeShowLabel.setStyleSheet('font-weight:bold;')
                    self.strokeCharBox.clear()
                    self.strokeCharBox.addItems(self.converter.dict_stroke_to_char.get(str(stroke), ["-1"]))
        elif sender == self.openSrcFile:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.srcPathLineEdit.setText(str(path))
            self.srcPath = str(path)
        elif sender == self.openTgtFile:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.tgtPathLineEdit.setText(str(path))
            self.tgtPath = str(path)
        elif sender == self.openStatsSrcFile:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.statsSrcPathLineEdit.setText(str(path))
            self.statsSrcPath = str(path)
        elif sender == self.openStatsTgtFile:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.statsTgtPathLineEdit.setText(str(path))
            self.statsTgtPath = str(path)
        elif sender == self.sortPathButton:
            path = QFileDialog.getOpenFileName(self, 'Open File', './', 'CSV files (*.csv)')[0]
            self.sortPathLineEdit.setText(str(path))
            self.sortPath = str(path)
        elif sender == self.groupSrcButton:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.groupSrcLineEdit.setText(str(path))
            self.groupSrcPath = str(path)
        elif sender == self.groupTgtButton:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.groupTgtLineEdit.setText(str(path))
            self.groupTgtPath = str(path)
        elif sender == self.segmentSrcButton:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.segmentSrcLineEdit.setText(str(path))
            self.segmentSrcPath = str(path)
        elif sender == self.segmentTgtButton:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.segmentTgtLineEdit.setText(str(path))
            self.segmentTgtPath = str(path)
        elif sender == self.wordStatsSrcButton:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.wordStatsSrcLineEdit.setText(str(path))
            self.wordStatsSrcPath = str(path)
        elif sender == self.wordStatsTgtButton:
            path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
            self.wordStatsTgtLineEdit.setText(str(path))
            self.wordStatsTgtPath = str(path)
        elif sender == self.sortWordPathButton:
            path = QFileDialog.getOpenFileName(self, 'Open File', './', 'CSV files (*.csv)')[0]
            self.sortWordPathLineEdit.setText(str(path))
            self.sortWordPath = str(path)

    def codeConfirm(self):
        code = self.codeShowLabel.text()
        code = code.lower()
        codeType = self.codeTypeBox.currentText()
        self.codeCharLable.setStyleSheet('font-weight:bold;')
        if codeType == 'UTF-8':
            self.codeCharLable.setText(self.converter.dict_utf8_to_char.get(code, "-1"))
        elif codeType == 'Unicode':
            self.codeCharLable.setText(self.converter.dict_unicode_to_char.get(code, "-1"))
        elif codeType == 'Big5':
            self.codeCharLable.setText(self.converter.dict_big5_to_char.get(code, "-1"))
        else:
            self.codeCharLable.setText(self.converter.dict_gbk_to_char.get(code, "-1"))
    
    def pathConfirm(self):
        sender = self.sender()
        if sender == self.pathButton:
            if os.path.exists(self.srcPath):
                self.converter.decodeFile(self.srcPath, self.tgtPath)
                self.pathLabel.setText("Done")
                self.pathLabel.setStyleSheet("font-weight:bold;")
            else:
                self.pathLabel.setText("Error")
                self.pathLabel.setStyleSheet("color:red;font-weight:bold;")
        elif sender == self.statsPathButton:
            if os.path.exists(self.statsSrcPath):
                self.counter.countFile(self.statsSrcPath, self.statsTgtPath)
                self.statsPathLabel.setText("Done")
                self.statsPathLabel.setStyleSheet("font-weight:bold;")
            else:
                self.statsPathLabel.setText("Error")
                self.statsPathLabel.setStyleSheet("color:red;font-weight:bold;")
        elif sender == self.sortConfirmButton:
            if os.path.exists(self.sortPath):
                self.counter.sortBy(self.sortPath, mode=self.sortTypeComboBox.currentText(), reverse=self.reverseCheckBox.isChecked())
                self.sortConfirmLabel.setText("Done")
                self.sortConfirmLabel.setStyleSheet("font-weight:bold;")
            else:
                self.sortConfirmLabel.setText("Error")
                self.sortConfirmLabel.setStyleSheet("color:red;font-weight:bold;")
        elif sender == self.groupConfirmButton:
            if os.path.exists(self.groupSrcPath):
                self.counter.groupBy(self.groupSrcPath, self.groupTgtPath)
                self.groupConfirmLabel.setText("Done")
                self.groupConfirmLabel.setStyleSheet("font-weight:bold;")
            else:
                self.groupConfirmLabel.setText("Error")
                self.groupConfirmLabel.setStyleSheet("color:red;font-weight:bold;")
        elif sender == self.segmentConfirmButton:
            if os.path.exists(self.segmentSrcPath):
                self.extractor.segment(self.segmentSrcPath, self.segmentTgtPath)
                self.segmentConfirmLabel.setText("Done")
                self.segmentConfirmLabel.setStyleSheet("font-weight:bold;")
            else:
                self.segmentConfirmLabel.setText("Error")
                self.segmentConfirmLabel.setStyleSheet("color:red;font-weight:bold;")
        elif sender == self.wordStatsConfirmButton:
            if os.path.exists(self.wordStatsSrcPath):
                self.extractor.countSegmentedFile(self.wordStatsSrcPath, self.wordStatsTgtPath)
                self.wordStatsConfirmLabel.setText("Done")
                self.wordStatsConfirmLabel.setStyleSheet("font-weight:bold;")
            else:
                self.wordStatsConfirmLabel.setText("Error")
                self.wordStatsConfirmLabel.setStyleSheet("color:red;font-weight:bold;")
        elif sender == self.sortWordConfirmButton:
            if os.path.exists(self.sortWordPath):
                self.extractor.sortBy(self.sortWordPath, mode=self.sortWordTypeComboBox.currentText(), reverse=self.reverseWordCheckBox.isChecked())
                self.sortWordConfirmLabel.setText("Done")
                self.sortWordConfirmLabel.setStyleSheet("font-weight:bold;")
            else:
                self.sortWordConfirmLabel.setText("Error")
                self.sortWordConfirmLabel.setStyleSheet("color:red;font-weight:bold;")