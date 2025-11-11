# demoDict.py 
colors = {"apple":"red", "banana":"yellow"}

print(len(colors))
#검색
print(colors["apple"])
#입력
colors["cherry"] = "red"
print(colors)
#삭제
del colors["apple"]
print(colors)

for item in colors.items():
    print(item)
    