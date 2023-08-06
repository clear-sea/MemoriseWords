from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QFont,QStandardItemModel,QStandardItem
import sys
from UI import Ui_passWords,Ui_about,Ui_show,Ui_entryDialog
import Ui_main

def readQSS(filepath:str) -> str:
    '''读取QSS文件'''
    with open(filepath,'r',encoding="utf-8") as file:
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

def showMain()->None:
    '''显示主页面'''
    subWin=QWidget(window)
    ui=Ui_main.Ui_Form()
    ui.setupUi(subWin)
    window.setWindowTitle("背单词小程序")
    
    subWin.show()

    ui.label.setText(f"词汇表单词数量:{length}")
    initMainButtons()
    
def passWords()->None:
    '''过单词'''
    subWin=QWidget(window)

    ui=Ui_passWords.Ui_Form()
    ui.setupUi(subWin)
    window.setWindowTitle("记单词")
    subWin.show()
    
    ui.commandLinkButton.clicked.connect(showMain)

    index=0 # 记录目前查看的单词的索引
    word=wordsKeyList[index] # 通过index

    def next1():
        '''记住了'''
        nonlocal index,word

        if index>length-1: # 已经是最后一个单词，不再继续
            QMessageBox.warning(window,"警告","已经是单词表里的最后一个单词了",QMessageBox.Ok)
            return None
        word=wordsKeyList[index] # 通过index获取当前的单词
        ui.label.setText(f"{word}\n{words[word]}") # 显示当前单词
        
        index+=1 # 索引+1，查看下一个单词
        
    def next2():
        '''加入生词本'''
        nonlocal index,word

        if index>length-1: # 已经是最后一个单词，不再继续
            QMessageBox.warning(window,"警告","已经是单词表里的最后一个单词了",QMessageBox.Ok)
            return None
        
        word=wordsKeyList[index] # 通过index获取当前的单词

        dictVbook[word]=words[word] # 加入生词本
        saveWordsData("dict.json",dictVbook)
        ui.label.setText(f"{word}\n{words[word]}") # 显示当前单词

        index+=1 # 索引+1，查看下一个单词
        
    ui.label.setText("过单词\n点击下面任意按钮开始")

    ui.pushButton_2.clicked.connect(next1)
    ui.pushButton.clicked.connect(next2)

def test()->None:
    '''测验单词'''
    pass

def showAbout()->None:
    '''关于页面'''
    global window
    subWin=QWidget(window)

    ui=Ui_about.Ui_Form()
    ui.setupUi(subWin)
    subWin.show()
    
    ui.label_2.setOpenExternalLinks(True)
    ui.label_4.setOpenExternalLinks(True)
    ui.commandLinkButton.clicked.connect(showMain)
        
'''单词本类，具有增删功能'''
class WordsBook:
    def __init__(self,parent:QWidget,model:QStandardItemModel,filepath:str,browseWidgetTitle:str) -> None:
        self.window=parent # 父类控件
        self.browseWidgetTitle=browseWidgetTitle
        self.wordsDict=readWordsData(filepath) # 单词字典
        self.model=model # Qt表格视图标准模型
        self.filepath=filepath # 引用的文件
        self.subWin=QWidget(self.window) # 窗口控件
        self.ui=Ui_show.Ui_Form() # 创建UI界面
        self.ui.setupUi(self.subWin)

        self.ui.commandLinkButton.clicked.connect(showMain)
        self.ui.tableView.setModel(self.model) # 给列表视图设置模型
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中整行
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中一行
        self.ui.tableView.setEditTriggers(QTableView.NoEditTriggers) # 不可编辑

        self.dialog=QDialog(self.window) # 输入添加单词的对话框
        self.uiDialog=Ui_entryDialog.Ui_Dialog()

        self.addWordResult=(None,None)

        self.ui.pushButton.clicked.connect(self.addWord)

    '''关于添加单词对话框的函数'''
    def initAddWordDialog(self) -> None:
        # 创建并初始化界面
        self.uiDialog.setupUi(self.dialog)
        self.dialog.show()
        # 连接事件
        self.uiDialog.buttonBox.accepted.connect(self.setDataByButton)
        self.uiDialog.buttonBox.rejected.connect(lambda:self.dialog.destroy())
    def setDataByButton(self)->None:
        if(self.uiDialog.lineEdit.text()=='' or self.uiDialog.lineEdit_2.text()==''): # 判断输入内容是否为空
            QMessageBox.warning(self.dialog,"警告","输入内容不能为空",QMessageBox.Ok)
            return None
        self.addWordResult=(self.uiDialog.lineEdit.text(),self.uiDialog.lineEdit_2.text())
        word,mean=self.addWordResult
        self.model.appendRow([QStandardItem(word),QStandardItem(mean)])
        # 在字典中添加，并写入文件
        self.wordsDict[word]=mean
        saveWordsData(self.filepath,self.wordsDict)

        self.dialog.destroy()

    def addWord(self):
        self.initAddWordDialog()

    def deleteSelectedWord(self) -> None:
        '''删除选中行单词'''
        index = self.ui.tableView.currentIndex()  # 取得当前选中行的index
        word=self.ui.tableView.currentIndex().data() # 获取选中行的内容
        self.model.removeRow(index.row())  # 通过index的row()操作得到行数进行删除
        
        self.wordsDict.pop(word) # 在生词本字典中删除该单词
        saveWordsData(self.filepath,self.wordsDict) # 写入dict.json

    def browseWordsDict(self):
        '''显示单词'''
        self.subWin.show()
        self.window.setWindowTitle(self.browseWidgetTitle) # 主设置窗口标题

        for word in self.wordsDict:
            self.model.appendRow([QStandardItem(word),QStandardItem(self.wordsDict[word])])

        self.ui.pushButton_2.clicked.connect(lambda:self.deleteSelectedWord())
        self.ui.pushButton.clicked.connect(lambda:None)

def initMainButtons()->None:

    '''绑定事件'''
    ui.pushButton_5.clicked.connect(passWords)
    ui.pushButton_4.clicked.connect(wordsBook.browseWordsDict)
    ui.pushButton_3.clicked.connect(vBook.browseWordsDict)
    ui.pushButton_2.clicked.connect(test)
    ui.pushButton_1.clicked.connect(showAbout)

if __name__=="__main__":
    '''创建qt应用'''
    app = QApplication(sys.argv)
    '''加载QSS'''
    qssFile=readQSS("style.qss")
    app.setStyleSheet(qssFile)
    '''读取文件'''
    words=readWordsData("words.json") # 单词表里的所有单词即中文意思
    length=len(words) # 单词表词数
    wordsKeyList=list(words.keys()) # 只有所有的单词，没有中文意思
    dictVbook=readWordsData("vbook.json") # 生词本Vocabulary books
    '''创建窗口'''
    window=QWidget()
    window.setWindowIcon(QIcon('images/logo.png'))
    '''显示主页面'''
    ui=Ui_main.Ui_Form()
    ui.setupUi(window)
    window.setFixedSize(window.width(), window.height()) # 禁止拉伸窗口大小
    
    window.show()
    '''创建WordsBook实例(单词本和生词本)'''
    model=QStandardItemModel() # 创建列表模型
    model.setHorizontalHeaderLabels(['单词','释义']) # 设置模型的表头
    wordsBook=WordsBook(window,model,"words.json","单词本")
    vBook=WordsBook(window,model,"vbook.json","生词本")

    ui.label.setText(f"词汇表单词数量:{length}")
    initMainButtons()
    
    app.exec_()
    