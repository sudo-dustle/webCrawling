import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from operator import eq

url = 'https://www.dongduk.ac.kr/ajax/board/kor/kor_notice/list.json'
req = requests.get(url)

html = req.text

data = json.loads(html)
rslt = data.get('data').get('list')

idx = 0
noticelist = []
for i in rslt:
    date = i.get('REG_DT')[:8]
    index = i.get('B_IDX')
    title = i.get('B_TITLE')
    href = 'https://www.dongduk.ac.kr/board/kor/kor_notice/detail.do?curPageNo=1&pageStatus=N&rowSize=15&B_IDX=' + \
        str(index)
    today = datetime.today().strftime("%Y%m%d")
    # 추후 today로 변경
    if eq('20210302', date):
        # 오늘 날짜 공지인 경우
        # 밑에 카카오링크 api로 변경? 추후 결정
        rslt = "[" + date + "]\n" + title + "\n" + href
        noticelist.append(rslt)

check = len(noticelist)
if(idx < check):
    for i in range(idx, check):
        print(noticelist[i])

print(idx)
idx = check
print(noticelist)
print(idx)
