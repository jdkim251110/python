# demoStrList.py 

strA = "python"
strB = "파이썬은 강력해"

print(len(strA))
print(len(strB))
print(strA[0:3])
print(strA[:3])
print(strA[-2:])

#리스트를 연습
colors = ["red", "blue", "green"]
print(len(colors))
print(type(colors))
colors.append("white")
colors.insert(1, "black")
print(colors)
colors.remove("red")
print(colors)
colors.sort()
print(colors)
colors.reverse()
print(colors)

#세트 형식 연습 
a = {1, 2, 3, 3}
b = {3, 4, 4, 5}
print(a)
print(b)
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))

#튜플 연습
tp = (10, 20, 30)
print(tp)
print(len(tp))
print(tp[0])

#함수 정의
def calc(a,b):
    return a+b, a*b 

#함수 호출
result = calc(3,4)
print(result)

args = (5,6)
print(calc(*args))

#형식 변환(Type Casting)
a = set((1,2,3))
print(a)
b = list(a)
b.append(30)
print(b)



