import os
import pandas as pd
from tqdm import tqdm   # 진행률 표시줄 라이브러리

# dataframe 초기화
df = pd.DataFrame(columns=['accuracy', 'ad_name', 'record_time', 'user_id', 'gender', 'birth_year', 'local_code', 'is_test'])

# # 정보를 뽑아내는 디렉토리 지정, hdd > 230517 > d_80 기준
# root_dir = 'D:/to_230517_voicedata_all/230517/d_80/gcs'
# parts = root_dir.split('/')
# extracted_path = "_".join(parts[3:5])   # d_80_gcs
# accuracy = 80   # 정확도

# 정보를 뽑아내는 디렉토리 지정, ssd > 230517 > d_80 기준
root_dir = 'E:/0707/voicedata/230517/d_95/firebase'
parts = root_dir.split('/')
extracted_path = "_".join(parts[3:5])   # d_95_firebase
accuracy = 95   # 정확도


# count for test
count = 5000

# root_dir 폴더 탐색
for dir_name in  tqdm(os.listdir(root_dir), desc="Processing dir"):
    print(f'\tdir name: {dir_name}')

    ad_name = dir_name.split('/')[-1]
    dir_path = os.path.join(root_dir, dir_name)
    
    # 폴더인지 확인
    if not os.path.isdir(dir_path):
        break
    else:
        # 각각의 폴더마다 루프, 반복자는 파일명
        for f_name in os.listdir(dir_path):

            # # hdd > 230517 > d_80의 폴더파일 형식 관련
            # # 파일명이 46글자보다 작거나 48글자보다 크거나 확장자가 있다면 제외
            # if len(f_name) > 48 or len(f_name) < 46 or '.' in f_name:
            #     continue
            # if len(f_name) == 48:
            #     record_time = f_name[:14]  # 첫 14 문자
            #     user_id = f_name[14:42]  # 다음 28 문자
            #     gender = f_name[43]  # 다음 '_' 뒤 문자
            #     birth = f_name[44:46]  # 다음 2 문자
            #     local_code = f_name[46:48]  # 다음 2 문자
            #     is_test = 0     # 테스트용 음성데이터인지
            # if len(f_name) == 46:
            #     record_time = f_name[:14]  # 첫 14 문자
            #     user_id = f_name[14:42]  # 다음 28 문자
            #     gender = f_name[43]  # 다음 '_' 뒤 문자
            #     birth = f_name[44:46]  # 다음 2 문자
            #     local_code = None  # 다음 2 문자
            #     is_test = 0     # 테스트용 음성데이터인지


            # ssd > 230517 > d_95의 폴더파일 형식 관련
            # 파일명이 46글자보다 작거나 48글자보다 크거나 확장자가 있다면 제외
            if len(f_name) > 48 or len(f_name) < 46 or '.' in f_name:
                continue
            if len(f_name) == 48:
                record_time = f_name[:14]  # 첫 14 문자
                user_id = f_name[14:42]  # 다음 28 문자
                gender = f_name[43]  # 다음 '_' 뒤 문자
                birth = f_name[44:46]  # 다음 2 문자
                local_code = f_name[46:48]  # 다음 2 문자
                is_test = 0     # 테스트용 음성데이터인지
            if len(f_name) == 46:
                record_time = f_name[:14]  # 첫 14 문자
                user_id = f_name[14:42]  # 다음 28 문자
                gender = f_name[43]  # 다음 '_' 뒤 문자
                birth = f_name[44:46]  # 다음 2 문자
                local_code = None  # 다음 2 문자
                is_test = 0     # 테스트용 음성데이터인지

            if birth <= 20:
                print(f_name)

            # if local_code == 'EE' or dir_name[:3].isdigit():
            #     is_test = 1
        
            # new_row = pd.DataFrame({
            #     'accuracy': [accuracy],
            #     'ad_name': [ad_name],
            #     'record_time': [record_time],
            #     'user_id': [user_id],
            #     'gender': [gender],
            #     'birth_year': [birth],
            #     'local_code': [local_code],
            #     'is_test': [is_test]
            # })
            
            # df = pd.concat([df, new_row], ignore_index=True)

            count -= 1
            if count <= 0: break
    if count <= 0: break

# dataframe울 excel 파일로 저장
# 파일 크기가 100만을 넘어가면 새 엑셀파일을 만들어서 넣도록 만들기
chunks = [df[i:i+1000000] for i in range(0,df.shape[0],1000000)]

for i, chunk in enumerate(chunks, 1):
    chunk.to_excel(f'C:/Users/admin/Desktop/{extracted_path}_extracted_ssd_d95_data_{i}.xlsx', index=False)