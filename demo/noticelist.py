import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

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
        title_element = element.find_element(By.CSS_SELECTOR, 'td.list_left > a')
        date_element = element.find_element(By.CSS_SELECTOR, 'td:nth-child(3)')  # 공지사항의 날짜 요소 선택
        title = title_element.text.strip()
        date = date_element.text.strip()
        link = title_element.get_attribute('href')

        if date == today:
            all_notices.append({'number': idx, 'title': title, 'link': link})    # 브라우저 닫기
    
    driver.quit()

    return all_notices

# 모든 공지사항 가져오기
notices = get_all_notices()

# 결과 출력
for notice in notices:
    print(notice)
