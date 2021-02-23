import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

today = datetime.today().strftime("%Y%m%d")

url = 'https://www.dongduk.ac.kr/ajax/board/kor/kor_notice/list.json'
req = requests.get(url)

html = req.text

data = json.loads(html)

temp = data.get('data')
rslt = temp.get('list')

# TODO : Dict 사용해서 날짜, 제목, 링크 저장
# Dict 되어 있는 오늘자 공지사항 저장하는 list 만들기
# for문 돌려서 마지막으로 올린 게시물의 idx보다 list.idx 가 클 경우,
# i = idx; i < list.idx; i++ 이런식으로 for문 돌려서 카톡에 공지사항 올리기
a = []
for i in rslt:
    index = i.get('B_IDX')
    date = i.get('REG_DT')[:8]

    # 오늘 올라온 공지사항 list 만들기
    if (date == str(20210223)):
        a.append(date)
        a.append(i.get('B_TITLE'))
        a.append('https://www.dongduk.ac.kr/board/kor/kor_notice/detail.do?curPageNo=1&pageStatus=N&rowSize=15&B_IDX=' + str(index))


s = "\n".join(a)

print(s)