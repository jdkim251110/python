# demoFunction.py 
#1)함수를 정의
def setValue(newValue):
    x = newValue
    print("함수내부:", x)

#2)함수를 호출
retValue = setValue(5)
print(retValue)

#함수를 정의
def swap(x,y):
    return y,x 

#호출
result = swap(3,4)
print(result)

#디버깅연습 함수
def intersect(prelist, postlist):
    result = []
    for x in prelist:
        if x in postlist and x not in result:
            result.append(x)
    return result 

#호출
print(intersect("HAM", "SPAM"))


#LGB 이름 해석 규칙 
#전역변수 
x = 5 
def func(a):
    return a+x 

#호출
print(func(1))

def func2(a):
    #지역변수
    x = 10 
    return a+x 

#호출
print(func2(1))

#기본값을 명시 
def times(a=10, b=20):
    return a*b 

#호출
print(times())
print(times(5))
print(times(5,6))

#키워드인자-매개변수명을 지정 
def connectURI(server, port):
    strURL = "https://" + server + ":" + port 
    return strURL 

#호출
print(connectURI("multi.com", "80"))
print(connectURI(port="80", server="naver.com"))

#가변인자 처리
def union(*ar):
    result = [] 
    for item in ar:
        for x in item:
            if x not in result:
                result.append(x)
    return result 

#호출
print(union("HAM","EGG"))
print(union("HAM","EGG","SPAM"))