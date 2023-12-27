import os
import pandas as pd

# 1. Excel 파일을 읽어서 DataFrame으로 변환
file_path = 'D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/for_search_metadata_230920.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# 원본 폴더 경로 설정
source_folder = 'D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/WAV_FILES'

# 2. 각 행에서 user_id, ad_name, voice_id를 추출
for index, row in df.iterrows():
    user_id = row['user_id']
    ad_name = row['ad_name']
    voice_id = row['voice_id']
    
    # 3. 원본 폴더에서 해당하는 파일을 검색
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_user_id = file[:28]  # 첫 28글자는 user_id
            file_ad_name = file[29:].rsplit('.', 1)[0]  # '_' 뒤는 ad_name, 확장자 전까지
            
            # 4. 검색된 파일의 이름을 voice_id.wav 형식으로 변경
            if file_user_id == user_id and file_ad_name == ad_name:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(root, f"{voice_id}.wav")
                os.rename(src_path, dest_path)
