import os
# import gspread_pandas
import gspread
import gspread_dataframe as gd
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

# Google Sheets API에 연결하고 인증
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('samboss-reward-394470968e63.json', scope)  # change the path to the actual json file
client = gspread.authorize(creds)

# Firebase initialize
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("firebase_admin 권한 확인 완료.")

db = firestore.Client()


# Google Sheet를 해당 타겟 시트로 할당
spreadsheet_id = '1fstoqfCCyIv38D4ZOxicoDdIaLhcfuXOf_9yn-ijn_U'  # replace with your Google Sheets ID
worksheet = client.open_by_key(spreadsheet_id).sheet1  # assuming you want to write to the first sheet

# # 콜렉션 안의 모든 문서 정보를 구글 시트에 넣음
# def get_all_documents_in_collection(collection_name):
#     try:
#         # Reference to the collection
#         collection_ref = db.collection(collection_name)

#         # Get all documents in the collection
#         docs = collection_ref.get()

#         # Process the documents and add them to the Google Sheet
#         data = []
#         for doc in docs:
#             row = doc.to_dict()
#             row['id'] = doc.id  # add the document ID
#             data.append(row)
#         df = pd.DataFrame(data)

#         # Sort the DataFrame by column names
#         df = df.sort_index(axis=1)

#         # Add the DataFrame to the Google Sheet
#         gd.set_with_dataframe  (worksheet, df, include_column_header=True)

    # except Exception as e:
    #     import traceback
    #     traceback.print_exc() 
    #     print(f"Error: {e}")

# Users > 유저 문서 > Attend > 모든 문서, 모든 문서 정보를 csv파일로 옮김
def get_all_documents_in_collection(collection_name):
    try:
        # Reference to the Users collection
        users_ref = db.collection(collection_name)

        # Iterate through each user document
        data = []
        for user_doc in users_ref.stream():
            user_id = user_doc.id
            user_ref = db.collection('Users').document(user_id)  # Get the document reference
            
            # Reference to the Attend collection inside the user's document
            attend_ref = user_ref.collection('Attend')
            if attend_ref.limit(1).get():  # Check if there's at least one document

                # Iterate through each attend document
                for attend_doc in attend_ref.stream():
                    row = attend_doc.to_dict()
                    row['user_id'] = user_id  # Add the user ID
                    row['attend_id'] = attend_doc.id  # Add the attend document ID
                    data.append(row)

        df = pd.DataFrame(data)

        # Write the DataFrame to a CSV file
        df.to_csv('C:/Users/admin/Desktop/attend_data.csv', index=False, escapechar='\\')

    except Exception as e:
        import traceback
        traceback.print_exc() 
        print(f"Error: {e}")

# Call the function with your collection name
collection_name = "Users"  # Replace with your actual collection name
get_all_documents_in_collection(collection_name)