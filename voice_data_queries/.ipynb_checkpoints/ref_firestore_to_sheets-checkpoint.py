import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import gspread
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials

def main(request, _):
    # Firebase admin계정 확인
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("./samboss-reward-c3d0250e9493.json")
        firebase_admin.initialize_app(cred)
        # print("firebase_admin 권한 확인 완료.")

    # Firestore 클라이언트 생성
    db = firestore.client()

    # 빈 DataFrame 생성
    account_df = pd.DataFrame()

    # WithdrawalRecord 컬렉션에서 "fail" 상태의 문서 가져오기
    for doc in db.collection("WithdrawalRecord").stream():
        field_dict = doc.to_dict()
        document_id = doc.id

        if field_dict["state"] == "fail":  # "fail" 상태의 문서만 가져오기
            field_dict["document_id"] = document_id
            account_df = pd.concat(
                [
                    account_df,
                    pd.DataFrame(data=[field_dict.values()], columns=field_dict.keys()),
                ],
                ignore_index=True,
            )

    # 원하는 열 순서로 DataFrame 재정렬
    desired_columns_order = [
        "document_id",
        "imageUrl",
        "uid",
        "state",
        "date",
        "bank",
        "accountNumber",
        "amount",
        "name",
    ]
    account_df = account_df[desired_columns_order]
    account_df.head()

    # 유사도 계산식
    def calculate_similarity(array_date_a, array_date_b):
        if array_date_a == array_date_b:
            return 1  # 완전히 동일
        else:
            return 0  # 다름
        
    # 유사도검사 과정 추가
    def compare_documents(uid1, uid2):
        # print(f"Comparing {uid1} and {uid2} ...")
        collection_a = db.collection(f"Users/{uid1}/Attend").get()
        collection_b = db.collection(f"Users/{uid2}/Attend").get()
        
        a_documents = {doc.id: doc.to_dict() for doc in collection_a}
        b_documents = {doc.id: doc.to_dict() for doc in collection_b}

        # 겹치는 문서 수 및 유사도 합 계산
        overlapping_documents = 0  # 겹치는 문서 수 초기화
        similarity_sum = 0  # 유사도 합 초기화
        for a_doc_id, a_doc_data in a_documents.items():
            if a_doc_id in b_documents:
                overlapping_documents += 1  # 겹치는 문서 수 증가
                b_doc_data = b_documents[a_doc_id]
                # 'ArrayDate' 필드 추출
                array_date_a = a_doc_data.get("ArrayDate")
                array_date_b = b_doc_data.get("ArrayDate")

                # 유사도 계산
                similarity = calculate_similarity(array_date_a, array_date_b)
                similarity_sum += similarity  # 유사도 합 계산

        if overlapping_documents > 0:
            similarity_average = (similarity_sum / overlapping_documents) * 100
            similarity_average = round(similarity_average, 2)
            return f"{similarity_average}%"  # 결과 반환, 백분율 형식

        return None  # 겹치는 문서가 없는 경우

    # 이름 또는 계좌 번호별로 uid를 그룹화
    uid_groups = {}
    for i, row in account_df.iterrows():
        key = (row['name'], row['accountNumber'])
        if key not in uid_groups:
            uid_groups[key] = []
        uid_groups[key].append(row['uid'])

    # 유사도 열 추가
    account_df['similarity'] = None

    # 각 그룹별로 모든 uid 조합에 대해 유사도를 계산
    for group in uid_groups.values():
        if len(group) < 2:
            continue  # 적어도 2개의 uid가 필요

        for i, uid1 in enumerate(group):
            for j, uid2 in enumerate(group):
                if i >= j or uid1 == uid2:  # 같은 UID를 비교하거나 이미 비교한 UID를 제외
                    continue

                #print(f"Comparing {uid1} and {uid2}")
                # 두 uid에 대해 문서 비교 수행
                similarity_percentage = compare_documents(uid1, uid2)

                # 유사도 결과 저장
                account_df.loc[account_df['uid'] == uid1, 'similarity'] = similarity_percentage
                account_df.loc[account_df['uid'] == uid2, 'similarity'] = similarity_percentage
                #print(f"Similarity percentage: {similarity_percentage}")

    # 시트권한 설트
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./logical-zephyr-388308-03c2dd5ea9e4.json', scope)
    client = gspread.authorize(creds)

    # 시트 열기
    sheet_key = '1ydyprGMXnj5OyyG3PJfXGa9o45QKBqWvrz9qj8whcUE'
    sheet_name = 'auto'
    worksheet = client.open_by_key(sheet_key).worksheet(sheet_name)

    # DataFrame을 스프레드시트에 쓰기
    gd.set_with_dataframe(worksheet, account_df)