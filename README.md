# vowing_data_engieering

# 구조 및 설명

231227 기준

## 폴더 및 그 안의 파일들

- **analyze_extracted_data**: 추출한 메타데이터 혹은 추출한 음성파일을 분석하는 코드가 있는 폴더

  - amr_to_wav.ipynb:
    - '확장자 없는 pcm형식의 amr-wb음성파일(보윙aos 음성파일)' -> wav형식으로 변환
  - analyze_ios_voicemetadata.ipynb:
    - '보윙ios 통합 라벨링데이터'를 읽어 -> 유저,광고별 수동 ETL(추출, 변형, 저장)
  - analyze_multi_voicemetadata.ipynb:
    - '보윙aos 통합 라벨링데이터를 분산한 16개의 라벨링데이터'를 읽어
      -> 데이터분석 작업들
      -> 데이터확인 작업들
      -> voice_id컬럼값으로 음성파일명 바꾸는 작업
      -> user_id컬럼값으로 폴더를 만들어 음성파일들을 넣고 해당하는 라벨링 및 음성데이터 작업들
      -> 월별로만 음성파일들을 분류하여 넣고 해당하는 라벨링 및 음성데이터 작업들
  - analyze_sample_voices.ipynb:
    - 'sample_voice_metadata_230918'을 분석
  - analyze_sheets.ipynb:
    - 구글시트(fs_point_20230801, fs_memo_20230801)를 읽어
      -> 분석하는 작업
  - analyze_structure_of_local.ipynb:
    - 폴더와 파일 구조를 그래픽하게 출력
  - analyze_voicemetadata.ipynb:
    - "integrated_join_operation.ipynb"에서 작업했던 보윙aos 통합데이터들을 읽어
      -> 데이터 정합성 관련 작업들
      -> voice_id 컬럼 생성 및 부여
      -> Training, Validation sets로 데이터셋 분할
      -> 월별 데이터셋 분할
      -> 포인트벌기와 암기플러스 데이터셋 분할
      -> 월별 데이터 추출
      -> 데이터 분포도 및 통계 작업들
  - analyze_xlsx.ipynb:
    - 외장 디스크 데이터 읽어
      -> 데이터 분석
      -> 도표, 그래프 작업
  - read_json.ipynb:
    - 'Firestore>kind_attend>levelDB' 파일들을 읽어 -> JSON 및 적합한 자료형으로 인코딩을 시도했던 코드

- **convert**: 파일변환 소스코드가 있는 폴더

  - convert_protoc_to_txt.ipynb:
    - Protocol Buffers 형식의 메타데이터 파일을 읽어와서 이를 디코드하여 일반 텍스트 형태로 변환하고, 그 결과를 다른 파일에 저장
  - convert_json_to_parquet.ipynb:
    - JSON 파일들을 읽어서 -> 그 내용을 Parquet 파일 형식으로 변환
  - conver_protoc_to_txt.ipynb:
    - Protocol Buffers 형식으로 저장된 메타데이터를 읽어 -> 읽을 수 있는 타입으로 변환하여 저장
  - convert_leveldb.ipynb:
    - levelDB 파일 디코딩 시도했던 코드
  - failed_convert_leveldb.ipynb:
    - levelDB 파일 디코딩 시도했던 코드(2)
  - failed_convert_leveldb_but_read_json.ipynb:
    - levelDB 파일 디코딩 시도했던 코드(3)
  - convert_json_to_csv.py:
    - json 파일들을 csv 파일로 변환
  - firestore_to_csv_or_json.py:
    - Firestore에서 데이터를 가져와 -> CSV 파일로 저장
  - firestore_to_csv_or_sheets.py:
    - Firestore에서 데이터를 가져와
      -> 로컬에 CSV 파일로 저장
      -> (주석 부분)Google Sheets에 추가
  - parquet_to_xlsx.py:
    - parquet 파일들을 읽어서 -> 그 내용을 xlsx 파일 형식으로 변환
  - ssd_to_xlsx.py:
    - 외장 디스크 특정 디렉토리에 있는 파일들을 탐색하여
      -> 특정 형식에 맞는 정보를 추출
      -> 이를 데이터프레임에 저장한 후
      -> 여러 개의 Excel 파일로 분할 저장

- **extracted_data**: 데이터를 추출하는 소스코드가 있는 폴더

  - classification_voicefiles_in_os.ipynb:
    - 보윙ios 라벨링데이터를 읽어
      -> 유저별로 조각난 JSON 데이터 처리
      -> 데이터 병합 및 저장
      -> 데이터 통계 확인
      -> 월별 라벨링 데이터 분리 및 저장
      -> Training, Validation sets로 데이터셋 분할
      -> 음성파일 위치 이동
      -> 뭉테기 라벨링데이터 분류 및 저장
  - extract_data_from_mysql.ipynb:
    - 보윙ios MySQL로부터 데이터 추출
  - extract_s3_voice.ipynb:
    - 보윙ios AWS S3로부터 데이터 추출
      -> 라벨링 데이터 정제
      -> 라벨링 데이터 저장
  - extract_sample_meta_files.ipynb:
    - ETRI 샘플 1만 데이터로부터
      -> (주석)20개 샘플 랜덤 추출
      -> ad_name, user_id 각각 5개를 랜덤하게 뽑아 추출
      -> 결과를 xlsx로 저장
  - extract_voicefiles_from_firebase.ipynb:
    - ETRI 샘플 1만 라벨링데이터를 통해
      -> Firebase를 검색하여 해당하는 음성데이터 추출
      -> SSD를 검색하여 해당하는 음성데이터 추출
      -> 추출 데이터 정합성 검증 작업들
  - extract_voicefiles_from_firebase_by_snapshot.ipynb:
    - 스냅샷 방식과 DASK를 통해 음성데이터 추출 작업 실행시간 단축 시도
  - extract_voicefiles_from_gcs.ipynb:
    - ETRI 샘플 1만 라벨링데이터를 통해
      -> GCS로부터 음성파일 추출
  - test_firestore_direct_read.ipynb:
    - (테스트)Firebase Firestore 데이터베이스에서 데이터를 직접 읽어오는 작업

- **voice_data_queries**: 짧은 분류 전 소스코드들이 있는 폴더
  - change_file_name.py:
    - ETRI 샘플 메타데이터를 읽어 -> 샘플 음성파일명을 voice_id로 변경
  - compare_amr_to_wav.py:
    - 파일명을 비교해 -> amr과 wav간 빠진 항목 찾는 작업
  - convert_json_to_csv.py:
    - 주어진 JSON 파일들을 읽어서 -> CSV 파일 형식으로 변환
  - delete_all_firestore.py:
    - firestore 특정 콜렉션 자료 삭제
  - extract_data_from_hdd_to_xlsx.py:
    - 외장 hdd로부터 데이터를 추출해 xlsx로 저장
  - extract_from_gcs_to_os.py:
    - GCS의 특정 버킷에 저장된 파일들의 이름을 변경
  - firestore_to_csv_or_json.py:
    - 'Users > 유저 문서 > Attend > 모든 문서, 모든 문서 정보'를 google sheets로 이동
  - firestore_to_csv_or_sheets.py:
    - 'Users > 유저 문서 > Attend > 모든 문서, 모든 문서 정보'를 csv파일로 옮김
  - os_delete_files.py:
    - 윈도우 내 특정 디렉토리 안의 csv 파일들을 모두 삭제
  - parquet_to_xlsx.py:
    - parquet 파일들을 읽어서 -> 그 내용을 xlsx 파일 형식으로 변환
  - ref_firestore_to_sheets.py:
    - firestore 데이터를 구글시트로(팀장님 코드)
  - search_file_in_os.py:
    - 윈도우 내 파일 검색해 리스트 추가 및 출력
  - ssd_to_xlsx.py:
    - 외장 디스크의 지정된 디렉토리 내의 파일들을 탐색
      -> 특정 형식의 데이터를 추출
      -> 이를 Excel 파일로 저장
  - test.py:
    - (테스트 코드)
  - test_api.py:
    - (테스트 코드)
  - test_query.py:
    - (테스트 코드)
  - test02.py:
    - (테스트 코드)
  - trans_filename.ipynb:
    - 외장디스크의 폴더 파일명 바꾸는 작업

## 파일들

- dataset_segmentation.ipynb:
  - ETRI 샘플데이터를 가져와
    -> Training, Validation, Test 데이터셋으로 분할, 저장
    -> 데이터 통계 그래프 작업
- integrate_mysql_ios.ipynb:
  - 보윙ios MySQL에서 추출한 데이터들을 조인, 저장
- integrated_join_operation.ipynb:
  - 보윙aos 음성 라벨링데이터 통합과정
- integrated_join_operation_by_csv.ipynb:
  - 보윙aos 음성 라벨링데이터 통합과정 이전 버전
- integrated_join_operation_by_json.ipynb:
  - 보윙aos 음성 라벨링데이터 통합과정 이전 버전(2)
- whats_the_dtype.ipynb:
  - 저장된 데이터파일의 데이터타입 출력
