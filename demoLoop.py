# demoLoop.py 

value = 5 
while value > 0:
    print(value)
    value -= 1 

print("for in루프")
lst = [100, 200, 300]
for i in lst:
    print(i)

#구구단 출력 
for x in [2,3,4,5,6,7,8,9]:
    print("---{0}단---".format(x))
    for y in [1,2,3,4,5,6,7,8,9]:
        print("{0} * {1} = {2}".format(x, y, x*y))


print("---range()함수---")
print(list(range(10)))
print(list(range(2000, 2026)))
print(list(range(1, 32)))

print("---리스트 컴프리헨션---")
lst = list(range(1,11))
print( [i**2 for i in lst if i > 5] )
d = {100:"apple", 200:"banana"}
print( [v.capitalize() for v in d.values()] )

