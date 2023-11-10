import os
# import gspread_pandas
# import gspread
# import gspread_dataframe as gd
from google.api_core.retry import Retry
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from oauth2client.service_account import ServiceAccountCredentials
# from google.auth.transport.requests import AuthorizedSession
import pandas as pd

# 이 py 스크립트가 실행되는 디렉토리에서 Firebase 서비스 계정 키를 찾고, 'GOOGLE~' 환경 변수(Google Cloud API 사용에 필요) 설정
script_dir = os.path.dirname(os.path.realpath(__file__))    # os.path.realpath(__file__)는 현재 실행 중인 py스크립트의 절대 경로를 반환
cred_path = os.path.join(script_dir, 'samboss-reward-firebase-adminsdk-9j6t2-097005da23.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path    # os.environ은 환경 변수를 다루는 데 사용되는 Python의 내장 객체 

# Firebase initialize
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("firebase_admin 권한 확인 완료.")

db = firestore.Client()

# 로컬에서 저장할 파일 경로
# csv_file_path = 'D:/DATA_PREPROCESS/FIRESTORE_DATAS/users_data.csv'
csv_file_path = 'D:/DATA_PREPROCESS/FIRESTORE_DATAS/attend_data.csv'

# Users > 유저 문서 > Attend > 모든 문서, 모든 문서 정보를 google sheets로 옮김
def get_all_documents_in_collection(collection_name):
    try:
        users_ref = db.collection(collection_name)
        batch_size = 1000
        data = []
        last_document = None
        
        # retry object에 timeout 설정
        retry_policy = Retry(deadline=1800)

        while True:
            # `start_after`를 사용하여 마지막 문서 이후의 문서들을 가져옵니다.
            if last_document:
                users_batch = users_ref.limit(batch_size).start_after(last_document).stream(retry=retry_policy)
            else:
                users_batch = users_ref.limit(batch_size).stream(retry=retry_policy)
            
            batch_data = []
            for user_doc in users_batch:
                user_id = user_doc.id
                user_ref = db.collection('Users').document(user_id)

                attend_ref = user_ref.collection('Attend')
                for attend_doc in attend_ref.stream():
                    row = attend_doc.to_dict()
                    row['user_id'] = user_id
                    row['attend_id'] = attend_doc.id
                    batch_data.append(row)
            
            if not batch_data:
                break
            
            data.extend(batch_data)
            
            # 마지막 문서를 저장합니다.
            last_document = user_doc

            df = pd.DataFrame(data)

            # # 변경하고 싶은 컬럼들을 리스트로 만듭니다.
            # columns_to_change = ['ArrayVoice', 'addText', 'name', 'ArrayPercent', 'ArrayDate', 'ArrayAddResult']

            # # 각 컬럼에 대해 쉼표를 공백으로 변경합니다.
            # for col in columns_to_change:
            #     df[col] = df[col].str.replace(',', ' ')

            # CSV형식으로 Append
            df.to_csv(csv_file_path, mode='a', index=False, header=(last_document is None), encoding='utf-8', escapechar='\\')

    except Exception as e:
        import traceback
        traceback.print_exc() 
        print(f"Error: {e}")

def get_all_documents_in_users(collection_name):
    try:
        users_ref = db.collection(collection_name)
        data = []
        # count = 0

        for user_doc in users_ref.stream():
            user_data = user_doc.to_dict()
            user_data['user_id'] = user_doc.id
            data.append(user_data)
            
            # count += 1
            # if count >= 10: break

        df = pd.DataFrame(data)

        # # 변경하고 싶은 컬럼들을 리스트로 만듭니다.
        # columns_to_change = ['address', 'detailAddress']

        # # 각 컬럼에 대해 쉼표를 공백으로 변경합니다.
        # for col in columns_to_change:
        #     df[col] = df[col].str.replace(',', ' ')

        df.to_csv(csv_file_path, index=False, encoding='utf-8', escapechar='\\', quoting=1)    # 특수 문자가 있는 문자열을 이스케이프 처리
        print(f"Data saved to {csv_file_path}")

    except Exception as e:
        print(f"Error: {e}")

collection_name = "Users"  # Replace with your actual collection name
get_all_documents_in_collection(collection_name)
# get_all_documents_in_users(collection_name)