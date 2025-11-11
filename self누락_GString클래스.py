#전역변수
strName = "Not Class Member"

class DemoString:
    def __init__(self):
        #인스턴스멤버변수
        self.strName = "" 
    def set(self, msg):
        self.strName = msg
    def print(self):
        #꼼꼼하게 코딩
        print(self.strName)

#인스턴스 생성 
d = DemoString()
d.set("First Message")
d.print()
