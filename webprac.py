import requests
import json
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}

url = 'https://www.dongduk.ac.kr/ajax/board/kor/kor_notice/list.json'

req = requests.get(url, headers = headers)

html = req.text

data = json.loads(html)

temp = data.get('data')
rslt = temp.get('list')

for i in rslt:
    a = i.get('B_IDX')
    print(i.get('B_TITLE'))
    print('https://www.dongduk.ac.kr/board/kor/kor_notice/detail.do?curPageNo=1&pageStatus=N&rowSize=15&B_IDX=' + str(a))
