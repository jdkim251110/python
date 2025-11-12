# web1.py 
#크롤링하는 코드 작성
from bs4 import BeautifulSoup

#페이지를 로딩
page = open("Chap09_test.html", "rt", encoding="utf-8").read()

#스프객체를 생성
soup = BeautifulSoup(page, "html.parser")

#검색
#print(soup.prettify())
#<p>태그 전체 검색 
#print( soup.find_all("a") )
#첫번째 <p>태그 검색
#print( soup.find("p") )
#조건 검색: <p class="outer-text">
#print( soup.find_all("p", attrs={"class":"outer-text"}) )

#태그내부의 문자열: .text 
for tag in soup.find_all("p"):
    title = tag.text.strip() 
    title = title.replace("\n", "")
    print(title)

