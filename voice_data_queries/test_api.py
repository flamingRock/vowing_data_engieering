import requests

# # 일일 비용 조회
url = "https://engine.hcmc.studio/common/prices/now"
headers = {
    "Accept": "application/json",
    "x-hcmc-gateway-recognition": "00000000-0000-0000-0000-000000000000"
}

response = requests.get(url, headers=headers)
print(response.text)


# # 특정 날짜의 비용 조회
# url = "https://engine.hcmc.studio/common/prices/{날짜}"
# headers = {
#     "Accept": "application/json",
#     "x-hcmc-gateway-recognition": "사용자 ID"
# }

# try:
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         print("Response:", response.json())
#     else:
#         print("Error:", response.status_code)
# except requests.exceptions.RequestException as e:
#     print("Request Exception:", e)
    
    
# # 음성 인식 요청
# url = "https://engine.hcmc.studio/recognitions"
# headers = {
#     "x-hcmc-gateway-recognition": "사용자 ID"
# }
# data = {
#     "locale": "ko-KR",
#     "preferredEngine": "Apple"
# }

# try:
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         print("Response:", response.json())
#     else:
#         print("Error:", response.status_code)
# except requests.exceptions.RequestException as e:
#     print("Request Exception:", e)
