import time
import json
import datetime
import win32con
import win32api
import win32gui
import logging
import os

from operator import eq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from apscheduler.schedulers.background import BackgroundScheduler
from logging.handlers import TimedRotatingFileHandler

# 카톡창 이름, (활성화 상태의 열려있는 창)
kakao_opentalk_name = 'test'
idx = 0

# 채팅방에 메시지 전송
def kakao_sendtext(chatroom_name, noticeList):
    # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx(hwndMain, None, "RICHEDIT50W", None)

    check = len(noticeList)
    global idx

    if(idx < check):
        for i in range(idx, check):
            # 문자열로 변환하여 전송
            notice_text = f"{noticeList[i]['title']} - {noticeList[i]['link']}"
            win32api.SendMessage(
                hwndEdit, win32con.WM_SETTEXT, 0, notice_text)
            SendReturn(hwndEdit)
            botLogger = logging.getLogger()
            botLogger.debug(notice_text)
            time.sleep(3)
    idx = check

# 엔터
def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

# 채팅방 열기
def open_chatroom(chatroom_name):
    # 채팅방 목록 검색하는 Edit (채팅방이 열려있지 않아도 전송 가능하기 위하여)
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakao_edit1 = win32gui.FindWindowEx(
        hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx(
        hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit2_2 = win32gui.FindWindowEx(
        hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
    hwndkakao_edit3 = win32gui.FindWindowEx(
        hwndkakao_edit2_2, None, "Edit", None)

    # Edit에 검색 _ 입력되어있는 텍스트가 있어도 덮어쓰기됨
    win32api.SendMessage(
        hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(1)   # 안정성 위해 필요
    SendReturn(hwndkakao_edit3)
    time.sleep(1)

# 공지사항 크롤링하기
def get_all_notices():
    # Chrome 드라이버 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    today = datetime.date.today().strftime("%Y-%m-%d")

    # 원하는 URL 열기
    driver.get('https://www.daegu.ac.kr/article/DG159/list?pageIndex=1&')

    # 모든 공지사항 요소 가져오기
    notice_elements = driver.find_elements(By.CSS_SELECTOR, '#sub_contents > div > table > tbody > tr')
    
    # 공지사항을 담을 리스트 초기화
    all_notices = []

    # 각 공지사항 요소에서 제목과 링크 추출하여 리스트에 추가
    for idx, element in enumerate(notice_elements, start=1):
        if idx <= 12:  # 12번째 공지사항은 리스트에 추가하지 않음
            continue
        number_element = element.find_element(By.CSS_SELECTOR, 'td:nth-child(1)')
        title_element = element.find_element(By.CSS_SELECTOR, 'td.list_left > a')
        date_element = element.find_element(By.CSS_SELECTOR, 'td:nth-child(5)')  # 공지사항의 날짜 요소 선택
        number = number_element.text.strip()
        title = title_element.text.strip()
        date = date_element.text.strip()
        link = title_element.get_attribute('href')

        if date == today:
            all_notices.append({'number':number, 'date': date, 'title': title, 'link': link})    # 브라우저 닫기
    
    driver.quit()

    return all_notices

def save_notices_to_json(notices, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(notices, json_file, ensure_ascii=False, indent=4)

def load_notices_from_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return []

# 중복된 타이틀을 제거하고 새로운 공지사항만 JSON 파일에 저장


# 스케줄러 job : 매 시간마다 공지사항 크롤링해서 가져오기
def job():
    open_chatroom(kakao_opentalk_name)
    noticeList = get_all_notices()
    save_notices_to_json(noticeList, 'notices.json')
    loaded_notices = load_notices_from_json('notices.json')
    kakao_sendtext(kakao_opentalk_name, loaded_notices)

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
        # 시작할 때 JSON 파일 초기화
        save_notices_to_json([], 'notices.json')
        sched = BackgroundScheduler()
        sched.start()
    except Exception as e:
        print(f"Error in scheduler initialization: {e}")

    try:
        set_logger()
    except Exception as e:
        print(f"Error in logger setup: {e}")

    try:
        sched.add_job(job, 'interval', minutes=0.5)
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