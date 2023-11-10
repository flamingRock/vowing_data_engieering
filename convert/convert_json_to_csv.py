import os
import json
import pandas as pd

def json_to_csv_v2(file_path, output_path):
    """Converts a given JSON file to a CSV with specified columns."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    users_data = data.get("Users", {})
    rows = []
    
    for user_id, user_info in users_data.items():
        attend_data = user_info.get("Attend", {})
        for attend_name, attend_info in attend_data.items():
            row = {
                "user_id": user_id,
                "ArrayVoice": attend_info.get("ArrayVoice"),
                "attend": attend_info.get("attend"),
                "resultPass": attend_info.get("resultPass"),
                "imageUrl": attend_info.get("imageUrl"),
                "addText": attend_info.get("addText"),
                "name": attend_info.get("name"),
                "ArrayPercent": attend_info.get("ArrayPercent"),
                "ArrayDate": attend_info.get("ArrayDate"),
                "title": attend_info.get("title"),
                "type": attend_info.get("type"),
                "review_wish": attend_info.get("review_wish"),
                "ArrayAddResult": attend_info.get("ArrayAddResult")
            }
            rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False, escapechar='\\', quoting=1)

attend_directory = "D:/DATA_PREPROCESS/FIRESTORE_DATAS/Users_Attend/Users_Attend_231004/all_namespaces/all_kinds"

# output-0.json부터 output-191.json까지 변환
for i in range(192):
    json_path = os.path.join(attend_directory, f"output-{i}.json")
    csv_path = os.path.join(attend_directory, f"output-{i}.csv")
    
    if os.path.exists(json_path):
        json_to_csv_v2(json_path, csv_path)
        print(f"Converted {json_path} to {csv_path}")

# # 변환된 CSV 파일 로드 및 head 확인
# converted_csv = pd.read_csv(csv_path)
# converted_csv_head = converted_csv.head()
# converted_csv_head