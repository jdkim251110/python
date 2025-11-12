import os
import shutil
from pathlib import Path
from datetime import datetime, date

# 다운로드 폴더 경로
DOWNLOADS_FOLDER = r"C:\Users\student\Downloads"

# 파일 분류 규칙
FILE_CATEGORIES = {
    r"\images": [".jpg", ".jpeg"],
    r"\data": [".csv", ".xlsx"],
    r"\docs": [".txt", ".doc", ".pdf"],
    r"\archive": [".zip"]
}

def create_folders():
    """필요한 폴더가 없으면 생성"""
    for folder in FILE_CATEGORIES.keys():
        folder_path = DOWNLOADS_FOLDER + folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"✓ 폴더 생성: {folder_path}")

def get_file_category(filename):
    """파일 확장자에 따라 해당 카테고리 반환"""
    file_ext = Path(filename).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if file_ext in extensions:
            return category
    return None

def is_today_file(file_path):
    """파일의 수정 날짜가 오늘인지 확인"""
    file_mtime = os.path.getmtime(file_path)
    file_date = datetime.fromtimestamp(file_mtime).date()
    today_date = date.today()
    return file_date == today_date

def organize_downloads():
    """다운로드 폴더의 파일을 분류하여 이동"""
    try:
        # 폴더 생성
        create_folders()
        print("\n파일 이동 시작...\n")
        
        # 다운로드 폴더의 모든 파일 확인
        moved_count = 0
        for filename in os.listdir(DOWNLOADS_FOLDER):
            file_path = os.path.join(DOWNLOADS_FOLDER, filename)
            
            # 폴더는 건너뛰기
            if os.path.isdir(file_path):
                continue
            
            # 오늘 날짜 파일만 확인
            if not is_today_file(file_path):
                continue
            
            # 파일 카테고리 확인
            category = get_file_category(filename)
            
            if category:
                # 목표 폴더 경로
                dest_folder = DOWNLOADS_FOLDER + category
                dest_path = os.path.join(dest_folder, filename)
                
                # 파일 이동
                shutil.move(file_path, dest_path)
                print(f"✓ 이동: {filename} → {category}")
                moved_count += 1
        
        print(f"\n오늘 날짜({date.today()})의 총 {moved_count}개 파일이 이동되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    organize_downloads()
