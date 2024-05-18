import time
import datetime
import win32con
import win32api
import win32gui
import requests
import json
import logging
import os
from bs4 import BeautifulSoup
from operator import eq
from apscheduler.schedulers.background import BackgroundScheduler
from logging.handlers import TimedRotatingFileHandler

# # 카톡창 이름, (활성화 상태의 열려있는 창)
kakao_opentalk_name = 'test'
idx = 0

# # 채팅방에 메시지 전송
def kakao_sendtext(chatroom_name, noticeList):
    # # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx(hwndMain, None, "RICHEDIT50W", None)

    check = len(noticeList)
    global idx

    if(idx < check):
        for i in range(idx, check):
            win32api.SendMessage(
                hwndEdit, win32con.WM_SETTEXT, 0, noticeList[i])
            SendReturn(hwndEdit)
            botLogger = logging.getLogger()
            botLogger.debug(noticeList[i])
            time.sleep(3)
    idx = check

# # 엔터
def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

# # 채팅방 열기
def open_chatroom(chatroom_name):
    # # # 채팅방 목록 검색하는 Edit (채팅방이 열려있지 않아도 전송 가능하기 위하여)
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakao_edit1 = win32gui.FindWindowEx(
        hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx(
        hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit2_2 = win32gui.FindWindowEx(
        hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
    hwndkakao_edit3 = win32gui.FindWindowEx(
        hwndkakao_edit2_2, None, "Edit", None)

    # # Edit에 검색 _ 입력되어있는 텍스트가 있어도 덮어쓰기됨
    win32api.SendMessage(
        hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(1)   # 안정성 위해 필요
    SendReturn(hwndkakao_edit3)
    time.sleep(1)

# 공지사항 크롤링하기
def get_dwu_notice():
    today = datetime.datetime.today().strftime("%Y%m%d")
    url = 'https://www.daegu.ac.kr/article/DG159/list'
    req = requests.get(url)
    req.encoding = 'utf-8'

    soup = BeautifulSoup(req.text, 'lxml')

    noticeList = []
    global global_title
    global_title = '공지방 홧팅'

    noticeList = []
    notices = soup.select('#sub_contents > div > table > tbody:nth-child(3) > tr:nth-child(1) > td.list_left > a')  # 여기서 tr의 셀렉터를 정확히 설정해야 합니다.
    for idx, notice in enumerate(notices):
        if idx >= 3:  # 최신 공지사항 3개만 가져오도록 설정
            break
        title = notice.text.strip()
        href = 'https://www.daegu.ac.kr/article/DG159/list' + notice['href'].strip()
        date = notice.find_previous('td').text.strip().replace('-', '')

        if eq(title, global_title):
            continue
        else:
            global_title = title

        if eq(today, date):
            rslt = "[" + date + "]\n" + title + "\n" + href
            noticeList.append(rslt)

    noticeList.reverse()
    return noticeList

# # 스케줄러 job : 매 시간마다 공지사항 크롤링해서 가져오기
def job():
    p_time_ymd_hms = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} / " \
                     f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"

    open_chatroom(kakao_opentalk_name)
    noticeList = get_dwu_notice()
    kakao_sendtext(kakao_opentalk_name, noticeList)

# # log 환경설정
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
