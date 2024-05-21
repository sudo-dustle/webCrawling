import requests
import json
import os

# 현재 스크립트 파일이 저장된 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# 파일 경로 설정
file_path = os.path.join(current_dir, 'kakao_code.json')

url="https://kapi.kakao.com/v2/api/talk/memo/default/send"
# JSON 파일에서 액세스 토큰 읽기
with open(file_path, "r") as fp:
    tokens = json.load(fp)

headers={
    "Authorization" : "Bearer " + tokens["access_token"]
}
def load_notices_from_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return []

# 카카오톡 메시지 전송 함수
def send_kakao_message():
    file_path = os.path.join(current_dir, 'notices.json')
    notices = load_notices_from_json(file_path)

for notice in notices:
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = { "Authorization" : "Bearer " + tokens["access_token"] }

        message_text = f"{notice['title']}\n{"https://www.daegu.ac.kr/article/DG159/list"}"
        data = {
            "template_object": json.dumps({
                "object_type": "text",
                "text": message_text,
                "link": {
                    "web_url": "https://www.daegu.ac.kr/article/DG159/list",
                    "mobile_web_url": "https://www.daegu.ac.kr/article/DG159/list"
                }
            })
        }

response = requests.post(url, headers=headers, data=data)
response.status_code
print(response.status_code)
if response.json().get('result_code') == 0:
	print('메시지를 성공적으로 보냈습니다.')
else:
	print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))