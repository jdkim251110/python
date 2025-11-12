import sqlite3
from typing import List, Tuple
import random
import string

class ProductDatabase:
    """SQLite를 사용한 전자제품 데이터베이스 관리 클래스"""
    
    def __init__(self, db_name: str = "MyProduct.db"):
        """
        데이터베이스 초기화
        
        Args:
            db_name: 데이터베이스 파일명 (기본값: MyProduct.db)
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """데이터베이스 연결"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ 데이터베이스 '{self.db_name}' 연결 성공")
        except sqlite3.Error as e:
            print(f"✗ 데이터베이스 연결 실패: {e}")
    
    def create_table(self):
        """Products 테이블 생성"""
        try:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS Products (
                productID INTEGER PRIMARY KEY AUTOINCREMENT,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            )
            """
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("✓ Products 테이블 생성/확인 완료")
        except sqlite3.Error as e:
            print(f"✗ 테이블 생성 실패: {e}")
    
    def insert(self, product_name: str, product_price: int) -> bool:
        """
        단일 제품 데이터 삽입
        
        Args:
            product_name: 제품명
            product_price: 제품가격
            
        Returns:
            성공 여부
        """
        try:
            insert_sql = """
            INSERT INTO Products (productName, productPrice)
            VALUES (?, ?)
            """
            self.cursor.execute(insert_sql, (product_name, product_price))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ 데이터 삽입 실패: {e}")
            return False
    
    def insert_many(self, products: List[Tuple[str, int]]) -> int:
        """
        여러 제품 데이터 일괄 삽입
        
        Args:
            products: [(제품명, 가격), ...] 형태의 리스트
            
        Returns:
            삽입된 행의 개수
        """
        try:
            insert_sql = """
            INSERT INTO Products (productName, productPrice)
            VALUES (?, ?)
            """
            self.cursor.executemany(insert_sql, products)
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"✗ 대량 데이터 삽입 실패: {e}")
            return 0
    
    def select_all(self) -> List[Tuple]:
        """
        모든 제품 데이터 조회
        
        Returns:
            모든 제품 데이터의 리스트
        """
        try:
            select_sql = "SELECT * FROM Products"
            self.cursor.execute(select_sql)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return []
    
    def select_by_id(self, product_id: int) -> Tuple:
        """
        ID로 제품 조회
        
        Args:
            product_id: 제품 ID
            
        Returns:
            조회된 제품 데이터
        """
        try:
            select_sql = "SELECT * FROM Products WHERE productID = ?"
            self.cursor.execute(select_sql, (product_id,))
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"✗ ID별 데이터 조회 실패: {e}")
            return None
    
    def select_by_name(self, product_name: str) -> List[Tuple]:
        """
        제품명으로 제품 조회
        
        Args:
            product_name: 제품명
            
        Returns:
            조회된 제품 데이터 리스트
        """
        try:
            select_sql = "SELECT * FROM Products WHERE productName LIKE ?"
            self.cursor.execute(select_sql, (f"%{product_name}%",))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ 제품명별 데이터 조회 실패: {e}")
            return []
    
    def select_by_price_range(self, min_price: int, max_price: int) -> List[Tuple]:
        """
        가격 범위로 제품 조회
        
        Args:
            min_price: 최소 가격
            max_price: 최대 가격
            
        Returns:
            조회된 제품 데이터 리스트
        """
        try:
            select_sql = "SELECT * FROM Products WHERE productPrice BETWEEN ? AND ?"
            self.cursor.execute(select_sql, (min_price, max_price))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ 가격범위 데이터 조회 실패: {e}")
            return []
    
    def update(self, product_id: int, product_name: str = None, product_price: int = None) -> bool:
        """
        제품 정보 수정
        
        Args:
            product_id: 제품 ID
            product_name: 수정할 제품명 (None이면 수정 안함)
            product_price: 수정할 가격 (None이면 수정 안함)
            
        Returns:
            성공 여부
        """
        try:
            if product_name is not None:
                update_sql = "UPDATE Products SET productName = ? WHERE productID = ?"
                self.cursor.execute(update_sql, (product_name, product_id))
            
            if product_price is not None:
                update_sql = "UPDATE Products SET productPrice = ? WHERE productID = ?"
                self.cursor.execute(update_sql, (product_price, product_id))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ 데이터 수정 실패: {e}")
            return False
    
    def delete(self, product_id: int) -> bool:
        """
        제품 데이터 삭제
        
        Args:
            product_id: 제품 ID
            
        Returns:
            성공 여부
        """
        try:
            delete_sql = "DELETE FROM Products WHERE productID = ?"
            self.cursor.execute(delete_sql, (product_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ 데이터 삭제 실패: {e}")
            return False
    
    def delete_all(self) -> bool:
        """
        모든 제품 데이터 삭제
        
        Returns:
            성공 여부
        """
        try:
            delete_sql = "DELETE FROM Products"
            self.cursor.execute(delete_sql)
            self.conn.commit()
            print(f"✓ 모든 데이터 삭제 완료")
            return True
        except sqlite3.Error as e:
            print(f"✗ 전체 데이터 삭제 실패: {e}")
            return False
    
    def get_total_count(self) -> int:
        """
        전체 제품 개수 조회
        
        Returns:
            제품 개수
        """
        try:
            count_sql = "SELECT COUNT(*) FROM Products"
            self.cursor.execute(count_sql)
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"✗ 데이터 개수 조회 실패: {e}")
            return 0
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            print("✓ 데이터베이스 연결 종료")


def generate_sample_products(count: int = 100000) -> List[Tuple[str, int]]:
    """
    샘플 제품 데이터 생성
    
    Args:
        count: 생성할 제품 개수 (기본값: 100000)
        
    Returns:
        [(제품명, 가격), ...] 형태의 제품 리스트
    """
    categories = [
        "노트북", "데스크탑", "모니터", "마우스", "키보드",
        "헤드폰", "스피커", "웹캠", "프린터", "라우터",
        "태블릿", "스마트폰", "이어폰", "충전기", "케이블"
    ]
    
    brands = [
        "삼성", "LG", "애플", "소니", "델",
        "에이수스", "레노버", "HP", "MSI", "ASUS"
    ]
    
    products = []
    for i in range(count):
        category = random.choice(categories)
        brand = random.choice(brands)
        model = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        product_name = f"{brand} {category} {model}"
        
        # 가격 범위: 10,000원 ~ 3,000,000원
        product_price = random.randint(10000, 3000000)
        
        products.append((product_name, product_price))
    
    return products


if __name__ == "__main__":
    # 데이터베이스 초기화
    db = ProductDatabase("MyProduct.db")
    
    # 기존 데이터 확인
    print(f"\n[현재 데이터 개수] {db.get_total_count()}")
    
    # 기존 데이터가 있으면 삭제
    if db.get_total_count() > 0:
        print("\n기존 데이터를 삭제합니다...")
        db.delete_all()
    
    # 샘플 데이터 생성 및 삽입
    print("\n10만개의 샘플 데이터를 생성 중입니다...")
    sample_products = generate_sample_products(100000)
    
    print("데이터베이스에 삽입 중입니다...")
    inserted_count = db.insert_many(sample_products)
    print(f"✓ {inserted_count}개의 데이터가 삽입되었습니다.\n")
    
    # INSERT 테스트 - 단일 삽입
    print("=" * 60)
    print("[INSERT 테스트]")
    print("=" * 60)
    result = db.insert("삼성 갤럭시 Z 폴드5", 2500000)
    print(f"단일 데이터 삽입: {'성공' if result else '실패'}\n")
    
    # SELECT 테스트 - 전체 조회
    print("=" * 60)
    print("[SELECT 테스트]")
    print("=" * 60)
    print(f"\n전체 데이터 개수: {db.get_total_count()}개\n")
    
    # SELECT 테스트 - ID로 조회
    print("▶ ID로 조회 (ID=1):")
    result = db.select_by_id(1)
    if result:
        print(f"  ID: {result[0]}, 제품명: {result[1]}, 가격: {result[2]:,}원\n")
    
    # SELECT 테스트 - 제품명으로 조회
    print("▶ 제품명으로 조회 (검색: '삼성'):")
    results = db.select_by_name("삼성")
    print(f"  검색 결과: {len(results)}개")
    for i, result in enumerate(results[:3]):  # 처음 3개만 출력
        print(f"  {i+1}. ID: {result[0]}, 제품명: {result[1]}, 가격: {result[2]:,}원")
    if len(results) > 3:
        print(f"  ... 외 {len(results)-3}개\n")
    else:
        print()
    
    # SELECT 테스트 - 가격 범위로 조회
    print("▶ 가격 범위로 조회 (50만원~100만원):")
    results = db.select_by_price_range(500000, 1000000)
    print(f"  검색 결과: {len(results)}개")
    for i, result in enumerate(results[:3]):  # 처음 3개만 출력
        print(f"  {i+1}. ID: {result[0]}, 제품명: {result[1]}, 가격: {result[2]:,}원")
    if len(results) > 3:
        print(f"  ... 외 {len(results)-3}개\n")
    else:
        print()
    
    # UPDATE 테스트
    print("=" * 60)
    print("[UPDATE 테스트]")
    print("=" * 60)
    print("ID=2 제품 정보 수정 전:")
    result = db.select_by_id(2)
    if result:
        print(f"  ID: {result[0]}, 제품명: {result[1]}, 가격: {result[2]:,}원")
    
    db.update(2, product_name="LG 울트라와이드 모니터 34인치", product_price=800000)
    
    print("ID=2 제품 정보 수정 후:")
    result = db.select_by_id(2)
    if result:
        print(f"  ID: {result[0]}, 제품명: {result[1]}, 가격: {result[2]:,}원\n")
    
    # DELETE 테스트
    print("=" * 60)
    print("[DELETE 테스트]")
    print("=" * 60)
    print(f"삭제 전 데이터 개수: {db.get_total_count()}개")
    
    # ID=100 삭제
    db.delete(100)
    print(f"ID=100 데이터 삭제 완료")
    print(f"삭제 후 데이터 개수: {db.get_total_count()}개\n")
    
    # 통계 정보
    print("=" * 60)
    print("[통계 정보]")
    print("=" * 60)
    all_products = db.select_all()
    if all_products:
        prices = [p[2] for p in all_products]
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        print(f"총 제품 개수: {len(all_products):,}개")
        print(f"평균 가격: {avg_price:,.0f}원")
        print(f"최저 가격: {min_price:,}원")
        print(f"최고 가격: {max_price:,}원\n")
    
    # 데이터베이스 연결 종료
    db.close()
