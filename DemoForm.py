# DemoForm.py 
# DemoForm.ui(화면단) + DemoForm.py(로직단)
import sys 
from PyQt5.QtWidgets import *
from PyQt5 import uic

#파일 로딩 
form_class = uic.loadUiType("DemoForm.ui")[0]

#폼 클래스 정의 
class DemoForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("첫번째 PyQt코딩")
       
#직접 모듈을 실행한 경우만 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoForm()
    demo.show()
    app.exec_()
    
