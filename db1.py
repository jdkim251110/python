# db1.py 
import sqlite3

#연결객체 
#영구적으로 파일에 저장
con = sqlite3.connect(r"c:\work\test.db")
#커서객체
cur = con.cursor()
#테이블생성(ANSI SQL99)
cur.execute("CREATE TABLE IF NOT EXISTS PhoneBook (name text, phoneNum text);")

#데이터삽입
cur.execute("INSERT INTO PhoneBook VALUES ('홍길동', '010-1234-5678');")

#입력 파라메터 처리
name = '전우치'
phoneNum = '010-9876-5432'
cur.execute("INSERT INTO PhoneBook VALUES (?, ?);", (name, phoneNum))

#여러건 입력
datalist = (('이영희', '010-1111-2222'), ('박민수', '010-3333-4444'))
cur.executemany("INSERT INTO PhoneBook VALUES (?, ?);", datalist)

#검색
# for row in cur.execute("SELECT * FROM PhoneBook;"):
#     print(row)

#패치메서드 호출
cur.execute("SELECT * FROM PhoneBook;")
print("---fetchone()---")
print(cur.fetchone()) #한건

print("---fetchmany(2)---")
print(cur.fetchmany(2)) #두건

print("---fetchall()---")
cur.execute("SELECT * FROM PhoneBook;")
print(cur.fetchall()) #전체 