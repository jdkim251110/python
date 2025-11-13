# MyProd 헬스케어 제품 관리 (PyQt5)

간단한 PyQt5 기반 데스크탑 앱입니다. SQLite 데이터베이스(`myprod.db`)에 `MyProd` 테이블을 만들고, `id`(INTEGER PRIMARY KEY AUTOINCREMENT), `name`(TEXT), `price`(INTEGER), `qty`(INTEGER) 컬럼을 관리합니다.

주요 기능
- 제품 입력 (name, price, qty)
- 선택한 항목 수정
- 선택한 항목 삭제
- 이름으로 검색
- 하단의 테이블에서 목록 확인 및 선택
- 처음 실행 시 샘플 데이터 100건을 채웁니다(이미 100건 이상이면 추가하지 않음)

파일
- `myprod_app.py`: 앱 메인 소스
- `requirements.txt`: 의존성 (PyQt5 포함)

실행 방법 (Windows PowerShell)
1. 가상환경(선택)

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. 의존성 설치

```powershell
pip install -r requirements.txt
```

3. 앱 실행

```powershell
python myprod_app.py
```

주의
- `myprod.db` 파일이 실행한 폴더에 생성됩니다.
- PyQt5 설치에 인터넷 연결이 필요합니다.

간단한 확장 아이디어
- 가격/수량에 대한 정렬, CSV 내보내기/불러오기, 상세 폼을 추가할 수 있습니다.
