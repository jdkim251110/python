KIMPGA 상위 코인 크롤러

사용법:

1) 의존성 설치

```powershell
pip install requests beautifulsoup4
```

Selenium을 사용하려면:

```powershell
pip install selenium
# ChromeDriver 등 브라우저 드라이버를 설치하고 --driver로 경로를 지정하거나 PATH에 추가
```

2) 실행 예

```powershell
python kimpga_top20.py --top 20 --csv top20.csv
```

설명:
- 기본적으로 requests로 페이지 소스를 가져와 파싱합니다. 만약 페이지가 자바스크립트로 렌더링되어 데이터가 보이지 않는다면 `--selenium` 옵션을 사용하세요.
- 파서는 범용(heuristic) 방식으로 동작하므로 사이트 구조 변경 시 셀렉터 조정이 필요할 수 있습니다.
