#!/usr/bin/python
# coding=utf-8
import os
from datetime import time, datetime


class LogManager:
    def __init__(self):
        pass

    @classmethod
    def writeToFile(cls,filename, fileContent):
        fp = file('result/' + filename + '.txt', 'a')
        fp.write(fileContent + '\n')
        fp.close()

    @classmethod
    def writeToLog(cls, logContent):
        fp = file(os.path.dirname(os.getcwd())+'\\zhihu\\zhihu\\log\\'+datetime.now().strftime('%Y%m%d')  + '.txt', 'a')
        fp.write(logContent + '\n')
        fp.close()
