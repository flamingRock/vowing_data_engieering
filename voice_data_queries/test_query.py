import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, storage

# Firebase SDK 초기화
cred = credentials.Certificate(r'C:\Users\admin\Desktop\voice_data_queries\samboss-reward-firebase-adminsdk-9j6t2-4f53253105.json')  # Replace with the path to your service account key
# 자격 증명(cred)을 사용해 Firebase SDK를 초기화(cred만 넣었을 땐), 뒤에 storageBucket옵션으로 해당 버킷을 파일 저장 및 검색에 사용할 버킷으로 지정
firebase_admin.initialize_app(cred, {'storageBucket': 'samboss-reward.appspot.com'})

# # Firestore client instance를 가져오는 것, firebase DB와 상호작용하기 위함
# db = firestore.client()



# Firebase 저장소에서 bucket은 개체를 저장하기 위한 컨테이너, 파일시스템의 dir 또는 folder와 유사
bucket = storage.bucket()

folder_path = 'ads_test/'
blobs = bucket.list_blobs(prefix=folder_path)

# Extract and print the folder names (prefixes)
# blob을 반복하고 이름이 슬래시(/)로 끝나고 AND /의 수가 하나 더 많은 경우 그 아래 폴더이기에
# Blob 이름을 분할하고 분할에서 마지막에서 두 번째 요소를 검색하여 폴더 이름을 추출
folder_names = set()
for blob in blobs:
    if blob.name.endswith('/') and blob.name.count('/') == folder_path.count('/') + 1:
        folder_name = blob.name.split('/')[-2]
        folder_names.add(folder_name)

# Print the folder names
for folder_name in folder_names:
    print(folder_name)


# bucket = storage.bucket()

# # List files in the "photo" folder
# folder_path = "photo/"
# blobs = bucket.list_blobs(prefix=folder_path)

# # Extract and print the names of the files
# for blob in blobs:
#     file_name = blob.name.split("/")[-1]
#     print(file_name)