from google.cloud import storage

def rename_files(bucket_name):
    # GCS 클라이언트 초기화
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # 버킷 내의 모든 파일(블롭)을 반복
    for blob in bucket.list_blobs():
        # 파일 이름에서 ':'를 '_'로 변경
        new_name = blob.name.replace(':', '_')
        if new_name != blob.name:
            # 이름이 변경된 경우, 파일(블롭)을 새 이름으로 이동
            bucket.rename_blob(blob, new_name)
            print(f'Renamed {blob.name} to {new_name}')

# 버킷 이름을 여기에 입력하세요
bucket_name = 'your-bucket-name'
rename_files(bucket_name)



# 아직 검증 전 코드들 사용 전 체크해서 적용