import os

# 매개변수로 전해진 디렉토리 안의 csv 파일들을 모두 삭제하는 메서드
def delete_csv_files_in_directory(directory_path):
    # 지정된 디렉토리 내의 모든 파일을 나열한다.
    files_in_directory = os.listdir(directory_path)
    
    # 각 파일에 대해 확장자가 .csv인 경우 삭제한다.
    for filename in files_in_directory:
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            os.remove(file_path)
            print(f"Deleted {file_path}")

directory_path = "D:\\DATA_PREPROCESS\\FIRESTORE_DATAS\\USERS"
delete_csv_files_in_directory(directory_path)