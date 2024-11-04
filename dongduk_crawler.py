import requests 
from bs4 import BeautifulSoup

url = 'https://www.dongduk.ac.kr/www/contents/kor-noti.do?gotoMenuNo=kor-noti'  
response = requests.get(url)    
dongduk_url = 'https://www.dongduk.ac.kr/www/contents/kor-noti.do?schM=view&page=1&viewCount=10&id='

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    notices = soup.select_one('ul.board-basic')
    elements = notices.select('li > dl')

    for element in elements:
        id = element.a.get('onclick').split("'")[1] # onclick 속성 값 중 " ' " 로 split 해서 두번째 값 가져옴
        title = element.a.text.strip() 
        date = element.find_all('span', 'p_hide')[1].text # .find_all(태그 이름, 속성) 해당 하는 정보 모두 조회

        print(date)
        print(title)
        print(dongduk_url + id)
        print('--------------------------------')


else : 
    print(response.status_code)