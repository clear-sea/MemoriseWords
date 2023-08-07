# 导入相关PyQt5模块
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from fileCore import *
from UI import Ui_entryDialog,Ui_show
'''单词本类，具有增删功能'''
class WordsBook:
    '''
    参数解释:
    parent:父类控件(应该为主程序中的主窗口)
    filepath:文件路径
    browseWidgetTitle:设置父类窗口的标题
    backFunction:返回按钮绑定的返回函数，用于返回到上一个界面
    '''
    def __init__(self,parent:QWidget,filepath:str,browseWidgetTitle:str,backFunction) -> None:
        self.window=parent # 父类控件
        self.browseWidgetTitle=browseWidgetTitle
        self.wordsDict=readWordsData(filepath) # 单词字典
        self.model=QStandardItemModel() # 创建Qt表格视图标准模型
        self.filepath=filepath # 引用的文件

        self.dialog=QDialog(self.window) # 输入添加单词的对话框
        self.uiDialog=Ui_entryDialog.Ui_Dialog()

        self.word,self.mean=None,None

        self.backFunction=backFunction

    '''关于添加单词对话框的函数'''
    def addWord(self) -> None:
        # 创建并初始化界面
        self.uiDialog.setupUi(self.dialog)
        self.dialog.show()
        # 连接事件
        self.uiDialog.buttonBox.accepted.connect(self.setDataByButton)
        self.uiDialog.buttonBox.rejected.connect(lambda:self.dialog.destroy())
    def setDataByButton(self)->None:
        '''点击OK按钮设置addWordResult'''
        self.word=self.uiDialog.lineEdit.text()
        self.mean=self.uiDialog.lineEdit_2.text()
        if(self.word=='' or self.mean==''): # 判断输入内容是否为空
            QMessageBox.warning(self.dialog,"警告","输入内容不能为空",QMessageBox.Ok)
            return None
        if(self.word in list(self.wordsDict.keys())):
            QMessageBox.warning(self.dialog,"警告","已经存在这个单词了",QMessageBox.Ok)
            return None

        self.model.appendRow([QStandardItem(self.word),QStandardItem(self.mean)])
        # 在字典中添加，并写入文件
        self.wordsDict[self.word]=self.mean
        saveWordsData(self.filepath,self.wordsDict)

    def deleteSelectedWord(self) -> None:
        '''删除选中行单词'''
        index = self.ui.tableView.currentIndex()  # 取得当前选中行的index
        word=self.ui.tableView.currentIndex().data() # 获取选中行的内容
        self.model.removeRow(index.row())  # 通过index的row()操作得到行数进行删除
        
        self.wordsDict.pop(word) # 在生词本字典中删除该单词
        saveWordsData(self.filepath,self.wordsDict) # 写入dict.json

    def browseWordsDict(self):
        '''显示单词'''
        # 设置界面
        self.window.setWindowTitle(self.browseWidgetTitle) # 主设置窗口标题
        self.subWin=QWidget(self.window) # 窗口控件
        self.ui=Ui_show.Ui_Form() # 创建UI界面
        self.ui.setupUi(self.subWin)
        # 设置tableView
        self.model.clear() # 先清空
        self.model.setHorizontalHeaderLabels(['单词','释义']) # 设置模型的表头
        self.ui.tableView.setModel(self.model) # 给列表视图设置模型
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中整行
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中一行
        self.ui.tableView.setEditTriggers(QTableView.NoEditTriggers) # 不可编辑
        # 遍历单词表并添加每一个单词到列表视图中
        for word in self.wordsDict:
            self.model.appendRow([QStandardItem(word),QStandardItem(self.wordsDict[word])])
        self.subWin.show() # 显示
        # 绑定事件
        self.ui.backbutton.clicked.connect(self.backFunction)
        self.ui.pushButton_2.clicked.connect(self.deleteSelectedWord)
        self.ui.pushButton.clicked.connect(self.addWord)
