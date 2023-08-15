# 导入相关PyQt5模块
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
# 导入必要内置库
import sys
import os
# 导入界面相关的模块
from UI import Ui_about,Ui_select
import Ui_main
# 导入自定义模块
from fileCore import *
from wordBook import WordsBook
from testCore import TestCore

def showMainPage()->None:
    '''显示主页面'''
    subWin=QWidget(window)
    ui=Ui_main.Ui_Form()
    ui.setupUi(subWin)
    window.setWindowTitle("背单词小程序")
    
    subWin.show()

    ui.label.setText(f"词汇表单词数量:{len(readWordsData(wordsFilePath))}")
    '''绑定事件'''
    ui.pushButton_4.clicked.connect(wordsBook.browseWordsDict)
    ui.pushButton_3.clicked.connect(vBook.browseWordsDict)
    ui.pushButton_2.clicked.connect(showSelectTestModePage)
    ui.pushButton_1.clicked.connect(showAboutPage)

def showSelectTestModePage()->None:
    '''测验单词'''
    # 显示选择测试模式界面
    subWin=QWidget(window)
    ui=Ui_select.Ui_Form()
    ui.setupUi(subWin)
    window.setWindowTitle("选择")
    subWin.show()

    ui.backbutton.clicked.connect(showMainPage)
    ui.pushButton.clicked.connect(testcore.CETest)
    ui.pushButton_2.clicked.connect(testcore.ECTest)

def showAboutPage()->None:
    '''关于页面'''
    global window
    subWin=QWidget(window)

    ui=Ui_about.Ui_Form()
    ui.setupUi(subWin)
    subWin.show()
    window.setWindowTitle("关于")

    ui.backbutton.clicked.connect(showMainPage)

if __name__=="__main__":
    '''创建qt应用'''
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) # 设置高分辨率
    app = QApplication(sys.argv)
    '''加载QSS'''
    qssFile=readQSS("style.qss")
    app.setStyleSheet(qssFile)
    '''读取文件'''
    wordsFilePath="words.json" # 单词表文件路径
    vBookFilePath="vbook.json" # 生词本文件路径
    # 判断文件是否存在
    createFile(wordsFilePath,{})
    createFile(vBookFilePath,{})

    '''创建窗口'''
    window=QWidget()
    '''初始化并显示主页面'''
    ui=Ui_main.Ui_Form()
    ui.setupUi(window)
    window.setFixedSize(window.width(), window.height()) # 禁止拉伸窗口大小
    ui.label.setText(f"词汇表单词数量:{len(readWordsData(wordsFilePath))}") # 单词表词数
    window.show()
    '''创建WordsBook实例(单词本和生词本)'''
    wordsBook=WordsBook(window,wordsFilePath,"单词本",showMainPage)
    vBook=WordsBook(window,vBookFilePath,"生词本",showMainPage)
    '''创建测试核心实例'''
    testcore=TestCore(window,wordsFilePath,showSelectTestModePage)
    '''绑定事件'''
    ui.pushButton_4.clicked.connect(wordsBook.browseWordsDict)
    ui.pushButton_3.clicked.connect(vBook.browseWordsDict)
    ui.pushButton_2.clicked.connect(showSelectTestModePage)
    ui.pushButton_1.clicked.connect(showAboutPage)
    
    app.exec_()
    