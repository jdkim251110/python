# coding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import re 

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
#파일 저장
f = open("todayhumor.txt", "wt", encoding="utf-8")
for n in range(1, 11):
    #오늘의 유머 베스트게시판  
    data ='https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=' + str(n)
    print(data)
    #웹브라우져 헤더 추가 
    req = urllib.request.Request(data, headers = hdr)
    data = urllib.request.urlopen(req).read()
    #한글이 깨지는 경우 
    page = data.decode('utf-8', 'ignore')
    soup = BeautifulSoup(page, 'html.parser')
    list = soup.find_all('td', attrs={'class':'subject'})
    for item in list:
        try:
            title = item.find('a').text.strip()
            #특정 속성을 검색
            href = item.find('a')['href']
            if re.search('일본', title):
                print(title) 
                print('https://www.todayhumor.co.kr/' + href)
                f.write(title + '\n')             
        except:
            pass

f.close()      

#<td class="subject">
#<a href="/board/view.php">한국 아마추어 러닝씬에 홀연히 등장한 노력의 천재</a>