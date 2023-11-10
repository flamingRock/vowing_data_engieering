import os

# 검색할 디렉토리 경로 설정
directory_path = r"E:\\0707\\voicedata\\230517\\d_80\\gcs\\여름이 오기 전 날씬락토페린 300mg!"

# 검색할 문자열 설정
search_string = "0BRBc3jsxpcGlVs98BpO1VSkp2b2"

found_files = []  # To store the paths of found files

# 파일을 찾아 리스트에 추가
found_files = []
for root, dirs, files in os.walk(directory_path):
    print(f"Searching in directory: {root}")  # Debug log
    for file in files:
        print(f"Checking file: {file}")  # Debug log
        if search_string in file:
            full_path = os.path.join(root, file)
            found_files.append(full_path)

# 결과 출력
if found_files:
    print("Files found:")
    for path in found_files:
        print(f"  - {path}")
else:
    print("No files found.")
