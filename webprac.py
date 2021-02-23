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

a = []
for i in rslt:
    index = i.get('B_IDX')
    date = i.get('REG_DT')[:8]

    if (date == str(today)):
        a.append(date)
        a.append(i.get('B_TITLE'))
        a.append('https://www.dongduk.ac.kr/board/kor/kor_notice/detail.do?curPageNo=1&pageStatus=N&rowSize=15&B_IDX=' + str(index))

s = "\n".join(a)

print(s)