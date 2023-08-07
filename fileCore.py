'''此模块定义核心的文件操作函数'''
import os

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

def createFile(filepath:str,defaultContext)->None:
    '''检测指定的文件是否存在，若不存在就创建'''
    if os.path.exists(filepath)==False or (os.path.exists(filepath) and os.path.isdir(filepath)): # 判断文件是否存在
        saveWordsData(filepath,defaultContext)