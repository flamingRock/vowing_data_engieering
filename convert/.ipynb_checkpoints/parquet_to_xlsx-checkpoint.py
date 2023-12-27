import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# # Parquet 파일 읽기
# df = pq.read_table('D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/public_sample_voice_metadata_230920/public_sample_voice_metadata_230920.parquet').to_pandas()

# # Excel 파일로 저장
# df.to_excel('D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/public_sample_voice_metadata_230920/public_sample_voice_metadata_230920.xlsx', index=False)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# # Excel 파일을 읽어서 DataFrame으로 변환
# df = pd.read_excel('D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/for_search_metadata_230920.xlsx', engine='openpyxl')
# df.to_parquet('D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/for_search_metadata_230920.parquet')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


# file_path = 'D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/SAMPLES/for_search_sample_230920.xlsx'
# df = pd.read_excel(file_path)

# df = df.drop(columns=['user_id'])

# save_path = 'D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/SAMPLES/public_sample_voice_metadata_230920.xlsx'
# df.to_excel(save_path, index=False)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

df = pq.read_table('D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/public_sample_voice_metadata_230920.parquet').to_pandas()

# DataFrame 'df'의 'video_id' 컬럼명을 'voice_id'로 변경
df.rename(columns={'video_id': 'voice_id'}, inplace=True)

# 새로운 파일명으로 DataFrame을 Parquet 파일로 저장
new_file_path = 'D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/new_public_sample_voice_metadata_230920.parquet'
df.to_parquet(new_file_path, index=False)