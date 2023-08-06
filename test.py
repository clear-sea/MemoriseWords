import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QDialogButtonBox, 
                             QMessageBox, QPushButton, QVBoxLayout)
 
class DemoDialogButtonBox(QWidget):
    def __init__(self, parent=None):
        super(DemoDialogButtonBox, self).__init__(parent)       
        
        # 设置窗口标题
        self.setWindowTitle('实战PyQt5: QDialogButtonBox Demo!')      
        # 设置窗口大小
        self.resize(400, 240)
        
        bbOkCancel = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel, self) 
        bbOkCancel.button(QDialogButtonBox.Ok).setDefault(True)
        bbOkCancel.accepted.connect(self.onAccepted)
        bbOkCancel.rejected.connect(self.onRejected)     
        
        bbARI = QDialogButtonBox(QDialogButtonBox.Abort|QDialogButtonBox.Retry|QDialogButtonBox.Ignore, self)
        bbARI.accepted.connect(self.onAccepted)
        bbARI.rejected.connect(self.onRejected)
        
        #添加按钮
        bbVert = QDialogButtonBox(Qt.Vertical, self) 
        btnAdd = QPushButton('加法', self)
        btnSub = QPushButton('减法', self)
        btnMul = QPushButton('乘法', self)
        btnDiv = QPushButton('除法', self)
        
        bbVert.addButton(btnAdd, QDialogButtonBox.AcceptRole)
        bbVert.addButton(btnSub, QDialogButtonBox.AcceptRole)
        bbVert.addButton(btnMul, QDialogButtonBox.AcceptRole)
        bbVert.addButton(btnDiv, QDialogButtonBox.AcceptRole)
        bbVert.accepted.connect(self.onAccepted)
        bbVert.rejected.connect(self.onRejected)
        
        vLayout = QVBoxLayout(self)
        vLayout.setSpacing(16)
        vLayout.addStretch()
        vLayout.addWidget(bbOkCancel)
        vLayout.addWidget(bbARI)
        vLayout.addWidget(bbVert)
        vLayout.addStretch()
       
        self.setLayout(vLayout)
        
    def onAccepted(self):
        QMessageBox.information(self, '信息',  'accepted!!!')
        
    def onRejected(self):
        QMessageBox.information(self, '信息', 'rejected!!!')
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoDialogButtonBox()
    window.show()
    sys.exit(app.exec())