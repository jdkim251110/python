# demoFile.py 

#쓰기 
f = open("demo.txt", "wt", encoding="utf-8")
f.write("첫번째\n두번째\n세번째\n")
f.close()

#읽기
f = open("demo.txt", "rt", encoding="utf-8")
content = f.read()
print(content)
f.close()
