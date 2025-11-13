import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# 검색어
search_keyword = "아이폰17"

# 네이버 블로그 검색 URL
url = f"https://search.naver.com/search.naver?where=blog&query={quote(search_keyword)}"

# 요청 헤더 설정 (User-Agent를 포함하여 요청)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # GET 요청
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    
    # 상태 코드 확인
    if response.status_code == 200:
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 블로그 글 제목 크롤링
        # 네이버 블로그 검색 결과의 제목은 'a.fds-comps-right-image-text-title' 클래스에 있음
        titles = soup.find_all('a', class_='fds-comps-right-image-text-title')
        
        if titles:
            print(f"'{search_keyword}' 검색 결과 블로그 글 제목:\n")
            for i, title in enumerate(titles[:10], 1):  # 상위 10개만 출력
                # span 태그 내의 텍스트를 추출
                title_text = title.find('span', class_='fds-comps-text')
                if title_text:
                    text = title_text.get_text(strip=True)
                    link = title.get('href')
                    print(f"{i}. {text}")
                    print(f"   링크: {link}\n")
        else:
            print("제목을 찾을 수 없습니다.")
    else:
        print(f"요청 실패: 상태 코드 {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"요청 오류: {e}")
except Exception as e:
    print(f"오류 발생: {e}")
