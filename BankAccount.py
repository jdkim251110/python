# BankAccount.py
#은행의 계정을 표현한 클래스 
class BankAccount(object):
    #초기화메서드 
    def __init__(self, id, name, balance):
        #내부에 숨김(이름변경)
        self.__id = id
        self.__name = name 
        self.__balance = balance 
    #입금 메서드 
    def deposit(self, amount):
        self.__balance += amount 
    #출금 메서드     
    def withdraw(self, amount):
        self.__balance -= amount
    #결과 문자열로 리턴 
    def __str__(self):
        return "{0} , {1} , {2}".format(self.__id, 
            self.__name, self.__balance)

#인스턴스 객체를 생성
account1 = BankAccount(100, "전우치", 15000)
account1.deposit(5000)
account1.withdraw(3000)
print(account1)
#외부에서 접근
#print(account1.__balance)
