import os

input_folder = "D:/DATA_PREPROCESS/FIRESTORE_DATAS/sample_voice_metadata_230918/VOICE_FILES"
output_folder = "D:\\DATA_PREPROCESS\\FIRESTORE_DATAS\\sample_voice_metadata_230918\\WAV_FILES"

# amr 파일명 리스트 생성
amr_files = [f for f in os.listdir(input_folder) if not '.' in f]

# wav 파일명 리스트 생성
wav_files = [f for f in os.listdir(output_folder) if f.lower().endswith('.wav')]

# amr 파일명은 확장자가 없으므로 별도의 처리 없이 그대로 사용
amr_names = [f for f in amr_files]

# wav 파일명에서 .wav 제거
wav_names = [os.path.splitext(f)[0] for f in wav_files]

# wav에는 있지만 amr에는 없는 파일명 찾기
why_in_files = [name for name in wav_names if name not in amr_names]

# amr에는 있지만 wav에는 없는 파일명 찾기
missing_files = [name for name in amr_names if name not in wav_names]


# Set으로 변환
amr_set = set(amr_names)
wav_set = set(wav_names)

# 차집합을 이용하여 빠진 항목 찾기
missing_files = amr_set - wav_set  # amr에는 있지만 wav에는 없는 항목
why_in_files = wav_set - amr_set  # wav에는 있지만 amr에는 없는 항목

print("Number of Why in Files: ", len(why_in_files))
print("Number of Missing Files: ", len(missing_files))