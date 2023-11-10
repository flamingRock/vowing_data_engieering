import firebase_admin
from firebase_admin import credentials, firestore, storage
import pandas as pd
from datetime import datetime, timedelta


def main(scheduled, context):
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(
            "./samboss-reward-firebase-adminsdk-9j6t2-097005da23.json"
        )
        firebase_admin.initialize_app(cred)
        print("firebase_admin 권한 확인 완료.")

    db = firestore.client()
    bucket = storage.bucket("samboss-reward.appspot.com")

    def backup_collection(collection_name):
        documents = []

        for doc in db.collection(collection_name).stream():
            field_dict = doc.to_dict()
            field_dict["doc_id"] = doc.id
            documents.append(field_dict)

        df = pd.DataFrame(documents).set_index("doc_id")

        nowtime = datetime.now() + timedelta(hours=9)  # UTC->Seoul
        filename = (
            nowtime.strftime("%Y-%m-%d_%H-%M-%S") + "_" + collection_name + ".csv"
        )  # 'CollectionName_YYYY-MM-DD_HH-MM-SS.csv'
        df.to_csv(filename, escapechar="\\")

        # Upload CSV to Firebase Storage
        blob = bucket.blob("backup/" + filename)  # backup 경로에 저장
        blob.upload_from_filename(filename)

    backup_collection("Memorization")
    backup_collection("Point")
    backup_collection("Users")

    firebase_admin.delete_app(firebase_admin.get_app())
