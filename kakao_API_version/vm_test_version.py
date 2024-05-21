import time
import json
import datetime
import logging
import os
import requests
from bs4 import BeautifulSoup

from apscheduler.schedulers.background import BackgroundScheduler
from logging.handlers import TimedRotatingFileHandler

# 카카오 API 설정

current_dir = os.path.dirname(os.path.abspath(__file__))

# 파일 경로 설정
file_path = os.path.join(current_dir, 'kakao_code.json')

url="https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
# JSON 파일에서 액세스 토큰 읽기
with open(file_path, "r") as fp:
    tokens = json.load(fp)

headers={
    "Authorization" : "Bearer " + tokens["access_token"]
}

# 공지사항 크롤링하기
def get_today_notices():
        # 오늘 날짜 가져오기
    today = datetime.date.today().strftime("%Y-%m-%d")

    # URL 가져오기
    url = 'https://www.daegu.ac.kr/article/DG159/list?pageIndex=1&'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 공지사항을 담을 리스트 초기화
    today_notices = []

    # 공지사항 요소 가져오기
    notice_elements = soup.select('#sub_contents > div > table > tbody > tr')

    # 각 공지사항 요소에서 제목과 링크 추출하여 리스트에 추가
    for idx, element in enumerate(notice_elements, start=1):
        if idx <= 12:
            continue
        title_element = element.select_one('td.list_left > a')
        date_element = element.select_one('td:nth-child(5)') 
        title = title_element.text.strip()
        date = date_element.text.strip()
        link = title_element['href']
        
        if date == today:
            today_notices.append({'date': date, 'title': title, 'link': link})   # 브라우저 닫기
   
    return today_notices

def save_notices_to_json(notices, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(notices, json_file, ensure_ascii=False, indent=4)

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
        if response.status_code == 200 and response.json().get('result_code') == 0:
            print('메시지를 성공적으로 보냈습니다.')
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

# 스케줄러 job : 매 시간마다 공지사항 크롤링해서 가져오기
def job():
    noticeList = get_today_notices()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'notices.json')
    save_notices_to_json(noticeList, file_path)
    send_kakao_message()

# log 환경설정
def set_logger():
    botLogger = logging.getLogger()
    botLogger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    log_dir = os.path.abspath('./noticebot_log')
    os.makedirs(log_dir, exist_ok=True)

    rotatingHandler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, 'webCrawling.log'), when='W0', encoding='utf-8', backupCount=5, atTime=datetime.time(0, 0, 0))
    rotatingHandler.setLevel(logging.DEBUG)
    rotatingHandler.setFormatter(formatter)
    rotatingHandler.suffix = datetime.datetime.today().strftime("%Y-%m-%d-%H-%M")
    botLogger.addHandler(rotatingHandler)

def main():
    try:
        #current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'notices.json')
        save_notices_to_json([], file_path)
        sched = BackgroundScheduler()
        sched.start()
    except Exception as e:
        print(f"Error in scheduler initialization: {e}")

    try:
        set_logger()
    except Exception as e:
        print(f"Error in logger setup: {e}")

    try:
        sched.add_job(job, 'interval', minutes=1)
    except Exception as e:
        print(f"Error in adding job to scheduler: {e}")

    while True:
        try:
            botLogger = logging.getLogger()
            botLogger.debug("-------------실행 중-------------")
            time.sleep(900)
        except Exception as e:
            print(f"Error in main loop: {e}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in main execution: {e}")
