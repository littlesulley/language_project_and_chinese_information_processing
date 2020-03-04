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
from pypinyin import pinyin, lazy_pinyin, Style
from PyQt5.Qt import *


class Window(QMainWindow):
    def __init__(self, converter):
        super().__init__()
        self.init()
        self.windowCenter()
        self.converter = converter
    
    def init(self):
        self.setFixedSize(900, 600)
        self.setWindowTitle('Chinese Language Processor')
        self.setWindowIcon(QIcon('./resource/emiya.jpg'))
        exeIcon = QSystemTrayIcon(self)
        exeIcon.setIcon(QIcon('./resource/emiya.jpg'))
        exeIcon.show()

        # 汉字转编码
        self.label4 = QLabel(self)
        self.label4.setText('汉字转编码')
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
        self.label4.setText('编码转汉字')
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
        self.label4.setText('笔画转汉字')
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
        self.label4.setText('转换文件夹下的文件编码')
        self.label4.resize(300, 20)
        self.label4.move(250, 350)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setStyleSheet('font-size:15px;font-weight:bold;font-family:Source Code Pro;')

        self.srcPath = ""
        self.tgtPath = ""

        openSrcFile = QPushButton('Open Source Folder', self)
        openSrcFile.clicked.connect(self.srcPathDialog)
        openSrcFile.move(100, 400)
        openSrcFile.resize(200, 30)

        self.srcPathlineEdit = QLineEdit(self)
        self.srcPathlineEdit.setObjectName("filePathlineEdit")
        self.srcPathlineEdit.setPlaceholderText('Source folder path')
        self.srcPathlineEdit.move(310, 400)
        self.srcPathlineEdit.resize(260, 30)

        openTgtFile = QPushButton('Open Target Folder', self)
        openTgtFile.clicked.connect(self.tgtPathDialog)
        openTgtFile.move(100, 440)
        openTgtFile.resize(200, 30)

        self.tgtPathlineEdit = QLineEdit(self)
        self.tgtPathlineEdit.setObjectName("filePathlineEdit")
        self.tgtPathlineEdit.setPlaceholderText('Target folder path')
        self.tgtPathlineEdit.move(310, 440)
        self.tgtPathlineEdit.resize(260, 30)

        self.pathButton = QPushButton('Confirm', self)
        self.pathButton.move(600, 400)
        self.pathButton.resize(100, 30)
        self.pathButton.clicked.connect(self.pathConfirm)

        self.pathLabel = QLabel(self)
        self.pathLabel.setAlignment(Qt.AlignCenter)
        self.pathLabel.move(600, 440)
        self.pathLabel.resize(100, 30)
        self.pathLabel.setStyleSheet("color:red;font-weight:bold;")

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

    def srcPathDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.srcPathlineEdit.setText(str(path))
        self.srcPath = str(path)

    def tgtPathDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.tgtPathlineEdit.setText(str(path))
        self.tgtPath = str(path)
        

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
        if os.path.exists(self.srcPath) and os.path.exists(self.tgtPath):
            self.converter.decodeFile(self.srcPath, self.tgtPath)
            self.pathLabel.setText("Done")
            self.pathLabel.setStyleSheet("font-weight:bold;")
        else:
            self.pathLabel.setText("Error")
            self.pathLabel.setStyleSheet("color:red;font-weight:bold;")