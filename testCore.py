'''此模块定义单词测验的核心功能'''
from UI import Ui_ECtest
from PyQt5.QtWidgets import *
from fileCore import *

class TestCore:
    def __init__(self,parent:QWidget,filepath:str,backFunction) -> None:
        self.parent=parent
        self.backFunction=backFunction
        self.filepath=filepath

    def ECTest(self)->None:
        '''English Chinese 看英语选意思'''
        self.words=readWordsData(self.filepath) # 读取文件
        # 设置界面
        subWin=QWidget(self.parent)
        ui=Ui_ECtest.Ui_Form()
        ui.setupUi(subWin)
        self.parent.setWindowTitle("选择")
        subWin.show()
        self.parent.setWindowTitle("测验")

        ui.backbutton.clicked.connect(self.backFunction)
        
    def CETest(self)->None:
        '''Chinese English 看汉语拼写单词'''
        pass