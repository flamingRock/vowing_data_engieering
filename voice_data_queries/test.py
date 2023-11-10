import os
import json

directory = "D:\\DATA_PREPROCESS\\FIRESTORE_DATAS\\USERS"
file_names = [f for f in os.listdir(directory) if f.startswith('output-') and f.endswith('.json')]


#------------------------------------------------ 참고 코드 ------------------------------------------------------------------------#
# Part 2: 행 비교 및 분석
def row_comparison_analysis():
    if not os.path.exists('./data/'):
        os.makedirs('./data/')

    # CSV 파일 읽기, 경로지정
    data = pd.read_csv('./output.csv')
    total_length = len(data)
    part_size = total_length // NUM_PARTS

    def process_part(part_number, start_index, end_index, data, pool):
        args = [(indexA, rowA, data) for indexA, rowA in data.iloc[start_index:end_index].iterrows()]
        results = list(tqdm(pool.imap(compare_rows, args), total=end_index - start_index, desc=f"Processing part {part_number}"))

        print(f"Processing part {part_number}: {len(results)} results found.")  # 디버깅 출력 추가

        result_filename = f'./data/result_part_{part_number}.csv'
        with open(result_filename, 'w', newline='', encoding='utf-8') as result_file:
            writer = csv.writer(result_file)
            writer.writerow(["문서A", "세부A", "문서B", "세부B", "겹친 개수"])  # 헤더 작성
            for result_set in results:
                for result in result_set:
                    writer.writerow(result)

        print(f"Saved results to {result_filename}.")  # 디버깅 출력 추가

    # 작업의 진행 상황을 저장/로드
    def save_progress(part_number):
        with open('./data/progress.txt', 'w') as file:
            file.write(str(part_number))

    def load_progress():
        if os.path.exists('./data/progress.txt'):
            with open('./data/progress.txt', 'r') as file:
                return int(file.read().strip())
        return 0  # 진행 상황 파일이 없으면 처음부터 시작

    data = pd.read_csv('./output.csv')
    total_length = len(data)
    part_size = total_length // NUM_PARTS
    """
    last_completed_part = load_progress()
    with Pool(processes=4) as pool:
        for part_number in range(last_completed_part, NUM_PARTS):
            start_index = part_number * part_size
            end_index = (part_number + 1) * part_size if part_number < NUM_PARTS - 1 else total_length
            process_part(part_number, start_index, end_index, data, pool)"""

    if __name__ == '__main__':
        with Pool(processes=4) as pool:
            last_completed_part = load_progress()
            for part_number in range(last_completed_part, NUM_PARTS):
                start_index = part_number * part_size
                end_index = (part_number + 1) * part_size if part_number < NUM_PARTS - 1 else total_length
                process_part(part_number, start_index, end_index, data, pool)

                # 현재 진행 상황 저장
                save_progress(part_number + 1)

            # 모든 부분을 하나의 최종 파일로 병합
            final_results = []
            for part_number in range(NUM_PARTS):
                part_result = pd.read_csv(f'./data/result_part_{part_number}.csv')  # 경로를 ./data/로 수정
                final_results.append(part_result)

            final_df = pd.concat(final_results)
            final_df.to_csv('./data/result.csv', index=False)
            print("작업완료")

    pass


# 비교 연산
def compare_rows(args):
    indexA, rowA, data = args

    # lastParticipation 값의 분포 확인
    participation_values_A = [value for value in (rowA[f'lastParticipation_{i}'] for i in range(30)) if pd.notna(value)]
    common_values_A = Counter(participation_values_A).most_common(1)

    # 가장 빈번한 값이 25 이상인 경우 제외
    if common_values_A and common_values_A[0][1] >= 25:
        return []

    results = []
    for indexB, rowB in data.iterrows():
        if indexA >= indexB: # compare with itself, excluding already compared pairs
            continue

        # lastParticipation 값의 분포 확인
        participation_values_B = [value for value in (rowB[f'lastParticipation_{i}'] for i in range(30)) if pd.notna(value)]
        common_values_B = Counter(participation_values_B).most_common(1)

        # 가장 빈번한 값이 25 이상인 경우 제외
        if common_values_B and common_values_B[0][1] >= 25:
            continue

        matching_count = 0

        # 0부터 29까지 반복하면서 timestamp 비교
        for i in range(30):
            time_strA = rowA[f'lastParticipation_{i}']
            time_strB = rowB[f'lastParticipation_{i}']
            if pd.isna(time_strA) or pd.isna(time_strB):
                continue  # 값이 없으면 연산에서 제외

            timestampA = pd.to_datetime(time_strA)
            timestampB = pd.to_datetime(time_strB)

            # 5초 오차 허용
            if abs((timestampA - timestampB).total_seconds()) <= 5:
                matching_count += 1

        # 30개 중 25개 이상 겹치면 결과 리스트에 추가
        if matching_count >= 25:
            results.append((rowA['Users'], rowA['Details'], rowB['Users'], rowB['Details'], matching_count))
    return results

# 특수 문자를 제거하는 함수
def remove_special_characters(input_string):
    return re.sub(r'[^\w\s]', '', input_string)

# 작업을 나누는 부분의 개수(!!!커스텀 영역!!!)
NUM_PARTS = 100

#------------------------------------------------ 참고 코드 ------------------------------------------------------------------------#