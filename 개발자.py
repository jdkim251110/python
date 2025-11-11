#개발자 클래스를 정의: id, name, skill속성 포함
class Developer:
    def __init__(self, id, name, skill):
        self.id = id
        self.name = name
        self.skill = skill

    def __str__(self):
        #f-string:변수명을 직접 넘기는 문법 
        return f"Developer(id={self.id}, name={self.name}, skill={self.skill})" 
    
#인스턴스 생성
dev1 = Developer(1, "Alice", "Python")
dev2 = Developer(2, "Bob", "JavaScript")

#인스턴스 정보 출력
print(dev1)
print(dev2)


