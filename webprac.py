import requests
import json
from bs4 import BeautifulSoup
import copy

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

noticelist = []
for i in rslt:
    date = i.get('REG_DT')[:8]
    index = i.get('B_IDX')
    title = i.get('B_TITLE')
    herf = 'https://www.dongduk.ac.kr/board/kor/kor_notice/detail.do?curPageNo=1&pageStatus=N&rowSize=15&B_IDX=' + str(index)
    # 공지사항 list 만들기
    noticelist.append([date, title, herf])



changelist = []               

#if changelist is None :
changelist = copy.deepcopy(noticelist)

print(changelist)
print("---------------------------------------------------------")

setChange = set(tuple(row) for row in changelist)
setCheck = set(tuple(row) for row in noticelist)

diff = setCheck - setChange
#diff = noticelist - changelist
#diff = [x for x in noticelist if x not in changelist]

if len(diff) > 0:
    changelist = copy.deepcopy(noticelist)

print(diff)

                