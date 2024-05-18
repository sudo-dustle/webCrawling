from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ChromeOptions 설정
chrome_options = webdriver.ChromeOptions()

# Chrome 드라이버 설정 및 Chrome 브라우저 열기
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 원하는 URL 열기
driver.get('https://www.google.com')

# 사용자 입력을 기다려 창을 유지
input("Press Enter to close the browser and exit...")

# 브라우저 닫기
driver.quit()]