#!/usr/bin/env python3
"""
kimpga_top20.py

KIMPGA(https://kimpga.com) 메인 페이지에서 상위 N개(기본 20개) 코인 정보를 추출하는 스크립트입니다.

방법:
- 기본(빠른) 모드: requests + BeautifulSoup 사용 (JS 불필요한 정적 요소 파싱)
- 필요시 Selenium(헤드리스 브라우저)을 사용해 렌더된 페이지 소스를 받아 파싱할 수 있습니다.

출력: 파이썬 리스트(딕셔너리) 형태로 반환, 옵션으로 CSV로 저장 가능

주의: 사이트가 자바스크립트로 동적으로 렌더링한다면 requests로는 데이터가 보이지 않을 수 있습니다.
그 경우 --selenium 옵션을 사용하세요(별도 설치 필요).

사용 예:
    python kimpga_top20.py --top 20 --csv top20.csv

필요 패키지:
    pip install requests beautifulsoup4
    # selenium 사용 시: pip install selenium 그리고 브라우저 드라이버 필요
"""

from typing import List, Dict, Optional
import re
import requests
from bs4 import BeautifulSoup
import csv
import argparse
import sys


def fetch_html(url: str, headers: Optional[dict] = None) -> Optional[str]:
    headers = headers or {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[ERROR] 요청 실패: {e}")
        return None


def try_parse_table(soup: BeautifulSoup, top_n: int) -> List[Dict]:
    """일반적인 테이블 구조에서 코인 목록 파싱 시도
    - 테이블 헤더를 보고 컬럼 매핑을 시도
    - 가능한 정보: rank, name, symbol, price, change, volume, market_cap
    """
    results = []
    tables = soup.find_all("table")
    for table in tables:
        # 헤더 셀 텍스트로 테이블인지 추정
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        headers_text = " ".join(headers).lower()
        if any(k in headers_text for k in ("코인", "coin", "price", "가격", "변동", "change")):
            # 후보 테이블
            for tr in table.select("tbody tr"):
                if len(results) >= top_n:
                    break
                cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if not cols:
                    continue
                entry = {"raw": cols}
                # 간단한 매핑 시도: 첫 열이 순위일 확률
                try:
                    if cols[0].isdigit():
                        entry["rank"] = int(cols[0])
                    else:
                        entry["rank"] = None
                except Exception:
                    entry["rank"] = None
                # 이름/심볼/가격/변동 등은 텍스트에서 추출
                # Best-effort: 긴 문자열을 name, 뒤에 통화 기호 등은 price로 추정
                if len(cols) >= 2:
                    entry["name"] = cols[1]
                if len(cols) >= 3:
                    entry["price"] = cols[2]
                if len(cols) >= 4:
                    entry["change"] = cols[3]
                results.append(entry)
            if results:
                return results[:top_n]
    return []


def try_parse_cards(soup: BeautifulSoup, top_n: int) -> List[Dict]:
    """테이블이 없는 경우, 카드형 목록에서 파싱 시도
    - 코인명이 포함된 요소들을 찾아서 핵심 텍스트를 수집
    """
    results = []
    # 코인 이름이나 가격을 포함하는 일반적인 클래스 후보
    candidates = soup.find_all(lambda tag: tag.name in ("div", "li", "tr") and tag.get_text(strip=True))
    for c in candidates:
        text = c.get_text(" ", strip=True)
        if any(k in text for k in ("BTC", "ETH", "코인", "가격", "원", "KRW", "USD")):
            # 간단히 name과 price를 분리하여 저장
            parts = text.split()
            entry = {"raw": parts}
            if parts:
                entry["name"] = parts[0]
            if len(parts) > 1:
                entry["price"] = parts[1]
            results.append(entry)
        if len(results) >= top_n:
            break
    return results[:top_n]


def try_parse_kimpga(soup: BeautifulSoup, top_n: int) -> List[Dict]:
    """KIMPGA 특화 파서
    제공하신 HTML 예시를 기반으로 구현:
    - 코인 심볼은 <img alt="SYMBOL"> 에 들어있음
    - 코인 이름은 같은 셀(또는 같은 tr) 안의 span(overflow-ellipsis 등)에 들어있음
    - 가격/변동은 같은 tr의 다른 td에서 찾아 시도
    """
    results: List[Dict] = []

    # img 태그의 alt 속성(심볼)을 기준으로 후보를 찾는다
    imgs = soup.find_all("img", alt=True)
    for img in imgs:
        if len(results) >= top_n:
            break

        symbol = img.get("alt", "").strip()
        if not symbol:
            continue

        # 가능한 tr 컨텍스트를 찾는다
        tr = img.find_parent("tr") or img.find_parent()
        # 이름 추출: 같은 td/컨테이너 내의 span 중에서 심볼과 다른 텍스트를 선택
        name = None
        parent = img.find_parent()
        spans = parent.find_all("span") if parent else []
        for sp in spans:
            txt = sp.get_text(strip=True)
            if not txt:
                continue
            # 심볼(예: USDT)와 동일한 텍스트는 건너뜀
            if txt.upper() == symbol.upper():
                continue
            # 너무 짧은 영문 대문자(아이콘 등) 건너뛰기
            if len(txt) <= 4 and txt.isupper():
                continue
            name = txt
            break

        # 가격/변동 추정: 같은 tr 내에서 숫자/통화표시를 포함한 td를 찾아본다
        price = None
        change = None
        if tr:
            tds = tr.find_all("td")
            for td in tds:
                txt = td.get_text(" ", strip=True)
                if not txt:
                    continue
                # 가격 패턴 예: 12,345 원 / $12,345 / 12,345.67
                if re.search(r"\d[\d,\.]+\s*(원|krw|usd|\$)?", txt.replace('\xa0',' '), re.I):
                    # 가격으로 추정. 첫 발견을 가격으로 사용
                    if price is None and any(ch.isdigit() for ch in txt):
                        price = txt
                        continue
                # 변동(%) 패턴
                if re.search(r"[-+]?\d+\.?\d*%", txt):
                    change = txt

        entry: Dict = {"symbol": symbol, "name": name or None, "price": price, "change": change, "raw": tr.get_text(" ", strip=True) if tr else parent.get_text(" ", strip=True)}
        results.append(entry)

    # 일부 중복/잘못 감지된 항목이 있을 수 있으므로 심볼 기준으로 고유화
    seen = set()
    unique_results: List[Dict] = []
    for e in results:
        sym = (e.get("symbol") or "").upper()
        if not sym or sym in seen:
            continue
        seen.add(sym)
        unique_results.append(e)
        if len(unique_results) >= top_n:
            break

    # 결과에 순위 추가
    for idx, it in enumerate(unique_results, start=1):
        it.setdefault("rank", idx)

    return unique_results[:top_n]


def get_top_coins(url: str, top_n: int = 20, use_selenium: bool = False, driver_path: Optional[str] = None) -> List[Dict]:
    """주어진 URL에서 상위 top_n 코인 정보를 반환합니다.

    기본적으로 requests로 시도합니다. 필요하면 use_selenium=True로 렌더링 후 파싱할 수 있습니다.
    """
    html = fetch_html(url)
    if html is None and use_selenium:
        html = None  # will try selenium below

    if html is None and use_selenium:
        # Selenium 사용 시도
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
        except Exception as e:
            print(f"[ERROR] selenium 모듈을 불러올 수 없습니다: {e}")
            return []

        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        driver = None
        try:
            if driver_path:
                driver = webdriver.Chrome(executable_path=driver_path, options=opts)
            else:
                driver = webdriver.Chrome(options=opts)
            driver.get(url)
            html = driver.page_source
        except Exception as e:
            print(f"[ERROR] Selenium으로 페이지를 로드하지 못했습니다: {e}")
            if driver:
                driver.quit()
            return []
        finally:
            if driver:
                driver.quit()

    if not html:
        print("[WARN] 페이지 소스를 가져오지 못했습니다.")
        return []

    soup = BeautifulSoup(html, "html.parser")

    # 1) 테이블 기반 파싱 시도
    res = try_parse_table(soup, top_n)
    if res:
        return res[:top_n]

    # 2) 카드/리스트 기반 파싱 시도
    res = try_parse_cards(soup, top_n)
    if res:
        return res[:top_n]

    print("[INFO] 자동 파서로 데이터를 찾지 못했습니다. 페이지 구조가 동적이거나 커스텀 클래스일 수 있습니다.")
    return []


def save_csv(items: List[Dict], path: str) -> None:
    if not items:
        print("[WARN] 저장할 데이터가 없습니다.")
        return
    # 모든 키 집합 수집
    keys = set()
    for it in items:
        keys.update(it.keys())
    keys = list(keys)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for it in items:
            writer.writerow(it)
    print(f"[OK] CSV 저장됨: {path}")


def main():
    p = argparse.ArgumentParser(description="KIMPGA 상위 코인 크롤러")
    p.add_argument("--url", default="https://kimpga.com/", help="크롤링 대상 URL")
    p.add_argument("--top", type=int, default=20, help="가져올 상위 개수 (기본 20)")
    p.add_argument("--csv", help="결과를 저장할 CSV 파일 경로")
    p.add_argument("--selenium", action="store_true", help="Selenium을 사용해 렌더된 페이지를 가져옵니다")
    p.add_argument("--driver", help="Selenium 사용시 브라우저 드라이버 경로(선택)")
    args = p.parse_args()

    items = get_top_coins(args.url, top_n=args.top, use_selenium=args.selenium, driver_path=args.driver)
    if not items:
        print("[INFO] 결과가 없습니다. --selenium 옵션을 시도하거나 크롤링 대상의 CSS 셀렉터를 확인하세요.")
        sys.exit(0)

    for i, it in enumerate(items, start=1):
        print(f"{i:2d}: {it}")

    if args.csv:
        save_csv(items, args.csv)


if __name__ == "__main__":
    main()
