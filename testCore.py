'''此模块定义单词测验的核心功能'''
from UI import Ui_ECtest,Ui_testResult,Ui_CETest
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtCore import Qt
from fileCore import *
import random

def getDRandomNum(a:int,min:int,max:int)->int:
    '''
    获取一个不等于a的随机数
    Get different random number
    '''
    result=random.randint(min,max)
    while(result==a):
        result=random.randint(min,max)

    return result

class TestCore:
    '''
    测验功能核心
    '''
    def __init__(self,parent:QWidget,filepath:str,backFunction) -> None:
        self.parent=parent
        self.backFunction=backFunction
        self.filepath=filepath

        self.words=readWordsData(filepath)
        self.wordsKeysList=list(self.words.keys())
        self.length=len(self.words)

        self.errorWords={}

        self.index=0 # 当前单词的索引
        self.correctNum=0 # 正确数量
        self.errorNum=0 # 错误数量
        self.word="" # 当前单词
        self.ansChoice=None # 正确答案的选择(1,2,3分别代表第一个第二个第三个选项)
        self.userChoice=None # 用户的选择(1,2,3分别代表第一个第二个第三个选项)

    def ECTest(self)->None:
        '''
        看英语选意思
        English Chinese
        '''
        # 初始化
        self.index=0
        self.correctNum=0
        self.errorNum=0
        self.errorWords={}
        # 设置界面
        self.subWin=QWidget(self.parent)
        self.ui=Ui_ECtest.Ui_Form()
        self.ui.setupUi(self.subWin)
        self.subWin.show()
        self.parent.setWindowTitle("测验")
        # 绑定事件
        self.ui.backbutton.clicked.connect(self.backFunction)
        self.ui.pushButton.clicked.connect(self.next1)
        # 按钮盒
        self.btnGroup=QButtonGroup(self.parent)
        self.btnGroup.addButton(self.ui.radioButton)
        self.btnGroup.addButton(self.ui.radioButton_2)
        self.btnGroup.addButton(self.ui.radioButton_3)
        # 设置为下一个单词(第一个单词)
        self.word=self.wordsKeysList[self.index]
        self.ui.label.setText(self.word)
        self.randomChoice() # 随机生成选项
        # 所有单选按钮取消选择
        self.btnGroup.setExclusive(False)
        self.ui.radioButton.setChecked(False)
        self.ui.radioButton_2.setChecked(False)
        self.ui.radioButton_3.setChecked(False)
        self.btnGroup.setExclusive(True)

    def randomChoice(self):
        '''随机生成选项'''
        self.ansChoice=random.randint(1,3)
        if self.ansChoice==1:
            self.ui.radioButton.setText(self.words[self.word])
            self.ui.radioButton_2.setText(self.words[self.wordsKeysList[getDRandomNum(self.index,0,self.length-1)]])
            self.ui.radioButton_3.setText(self.words[self.wordsKeysList[getDRandomNum(self.index,0,self.length-1)]])
        elif self.ansChoice==2:
            self.ui.radioButton_2.setText(self.words[self.word])
            self.ui.radioButton.setText(self.words[self.wordsKeysList[getDRandomNum(self.index,0,self.length-1)]])
            self.ui.radioButton_3.setText(self.words[self.wordsKeysList[getDRandomNum(self.index,0,self.length-1)]])
        elif self.ansChoice==3:
            self.ui.radioButton_3.setText(self.words[self.word])
            self.ui.radioButton_2.setText(self.words[self.wordsKeysList[getDRandomNum(self.index,0,self.length-1)]])
            self.ui.radioButton.setText(self.words[self.wordsKeysList[getDRandomNum(self.index,0,self.length-1)]])

    def next1(self):
        '''"English Chinese 看英语选意思"模式下'''
        # 判断是否选择
        if self.ui.radioButton.isChecked()==False and self.ui.radioButton_2.isChecked()==False and self.ui.radioButton_3.isChecked()==False:
            # 一个都没选的情况
            QMessageBox.warning(self.parent,"警告","没有选择任何一个选项",QMessageBox.Ok)
            return None
        
        # 根据radioButton选择
        if self.ui.radioButton.isChecked():self.userChoice=1
        elif self.ui.radioButton_2.isChecked():self.userChoice=2
        elif self.ui.radioButton_3.isChecked():self.userChoice=3
        # 判断选择的正误，计错误数
        if self.userChoice!=self.ansChoice:
            self.errorNum+=1
            self.errorWords[self.word]=self.words[self.word]

        # 设置为下一个单词
        if self.index==self.length-2: # 到倒数第二个单词，就改变按钮功能
            self.ui.pushButton.setText("查看结果")
            self.ui.pushButton.clicked.disconnect(self.next1)
            self.ui.pushButton.clicked.connect(self.testResult)
        elif self.index==self.length-1:
            return None
        self.index+=1
        self.word=self.wordsKeysList[self.index]
        self.ui.label.setText(self.word)
        self.randomChoice() # 随机生成选项
        
        # 所有单选按钮取消选择
        self.btnGroup.setExclusive(False)
        self.ui.radioButton.setChecked(False)
        self.ui.radioButton_2.setChecked(False)
        self.ui.radioButton_3.setChecked(False)
        self.btnGroup.setExclusive(True)

    def testResult(self)->None:
        # 设置界面
        self.subWin=QWidget(self.parent)
        self.ui=Ui_testResult.Ui_Form()
        self.ui.setupUi(self.subWin)
        self.parent.setWindowTitle("测验结果")
        self.subWin.show()
        # 绑定事件
        self.ui.backbutton.clicked.connect(self.backFunction)
        # 显示数据
        self.correctNum=self.length-self.errorNum
        self.ui.label.setText(f"正确:{self.correctNum}")
        self.ui.label_2.setText(f"错误:{self.errorNum}")
        self.ui.label_3.setText(f"错误率:{round((self.errorNum/self.length)*100,2)}%")
        # 设置表格
        model=QStandardItemModel(self.subWin)
        # 设置tableView
        model.clear() # 先清空
        model.setHorizontalHeaderLabels(['错误单词','释义']) # 设置模型的表头
        self.ui.tableView.setModel(model) # 给列表视图设置模型
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中整行
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中一行
        self.ui.tableView.setEditTriggers(QTableView.NoEditTriggers) # 不可编辑
        # 添加项，并把出错的单词保存在生词本
        vBookWords=readWordsData("vbook.json")
        for i in self.errorWords:
            model.appendRow([QStandardItem(i),QStandardItem(self.errorWords[i])])
            vBookWords[i]=self.errorWords[i]
        
        saveWordsData("vbook.json",vBookWords)
    
    def next2(self)->None:
        self.ui.lineEdit.setFocus()
        userAns=self.ui.lineEdit.text()
        # 判断是否填写
        if userAns=='':
            QMessageBox.warning(self.parent,"警告","没有填写",QMessageBox.Ok)
            return None
        # 判断选择的正误，计错误数
        if userAns!=self.word:
            self.errorNum+=1
            self.errorWords[self.word]=self.words[self.word]

        # 设置为下一个单词
        if self.index==self.length-2: # 到倒数第二个单词，就改变按钮功能
            self.ui.pushButton.setText("查看结果")
            self.ui.pushButton.clicked.disconnect(self.next2)
            self.ui.pushButton.clicked.connect(self.testResult)
        elif self.index==self.length-1:
            return None
        self.index+=1
        self.word=self.wordsKeysList[self.index]
        self.ui.label.setText(self.words[self.word])
        # 清空文本框
        self.ui.lineEdit.clear()
        
    def CETest(self)->None:
        '''Chinese English 看汉语拼写单词'''
        # 初始化
        self.index=0
        self.correctNum=0
        self.errorNum=0
        self.errorWords={}
        # 设置界面
        self.subWin=QWidget(self.parent)
        self.ui=Ui_CETest.Ui_Form()
        self.ui.setupUi(self.subWin)
        self.parent.setWindowTitle("测验")
        self.subWin.show()
        # 绑定事件
        self.ui.backbutton.clicked.connect(self.backFunction)
        self.ui.pushButton.clicked.connect(self.next2)
        # 设置为第一个单词
        self.word=self.wordsKeysList[self.index]
        self.ui.label.setText(self.words[self.word])
        self.ui.lineEdit.setFocus()
