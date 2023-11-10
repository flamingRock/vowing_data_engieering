import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
cred_path = os.path.join(script_dir, 'samboss-reward-firebase-adminsdk-9j6t2-4f53253105.json')
# GOOGLE_APPLICATION_CREDENTIALS 환경 변수를 JSON 파일의 경로로 설정
# -> google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials 오류 해결
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

# Firebase initialize
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("firebase_admin 권한 확인 완료.")

db = firestore.Client()


# [START firestore_data_delete_collection]
def delete_collection(coll_ref, batch_size):
    # docs = coll_ref.list_documents(page_size=batch_size)  # google cloud client library를 사용할 때
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f"Deleting doc {doc.id} => {doc.to_dict()}")
        # doc.delete()
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)
    # [END firestore_data_delete_collection]

kind_users_collection_red = db.collection("2023-08-10T09:01:35_26468").document("all_namespaces").collection("kind_Users")
delete_collection(kind_users_collection_red, 10)