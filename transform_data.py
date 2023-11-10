import pandas as pd

# 파일 읽기
df = pd.read_csv("D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/part-00000-b2a2fd5d-507e-4fc4-857f-17f0cf5d963f-c000.csv", error_bad_lines=False)

# "\\"로 시작하는 'ad_script' 수정
df['ad_script'] = df['ad_script'].apply(lambda x: x[1:] if x.startswith("\\") else x)

# 파일 다시 저장
df.to_csv("corrected_part-00000-b2a2fd5d-507e-4fc4-857f-17f0cf5d963f-c000.csv", index=False)
