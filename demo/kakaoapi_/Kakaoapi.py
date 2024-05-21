import requests
import json
import os

# 액세스 토큰 요청
url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type" : "authorization_code",
    "client_id" : "REST_API",
    "redirect_url" : "http://localhost:5050",
    "code" : " "
}
response = requests.post(url, data=data)
tokens = response.json()
print(tokens)


# 현재 스크립트 파일이 저장된 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# 파일 경로 설정
file_path = os.path.join(current_dir, 'kakao_code.json')

# JSON 파일에 저장
with open(file_path, "w") as fp:
    json.dump(tokens, fp)

print("Access token saved to kakao_code.json")
