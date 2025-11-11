#부모 클래스 
class Person:
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber
    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, 
            self.phoneNumber))

#자식 클래스 
class Student(Person):
    #상속받은 메서드를 덮어쓰기(override, 재정의)
    def __init__(self, name, phoneNumber, subject, studentID):
        #명시적으로 부모 초기화메서드
        #Person.__init__(self, name, phoneNumber)
        super().__init__(name, phoneNumber)
        self.subject = subject
        self.studentID = studentID
    #덮어쓰기
    def printInfo(self):
        print("Info(이름:{0}, 전화번호: {1})".format(self.name, 
            self.phoneNumber))
        print("Info(학과:{0}, 학번: {1})".format(self.subject, 
            self.studentID))
        

p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "인공지능", "251234")
p.printInfo() 
s.printInfo() 


