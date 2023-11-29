import datetime
import openpyxl

class XlsxFileMaker : 
    def __init__(self) :
        self.fileName = ""
        pass 

    def createFile(self) : 
        self.fileName = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
        pass 

    def overWriteFile(self):
        pass 
    