from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QFont,QStandardItemModel,QStandardItem
import sys
from UI import Ui_main,Ui_show,Ui_about,Ui_dict

def readQSS(filepath:str) -> str:
    '''读取QSS文件'''
    with open(filepath,'r') as file:
        return file.read()

def readWordsData(filepath:str) -> dict:
    '''读取文件'''
    with open(filepath,"r",encoding="utf-8") as file:
        words=eval(file.read())
    return words

def saveWordsData(filepath:str,data:dict) -> None:
    '''读取文件'''
    with open(filepath,"w",encoding="utf-8") as file:
        file.write(str(data))

def showMain():
    '''显示主页面'''
    subWin=QWidget(window)
    ui=Ui_main.Ui_Form()
    ui.setupUi(subWin)
    window.setWindowTitle("背单词小程序")
    
    subWin.show()

    ui.label.setText(f"词汇表单词数量:{length}")
    ui.pushButton_5.setIcon(QIcon("images/memorize.png"))
    ui.pushButton_4.setIcon(QIcon("images/add.png"))
    ui.pushButton_3.setIcon(QIcon("images/dict.png"))
    ui.pushButton_2.setIcon(QIcon("images/test.png"))
    '''绑定事件'''
    ui.pushButton_5.clicked.connect(showWords)
    ui.pushButton_4.clicked.connect(addWord)
    ui.pushButton_3.clicked.connect(showDict)
    ui.pushButton_2.clicked.connect(test)
    ui.pushButton.clicked.connect(showAbout)

def showWords():
    '''显示单词'''
    subWin=QWidget(window)

    ui=Ui_show.Ui_Form()
    ui.setupUi(subWin)
    window.setWindowTitle("记单词")
    subWin.show()
    
    ui.commandLinkButton.clicked.connect(showMain)

    index=0 # 记录目前查看的单词的索引
    word=wordsKeyList[index] # 通过index

    def next1():
        '''记住了'''
        nonlocal index,word

        if index>length: # 已经是最后一个单词，不再继续
            QMessageBox.warning(window,"警告","已经是单词表里的最后一个单词了",QMessageBox.Ok)
            return None
        word=wordsKeyList[index] # 通过index获取当前的单词
        ui.label.setText(f"{word}\n{words[word]}") # 显示当前单词
        
        index+=1 # 索引+1，查看下一个单词
        
    def next2():
        '''加入生词本'''
        nonlocal index,word

        if index>length: # 已经是最后一个单词，不再继续
            QMessageBox.warning(window,"警告","已经是单词表里的最后一个单词了",QMessageBox.Ok)
            return None
        
        word=wordsKeyList[index] # 通过index获取当前的单词

        dictWords[word]=words[word] # 加入生词本
        saveWordsData("dict.json",dictWords)
        ui.label.setText(f"{word}\n{words[word]}") # 显示当前单词
        index+=1 # 索引+1，查看下一个单词
        
    next1()

    ui.pushButton_2.clicked.connect(next1)
    ui.pushButton.clicked.connect(next2)

def addWord():
    '''添加单词'''
    pass

def deleteSelectedRow(tableView,model):
    '''删除选中行'''
    index = tableView.currentIndex()  # 取得当前选中行的index
    word=tableView.currentIndex().data() # 获取选中行的内容
    model.removeRow(index.row())  # 通过index的row()操作得到行数进行删除
    
    dictWords.pop(word) # 在生词本字典中删除该单词
    saveWordsData("dict.json",dictWords) # 写入dict.json

def showDict():
    '''打开生词本'''
    subWin=QWidget(window)
    ui=Ui_dict.Ui_Form()
    ui.setupUi(subWin)
    window.setWindowTitle("生词本")
    
    subWin.show()

    ui.commandLinkButton.clicked.connect(showMain)

    model=QStandardItemModel() # 创建列表模型
    model.setHorizontalHeaderLabels(['单词','释义']) # 设置模型的表头
    ui.tableView.setModel(model) # 给列表视图设置模型
    ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
    ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中整行
    ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中一行
    ui.tableView.setEditTriggers(QTableView.NoEditTriggers) # 不可编辑

    for word in dictWords:
        model.appendRow([QStandardItem(word),QStandardItem(dictWords[word])])

    ui.pushButton_2.clicked.connect(lambda:deleteSelectedRow(ui.tableView,model))

def test():
    '''测验单词'''
    pass

def showAbout():
    '''关于页面'''
    global window
    subWin=QWidget(window)

    ui=Ui_about.Ui_Form()
    ui.setupUi(subWin)
    window.setWindowTitle("关于")
    subWin.show()
    
    ui.label_2.setOpenExternalLinks(True)
    ui.label_4.setOpenExternalLinks(True)
    ui.commandLinkButton.clicked.connect(showMain)

if __name__=="__main__":
    '''创建qt应用'''
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    '''加载QSS'''
    qssFile=readQSS("style.qss")
    app.setStyleSheet(qssFile)
    '''读取文件'''
    words=readWordsData("words.json") # 单词表里的所有单词即中文意思
    length=len(words) # 单词表词数
    wordsKeyList=list(words.keys()) # 只有所有的单词，没有中文意思
    dictWords=readWordsData("dict.json")
    '''创建窗口'''
    window=QWidget()
    window.setWindowIcon(QIcon('images/logo.png'))
    '''显示主页面'''
    ui=Ui_main.Ui_Form()
    ui.setupUi(window)
    window.setWindowTitle("背单词小程序")
    
    window.show()

    ui.label.setText(f"词汇表单词数量:{length}")
    ui.pushButton_5.setIcon(QIcon("images/memorize.png"))
    ui.pushButton_4.setIcon(QIcon("images/add.png"))
    ui.pushButton_3.setIcon(QIcon("images/dict.png"))
    ui.pushButton_2.setIcon(QIcon("images/test.png"))
    '''绑定事件'''
    ui.pushButton_5.clicked.connect(showWords)
    ui.pushButton_4.clicked.connect(addWord)
    ui.pushButton_3.clicked.connect(showDict)
    ui.pushButton_2.clicked.connect(test)
    ui.pushButton.clicked.connect(showAbout)

    app.exec_()
    