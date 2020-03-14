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
import itertools, string
import jieba
from pypinyin import pinyin, lazy_pinyin, Style
from PyQt5.Qt import *

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)  #定义一个发送str的信号
    def write(self, text):
        self.textWritten.emit(str(text))

class subWindow(QWidget):
    def __init__(self, parent=None):
        super(subWindow, self).__init__(parent, Window)

class Window(QMainWindow):
    def __init__(self, converter, counter, extractor):
        super().__init__()
        self.init()
        self.windowCenter()
        self.converter = converter
        self.counter = counter 
        self.extractor = extractor
    
    def init(self):
        # 设置窗口大小、标题
        self.setWindowTitle('Chinese Language Processor')
        self.setWindowIcon(QIcon('./resource/emiya.jpg'))
        self.resize(600, 400)
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.resize(580, 340)

        centreWidget = QWidget(self)
        self.setCentralWidget(centreWidget)
        layout = QVBoxLayout()
        layout.addWidget(self.textBrowser)
        centreWidget.setLayout(layout)

        # 重定向输出到textBrowser
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)

        # 设置菜单
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&文件')
        self.charMenu = menubar.addMenu('&汉字')
        self.statMenu = menubar.addMenu('&统计')
        self.corpusMenu = menubar.addMenu('&语料库')
        self.parsingMenu = menubar.addMenu('&语法分析')
        self.helpMenu = menubar.addMenu('&帮助')

        # 构造菜单
        self.constructFileMenu(self.fileMenu)
        self.constructCharMenu(self.charMenu)
        self.constructStatMenu(self.statMenu)
        self.constructCorpusMenu(self.corpusMenu)
        self.constructParsingMenu(self.parsingMenu)
        self.constructHelpMenu(self.helpMenu)

        self.show()
    
    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def constructFileMenu(self, fileMenu):
        # 文件编码转换
        self.openFileAction = QAction('编码转换', self)
        self.openFileAction.setShortcut('Ctrl+E')
        self.openFileAction.setStatusTip('转换文件夹下所有文件编码')
        self.openFileAction.triggered.connect(self.openConvertDialog)
        fileMenu.addAction(self.openFileAction)

        # 退出
        self.quitAction = QAction('退出', self)
        self.quitAction.setShortcut('Alt+F4')
        self.quitAction.setStatusTip('退出')
        self.quitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(self.quitAction)

    def constructCharMenu(self, charMenu):
        # 汉字转编码
        self.charToCodeAction = QAction('汉字转编码', self)
        self.charToCodeAction.setShortcut('Alt+C')
        self.charToCodeAction.setStatusTip('汉字转换为编码、笔画、拼音')
        self.charToCodeAction.triggered.connect(self.openCharToCodeDialog)
        charMenu.addAction(self.charToCodeAction)

        # 编码转汉字
        self.codeToCharAction = QAction('编码转汉字', self)
        self.codeToCharAction.setShortcut('Alt+W')
        self.codeToCharAction.setStatusTip('输入编码与编码集，给出汉字')
        self.codeToCharAction.triggered.connect(self.openCodeToCharDialog)
        charMenu.addAction(self.codeToCharAction)

        # 笔画转汉字
        self.strokeToCharAction = QAction('笔画转汉字', self)
        self.strokeToCharAction.setShortcut('Alt+E')
        self.strokeToCharAction.setStatusTip('输入笔画，给出所有可能的汉字')
        self.strokeToCharAction.triggered.connect(self.openStrokeToCharDialog)
        charMenu.addAction(self.strokeToCharAction)

    def constructStatMenu(self, statMenu):
        # 分词
        self.segmentAction = QAction('分词', self)
        self.segmentAction.setShortcut('Alt+T')
        self.segmentAction.setStatusTip('分词文件或文件夹下所有文件')
        self.segmentAction.triggered.connect(self.openSegmentDialog)
        statMenu.addAction(self.segmentAction)

        # 统计数据
        self.infoMenu = QMenu('统计', self)
        statMenu.addMenu(self.infoMenu)

        # 按字统计
        self.charInfoAction = QAction('统计字信息', self)
        self.charInfoAction.setStatusTip('以字符为单位统计文件或文件夹下所有文件的数据')
        self.charInfoAction.triggered.connect(self.openCharInfoDialog)
        self.infoMenu.addAction(self.charInfoAction)

        # 按词统计
        self.wordInfoAction = QAction('统计词信息', self)
        self.wordInfoAction.setStatusTip('以词为单位统计文件或文件夹下所有文件的数据')
        self.wordInfoAction.triggered.connect(self.openWordInfoDialog)
        self.infoMenu.addAction(self.wordInfoAction)

        # 数据排序   
        self.sortMenu = QMenu('排序', self)
        statMenu.addMenu(self.sortMenu)

        # 字文件排序
        self.charSortAction = QAction('字符统计排序', self)
        self.charSortAction.setStatusTip('对单个.csv字符统计文件的数据排序')
        self.charSortAction.triggered.connect(self.openCharSortDialog)
        self.sortMenu.addAction(self.charSortAction)

        # 词文件排序
        self.wordSortAction = QAction('词统计排序', self)
        self.wordSortAction.setStatusTip('对单个.csv词统计文件的数据排序')
        self.wordSortAction.triggered.connect(self.openWordSortDialog)
        self.sortMenu.addAction(self.wordSortAction)

    def constructCorpusMenu(self, corpusMenu):
        pass

    def constructParsingMenu(self, parsingMenu):
        pass

    def constructHelpMenu(self, helpMenu):
        # 关于
        self.aboutAction = QAction('关于', self)
        self.aboutAction.setShortcut('Alt+A')
        self.aboutAction.setStatusTip('关于本程序')
        self.aboutAction.triggered.connect(self.openAboutDialog)
        helpMenu.addAction(self.aboutAction)

        # 使用说明
        self.instructionAction = QAction('使用说明', self)
        self.instructionAction.setShortcut('Alt+I')
        self.instructionAction.setStatusTip('本程序的使用说明')
        self.instructionAction.triggered.connect(self.openHelpDialog)
        helpMenu.addAction(self.instructionAction)
    
    def openConvertDialog(self):
        widget = QDialog()
        widget.setWindowTitle('分词')
        widget.resize(600, 100)

        layout = QGridLayout()

        self.srcPath = ""
        self.tgtPath = ""

        self.openSrcFile = QPushButton('打开源文件夹', self)
        self.openSrcFile.setToolTip('待转换的文件夹目录')
        self.openSrcFile.clicked.connect(self.srcFileDialog)
        self.openSrcFile.resize(100, 30)

        self.srcPathLineEdit = QLineEdit(self)
        self.srcPathLineEdit.setObjectName("filePathlineEdit")
        self.srcPathLineEdit.resize(200, 30)

        self.openTgtFile = QPushButton('打开目标文件夹', self)
        self.openTgtFile.setToolTip('转换后的文件夹目录')
        self.openTgtFile.clicked.connect(self.tgtFileDialog)
        self.openTgtFile.resize(100, 30)

        self.tgtPathLineEdit = QLineEdit(self)
        self.tgtPathLineEdit.setObjectName("filePathlineEdit")
        self.tgtPathLineEdit.resize(260, 30)

        self.pathButton = QPushButton('Confirm', self)
        self.pathButton.resize(100, 30)
        self.pathButton.clicked.connect(self.srcPathDialog)

        self.pathLabel = QLabel(self)
        self.pathLabel.resize(50, 30)
        self.pathLabel.setAlignment(Qt.AlignCenter)
        self.pathLabel.setStyleSheet("font-weight:bold;")

        layout.addWidget(self.openSrcFile, 0, 0)
        layout.addWidget(self.srcPathLineEdit, 0, 1)
        layout.addWidget(self.openTgtFile, 1, 0)
        layout.addWidget(self.tgtPathLineEdit, 1, 1)
        layout.addWidget(self.pathButton, 0, 2)
        layout.addWidget(self.pathLabel, 1, 2)

        widget.setLayout(layout)
        widget.exec_()

    def openAboutDialog(self):
        widget = QDialog()
        widget.setFixedSize(600, 400)
        widget.setWindowTitle('关于')

        text = QTextEdit(widget)

        text.setWindowTitle('关于本程序')
        text.resize(580, 380)
        text.move(10, 10)
        text.setReadOnly(True)

        text.insertHtml('1.本项目是北京大学课程<b>语言工程与中文信息处理</b>作业及课设，最终解释权归作者<font color="red">Sulley</font>所有.<br><br>')
        text.insertHtml('2.项目开源在github: https://github.com/littlesulley/language_project_and_chinese_information_processing，可随意clone、修改.<br><br>')
        text.insertHtml('3.本项目基于python3和pyqt5实现，并使用了xlrd，pypinyin，chardet，docx，jieba等python包，在运行前请务必保证满足以上依赖.<br><br>')
        text.insertHtml('4.若对项目内容、代码有任何疑问，可以在github上提issue，我会尽量尽快回复.<br><br>')
        text.insertHtml('5.本项目不一定会更新，请勿催更.')

        widget.exec_()

    def openHelpDialog(self):
        widget = QDialog()
        widget.setFixedSize(600, 400)
        widget.setWindowTitle('关于')

        text = QTextEdit(widget)

        text.setWindowTitle('关于本程序')
        text.resize(580, 380)
        text.move(10, 10)
        text.setReadOnly(True)

        text.insertHtml('本项目主要实现如下功能：（1）文件编码转换；（2）汉字编码转换；（3）文件分词及统计；（4）语料库功能；（5）语法分析。各功能介绍及使用说明如下：<br><br>')
        text.insertHtml('（1）文件编码功能实现了将文件夹下的所有.txt和.docx文件转换为.txt文件，并且统一编码为utf8。点击第一个菜单“文件”，选择“编码转换”，打开需要转换编码的文件夹即可。注意，本功能只支持打开文件夹而非文件，编码转换结束后会按照<b>源文件夹的层次结构</b>将转换后的文件存放到目标文件夹中.<br><br>')
        text.insertHtml('（2）汉字编码转换实现了给定汉字，输出汉字的各编码、笔画和拼音的功能；同时也支持将编码转换为汉字；支持输入笔画数，输出所有可能的汉字。点击“汉字”菜单选择想要的功能即可.<br><br>')
        text.insertHtml('（3）文件分词及统计功能完成了下述功能：对文件夹下所有文件分词（请保证所有文件均为未分词文件）；对文件夹下所有文件统计字符（或词）级别信息，包括频次、编码、拼音、笔画，并对每个文件输出一个.csv文件，若是词级别信息，请保证所有文件均已分词；对得到的单个.csv文件排序，排序标准有按频次、按编码、按拼音、按笔画，输出一个排序的.csv文件。点击“统计”菜单选择想要的功能.<br><br>')
        text.insertHtml('（4）')
        text.insertHtml('（5）')

        widget.exec_()

    def openCharToCodeDialog(self):
        widget = QDialog()
        widget.setWindowTitle('汉字转编码、拼音、笔画')
        widget.resize(600, 140)

        layout = QGridLayout()

        self.charInputButton = QPushButton('输入汉字', widget)
        self.charInputButton.setToolTip('请输入<b>一个</b>汉字')
        self.charInputButton.resize(100, 30)
        self.charInputButton.clicked.connect(self.charToCodeDialog)

        self.charShowLabel = QLabel('', widget)
        self.charShowLabel.resize(50, 30)
        self.charShowLabel.setStyleSheet('font-weight:bold;')

        self.charUTFLabel = QLabel('UTF8:', widget)
        self.charUTFShowLabel = QLabel('', widget)
        self.charUTFShowLabel.resize(90,30)
        self.charUTFShowLabel.setStyleSheet('font-weight:bold;')

        self.charUnicodeLabel = QLabel('Unicode:', widget)
        self.charUnicodeShowLabel = QLabel('', widget)
        self.charUnicodeShowLabel.resize(90,30)
        self.charUnicodeShowLabel.setStyleSheet('font-weight:bold;')

        self.charBig5Label = QLabel('Big5:', widget)
        self.charBig5ShowLabel = QLabel('', widget)
        self.charBig5ShowLabel.resize(90,30)
        self.charBig5ShowLabel.setStyleSheet('font-weight:bold;')

        self.charGBKLabel = QLabel('GBK:', widget)
        self.charGBKShowLabel = QLabel('', widget)
        self.charGBKShowLabel.resize(90,30)
        self.charGBKShowLabel.setStyleSheet('font-weight:bold;')


        self.charPinyinLabel = QLabel('pinyin:', widget)
        self.charPinyinShowLabel = QLabel('', widget)
        self.charPinyinShowLabel.resize(90,60)
        self.charPinyinShowLabel.setStyleSheet('font-weight:bold;')

        self.charStrokeLabel = QLabel('Stroke:', widget)
        self.charStrokeShowLabel = QLabel('', widget)
        self.charStrokeShowLabel.resize(90,30)
        self.charStrokeShowLabel.setStyleSheet('font-weight:bold;')

        layout.addWidget(self.charInputButton, 0, 0)
        layout.addWidget(self.charShowLabel, 1, 0, Qt.AlignCenter)
        layout.addWidget(self.charUTFLabel, 0, 1)
        layout.addWidget(self.charUTFShowLabel, 0, 2)
        layout.addWidget(self.charUnicodeLabel, 0, 3)
        layout.addWidget(self.charUnicodeShowLabel, 0, 4)
        layout.addWidget(self.charBig5Label, 0, 5)
        layout.addWidget(self.charBig5ShowLabel, 0, 6)
        layout.addWidget(self.charGBKLabel, 1, 1)
        layout.addWidget(self.charGBKShowLabel, 1, 2)
        layout.addWidget(self.charPinyinLabel, 1, 3)
        layout.addWidget(self.charPinyinShowLabel, 1, 4)
        layout.addWidget(self.charStrokeLabel, 1, 5)
        layout.addWidget(self.charStrokeShowLabel, 1, 6)

        widget.setLayout(layout)
        widget.exec_()

    def openCodeToCharDialog(self):
        widget = QDialog()
        widget.setWindowTitle('编码转汉字')
        widget.resize(400, 100)

        layout = QGridLayout()

        self.codeInputButton = QPushButton('输入编码', widget)
        self.codeInputButton.setToolTip('请输入编码，大小写均可')
        self.codeInputButton.resize(100, 30)
        self.codeInputButton.clicked.connect(self.codeToCharDialog)

        self.codeShowLabel = QLabel('', widget)
        self.codeShowLabel.setStyleSheet('font-weight:bold;')
        self.codeTypeLabel = QLabel('Code Type:', widget)

        choices = ['UTF-8', 'Unicode', 'Big5', 'GBK']
        self.codeTypeBox = QComboBox(widget)
        self.codeTypeBox.addItems(choices)
        self.codeTypeBox.resize(50, 50)
        
        self.codeConfirmButton = QPushButton('Confirm', widget)
        self.codeConfirmButton.clicked.connect(self.codeConfirm)

        self.codeCharLable = QLabel('', widget)

        layout.addWidget(self.codeInputButton, 0, 0)
        layout.addWidget(self.codeShowLabel, 0, 1)
        layout.addWidget(self.codeTypeLabel, 0, 2)
        layout.addWidget(self.codeTypeBox, 0, 3)
        layout.addWidget(self.codeConfirmButton, 0, 4)
        layout.addWidget(self.codeCharLable, 0, 5)


        widget.setLayout(layout)
        widget.exec_()

    def openStrokeToCharDialog(self):
        widget = QDialog()
        widget.setWindowTitle('笔画转汉字')
        widget.resize(200, 100)

        layout = QGridLayout()

        self.strokeInputButton = QPushButton('输入笔画', widget)
        self.strokeInputButton.setToolTip('请输入一个正整数')
        self.strokeInputButton.resize(100, 30)
        self.strokeInputButton.clicked.connect(self.strokeToCharDialog)

        self.strokeShowLabel = QLabel('', widget)
        self.strokeCharShowLabel = QLabel('Characters:', widget)
        self.strokeCharBox = QComboBox(self)

        layout.addWidget(self.strokeInputButton, 0, 0)
        layout.addWidget(self.strokeShowLabel, 0, 1)
        layout.addWidget(self.strokeCharShowLabel, 0, 2)
        layout.addWidget(self.strokeCharBox, 0, 3)

        widget.setLayout(layout)
        widget.exec_()

    def openCharInfoDialog(self):
        widget = QDialog()
        widget.setWindowTitle('统计字符信息')
        widget.resize(600, 100)

        layout = QGridLayout()

        self.statsSrcPath = ''
        self.statsTgtPath = ''

        self.openStatsSrcFile = QPushButton('打开源文件夹', self)
        self.openStatsSrcFile.setToolTip('待统计字符信息文件夹目录')
        self.openStatsSrcFile.clicked.connect(self.statsSrcFileDialog)
        self.openStatsSrcFile.resize(200, 30)

        self.statsSrcPathLineEdit = QLineEdit(self)
        self.statsSrcPathLineEdit.setObjectName('filePathlineEdit')
        self.statsSrcPathLineEdit.resize(260, 30)

        self.openStatsTgtFile = QPushButton('打开目标文件夹', self)
        self.openStatsTgtFile.setToolTip('统计后存放信息的目标文件夹目录')
        self.openStatsTgtFile.clicked.connect(self.statsTgtFileDialog)
        self.openStatsTgtFile.resize(200, 30)

        self.statsTgtPathLineEdit = QLineEdit(self)
        self.statsTgtPathLineEdit.setObjectName('filePathlineEdit')
        self.statsTgtPathLineEdit.resize(260, 30)

        self.statsPathButton = QPushButton('Confirm', self)
        self.statsPathButton.resize(100, 30)
        self.statsPathButton.clicked.connect(self.statsPathDialog)

        self.statsPathLabel = QLabel(self)
        self.statsPathLabel.setAlignment(Qt.AlignCenter)
        self.statsPathLabel.resize(100, 30)
        self.statsPathLabel.setStyleSheet("color:red;font-weight:bold;")

        layout.addWidget(self.openStatsSrcFile, 0, 0)
        layout.addWidget(self.statsSrcPathLineEdit, 0, 1)
        layout.addWidget(self.openStatsTgtFile, 1, 0)
        layout.addWidget(self.statsTgtPathLineEdit, 1, 1)
        layout.addWidget(self.statsPathButton, 0, 2)
        layout.addWidget(self.statsPathLabel, 1, 2)

        widget.setLayout(layout)
        widget.exec_()
    
    def openWordInfoDialog(self):
        widget = QDialog()
        widget.setWindowTitle('统计词信息')
        widget.resize(600, 100)

        layout = QGridLayout()

        self.wordStatsSrcPath = ''
        self.wordStatsTgtPath = ''

        self.wordStatsSrcButton = QPushButton('打开源文件夹', self)
        self.wordStatsSrcButton.setToolTip('待统计已分词源文件夹目录')
        self.wordStatsSrcButton.clicked.connect(self.wordStatsSrcDialog)
        self.wordStatsSrcButton.resize(200, 30)

        self.wordStatsSrcLineEdit = QLineEdit(self)
        self.wordStatsSrcLineEdit.setObjectName('filePathlineEdit')
        self.wordStatsSrcLineEdit.resize(260, 30)

        self.wordStatsTgtButton = QPushButton('打开目标文件夹', self)
        self.wordStatsTgtButton.setToolTip('统计后存放信息的目标文件夹目录')
        self.wordStatsTgtButton.clicked.connect(self.wordStatsTgtDialog)
        self.wordStatsTgtButton.resize(200, 30)

        self.wordStatsTgtLineEdit = QLineEdit(self)
        self.wordStatsTgtLineEdit.setObjectName('filePathlineEdit')
        self.wordStatsTgtLineEdit.resize(260, 30)

        self.wordStatsConfirmButton = QPushButton('Confirm', self)
        self.wordStatsConfirmButton.resize(100, 30)
        self.wordStatsConfirmButton.clicked.connect(self.wordStatsPathDialog)

        self.wordStatsConfirmLabel = QLabel(self)
        self.wordStatsConfirmLabel.setAlignment(Qt.AlignCenter)
        self.wordStatsConfirmLabel.resize(100, 30)
        self.wordStatsConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        layout.addWidget(self.wordStatsSrcButton, 0, 0)
        layout.addWidget(self.wordStatsSrcLineEdit, 0, 1)
        layout.addWidget(self.wordStatsTgtButton, 1, 0)
        layout.addWidget(self.wordStatsTgtLineEdit, 1, 1)
        layout.addWidget(self.wordStatsConfirmButton, 0, 2)
        layout.addWidget(self.wordStatsConfirmLabel, 1, 2)

        widget.setLayout(layout)
        widget.exec_()

    def openSegmentDialog(self):
        widget = QDialog()
        widget.setWindowTitle('分词')
        widget.resize(600, 100)

        layout = QGridLayout()

        self.segmentSrcPath = ''
        self.segmentTgtPath = ''

        self.segmentSrcButton = QPushButton('打开源文件夹', self)
        self.segmentSrcButton.setToolTip('输入待分词源文件夹目录')
        self.segmentSrcButton.clicked.connect(self.segmentSrcDialog)
        self.segmentSrcButton.resize(200, 30)

        self.segmentSrcLineEdit = QLineEdit(self)
        self.segmentSrcLineEdit.setObjectName('filePathlineEdit')
        self.segmentSrcLineEdit.resize(260, 30)

        self.segmentTgtButton = QPushButton('打开目标文件夹', self)
        self.segmentTgtButton.setToolTip('输入分词后目标文件夹目录')
        self.segmentTgtButton.clicked.connect(self.segmentTgtDialog)
        self.segmentTgtButton.resize(200, 30)

        self.segmentTgtLineEdit = QLineEdit(self)
        self.segmentTgtLineEdit.setObjectName('filePathlineEdit')
        self.segmentTgtLineEdit.resize(260, 30)

        self.segmentConfirmButton = QPushButton('Confirm', self)
        self.segmentConfirmButton.resize(100, 30)
        self.segmentConfirmButton.clicked.connect(self.segmentPathDialog)

        self.segmentConfirmLabel = QLabel(self)
        self.segmentConfirmLabel.setAlignment(Qt.AlignCenter)
        self.segmentConfirmLabel.resize(100, 30)
        self.segmentConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        layout.addWidget(self.segmentSrcButton, 0, 0)
        layout.addWidget(self.segmentSrcLineEdit, 0, 1)
        layout.addWidget(self.segmentTgtButton, 1, 0)
        layout.addWidget(self.segmentTgtLineEdit, 1, 1)
        layout.addWidget(self.segmentConfirmButton, 0, 2)
        layout.addWidget(self.segmentConfirmLabel, 1, 2)

        widget.setLayout(layout)
        widget.exec_()

    def openCharSortDialog(self):
        widget = QDialog()
        widget.setWindowTitle('字统计文件排序')
        widget.resize(900, 100)

        layout = QGridLayout()

        self.sortPathButton = QPushButton('打开.csv字符信息文件', self)
        self.sortPathButton.setToolTip('输入已统计的.csv文件目录')
        self.sortPathButton.clicked.connect(self.sortFileDialog)
        self.sortPathButton.resize(100, 30)

        self.sortPathLineEdit = QLineEdit(self)
        self.sortPathLineEdit.setObjectName('filePathlineEdit')
        self.sortPathLineEdit.resize(200, 30)

        self.sortPath = ''

        self.sortTypeLabel = QLabel('排序标准: ', self)
        self.sortTypeLabel.resize(60, 30)

        self.sortTypeComboBox = QComboBox(self)
        sortChoices = ['frequency', 'unicode', 'utf8', 'gbk', 'big5', 'pinyin', 'stroke']
        self.sortTypeComboBox.addItems(sortChoices)
        self.sortTypeComboBox.resize(50, 30)

        self.sortReverseLabel = QLabel('逆序: ', self)
        self.sortReverseLabel.resize(50, 30)

        self.reverseCheckBox = QCheckBox('Yes', self)

        self.sortConfirmButton = QPushButton('Confirm', self)
        self.sortConfirmButton.resize(50, 30)
        self.sortConfirmButton.clicked.connect(self.sortPathDialog)

        self.sortConfirmLabel = QLabel(self)
        self.sortConfirmLabel.setAlignment(Qt.AlignCenter)
        self.sortConfirmLabel.resize(50, 30)
        self.sortConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        layout.addWidget(self.sortPathButton, 0, 0)
        layout.addWidget(self.sortPathLineEdit, 0, 1)
        layout.addWidget(self.sortTypeLabel, 0, 2)
        layout.addWidget(self.sortTypeComboBox, 0, 3)
        layout.addWidget(self.sortReverseLabel, 0, 4)
        layout.addWidget(self.reverseCheckBox, 0, 5)
        layout.addWidget(self.sortConfirmButton, 0, 6)
        layout.addWidget(self.sortConfirmLabel, 0, 7)

        widget.setLayout(layout)
        widget.exec_()

    def openWordSortDialog(self):
        widget = QDialog()
        widget.setWindowTitle('词统计文件排序')
        widget.resize(900, 100)

        layout = QGridLayout()


        self.sortWordPathButton = QPushButton('打开.csv字符信息文件', self)
        self.sortWordPathButton.setToolTip('输入已统计词的.csv文件目录')
        self.sortWordPathButton.clicked.connect(self.sortWordFileDialog)
        self.sortWordPathButton.resize(100, 30)

        self.sortWordPathLineEdit = QLineEdit(self)
        self.sortWordPathLineEdit.setObjectName('filePathlineEdit')
        self.sortWordPathLineEdit.resize(200, 30)

        self.sortWordPath = ''

        self.sortWordTypeLabel = QLabel('排序标准: ', self)
        self.sortWordTypeLabel.resize(60, 30)

        self.sortWordTypeComboBox = QComboBox(self)
        sortChoices = ['frequency', 'unicode', 'utf8', 'gbk', 'big5', 'pinyin', 'stroke']
        self.sortWordTypeComboBox.addItems(sortChoices)
        self.sortWordTypeComboBox.resize(60, 30)

        self.sortWordReverseLabel = QLabel('逆序: ', self)
        self.sortWordReverseLabel.resize(50, 30)

        self.reverseWordCheckBox = QCheckBox('Yes', self)

        self.sortWordConfirmButton = QPushButton('Confirm', self)
        self.sortWordConfirmButton.resize(50, 30)
        self.sortWordConfirmButton.clicked.connect(self.sortWordPathDialog)

        self.sortWordConfirmLabel = QLabel(self)
        self.sortWordConfirmLabel.resize(50, 30)
        self.sortWordConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

        layout.addWidget(self.sortWordPathButton, 0, 0)
        layout.addWidget(self.sortWordPathLineEdit, 0, 1)
        layout.addWidget(self.sortWordTypeLabel, 0, 2)
        layout.addWidget(self.sortWordTypeComboBox, 0, 3)
        layout.addWidget(self.sortWordReverseLabel, 0, 4)
        layout.addWidget(self.reverseWordCheckBox, 0, 5)
        layout.addWidget(self.sortWordConfirmButton, 0, 6)
        layout.addWidget(self.sortWordConfirmLabel, 0, 7)

        widget.setLayout(layout)
        widget.exec_()

    def windowCenter(self):
        screenSize = QDesktopWidget().screenGeometry()
        windowSize = self.geometry()
        newLeft = (screenSize.width() - windowSize.width()) / 2
        newTop = (screenSize.height() - windowSize.height()) / 2
        self.move(newLeft, newTop)

    def charToCodeDialog(self):
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

    def codeToCharDialog(self):
        code, ok = QInputDialog.getText(self, '输入编码', '请输入编码：')
        if ok:
            self.codeShowLabel.setText(code)
            self.codeShowLabel.setStyleSheet('font-weight:bold;')
    
    def strokeToCharDialog(self):
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
    
    def srcFileDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.srcPathLineEdit.setText(str(path))
        self.srcPath = str(path)
    
    def tgtFileDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.tgtPathLineEdit.setText(str(path))
        self.tgtPath = str(path)
    
    def statsSrcFileDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.statsSrcPathLineEdit.setText(str(path))
        self.statsSrcPath = str(path)

    def statsTgtFileDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.statsTgtPathLineEdit.setText(str(path))
        self.statsTgtPath = str(path)

    def sortFileDialog(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', './', 'CSV files (*.csv)')[0]
        self.sortPathLineEdit.setText(str(path))
        self.sortPath = str(path)
    
    def groupSrcDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.groupSrcLineEdit.setText(str(path))
        self.groupSrcPath = str(path)

    def groupTgtDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.groupTgtLineEdit.setText(str(path))
        self.groupTgtPath = str(path)

    def segmentSrcDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.segmentSrcLineEdit.setText(str(path))
        self.segmentSrcPath = str(path)
    
    def segmentTgtDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.segmentTgtLineEdit.setText(str(path))
        self.segmentTgtPath = str(path)

    def wordStatsSrcDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.wordStatsSrcLineEdit.setText(str(path))
        self.wordStatsSrcPath = str(path)

    def wordStatsTgtDialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open Directory', './')
        self.wordStatsTgtLineEdit.setText(str(path))
        self.wordStatsTgtPath = str(path)

    def sortWordFileDialog(self):
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

    def srcPathDialog(self):
        if os.path.exists(self.srcPath):
            self.converter.decodeFile(self.srcPath, self.tgtPath)
            self.pathLabel.setText("Done")
            self.pathLabel.setStyleSheet("font-weight:bold;")
        else:
            self.pathLabel.setText("Error")
            self.pathLabel.setStyleSheet("color:red;font-weight:bold;")
    
    def statsPathDialog(self):
        if os.path.exists(self.statsSrcPath):
            self.counter.countFile(self.statsSrcPath, self.statsTgtPath)
            self.statsPathLabel.setText("Done")
            self.statsPathLabel.setStyleSheet("font-weight:bold;")
        else:
            self.statsPathLabel.setText("Error")
            self.statsPathLabel.setStyleSheet("color:red;font-weight:bold;")

    def sortPathDialog(self):
        if os.path.exists(self.sortPath):
            self.counter.sortBy(self.sortPath, mode=self.sortTypeComboBox.currentText(), reverse=self.reverseCheckBox.isChecked())
            self.sortConfirmLabel.setText("Done")
            self.sortConfirmLabel.setStyleSheet("font-weight:bold;")
        else:
            self.sortConfirmLabel.setText("Error")
            self.sortConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

    def groupPathDialog(self):
        if os.path.exists(self.groupSrcPath):
            self.counter.groupBy(self.groupSrcPath, self.groupTgtPath)
            self.groupConfirmLabel.setText("Done")
            self.groupConfirmLabel.setStyleSheet("font-weight:bold;")
        else:
            self.groupConfirmLabel.setText("Error")
            self.groupConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

    def segmentPathDialog(self):
        if os.path.exists(self.segmentSrcPath):
            self.extractor.segment(self.segmentSrcPath, self.segmentTgtPath)
            self.segmentConfirmLabel.setText("Done")
            self.segmentConfirmLabel.setStyleSheet("font-weight:bold;")
        else:
            self.segmentConfirmLabel.setText("Error")
            self.segmentConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

    def wordStatsPathDialog(self):
        if os.path.exists(self.wordStatsSrcPath):
            self.extractor.countSegmentedFile(self.wordStatsSrcPath, self.wordStatsTgtPath)
            self.wordStatsConfirmLabel.setText("Done")
            self.wordStatsConfirmLabel.setStyleSheet("font-weight:bold;")
        else:
            self.wordStatsConfirmLabel.setText("Error")
            self.wordStatsConfirmLabel.setStyleSheet("color:red;font-weight:bold;")

    def sortWordPathDialog(self):
        if os.path.exists(self.sortWordPath):
            self.extractor.sortBy(self.sortWordPath, mode=self.sortWordTypeComboBox.currentText(), reverse=self.reverseWordCheckBox.isChecked())
            self.sortWordConfirmLabel.setText("Done")
            self.sortWordConfirmLabel.setStyleSheet("font-weight:bold;")
        else:
            self.sortWordConfirmLabel.setText("Error")
            self.sortWordConfirmLabel.setStyleSheet("color:red;font-weight:bold;")