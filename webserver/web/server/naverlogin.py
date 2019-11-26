# -*- coding:utf-8 -*-
from .naver import Naver
import time
from bs4 import BeautifulSoup as bs
import re
from . import returnKeyword

#if __name__ == "__main__":
def naverStart(t, b):
    print(t, b)
    #return
    naver = Naver('', '')
    clubid = "10050146"
    menuid = "358"
    #네이버 로그인
    try:
        naver.clipboard_login("siso9800", "dundunsh!")
    finally:
        time.sleep(1)

    # line = []

    input = []
    input.append(['남성상의', '이름', '브랜드', '가격', '상태', '색상', '거래방식', '착용횟수', '사이즈'])
    index = []
    tit = ""
    pri = ""
    con = ""

    #페이지마다 크롤링
    # start_time = time.time()

    data = []
    #페이지 이동
    start_time = time.time()
    naver.driver.get("https://cafe.naver.com/ArticleList.nhn?search.clubid=" + clubid + "&search.menuid=" + menuid + "&search.boardtype=L&search.totalCount=151&search.page=1")
    #중고나라 프레임 변환
    naver.driver.switch_to_frame('cafe_main')
    html = naver.driver.page_source
    soup = bs(html, 'html.parser')  # html의 관점에서 이해해라!
    #게시글 번호 크롤링
    id = soup.select(
        'div[class=inner_number]'  # class가 inner_number인 div 태그 수집
    )

    #게시글 번호 저장
    for i in id:
        data.append(i.text)

    # mobile
    temp = []
    #한 페이지의 15개 게시물 크롤링
    for i in range(len(data)):
        index = []
        #게시글 번호로 접근
        naver.driver.get('https://m.cafe.naver.com/ArticleRead.nhn?clubid=' + clubid + '&articleid=' + data[i])
        html = naver.driver.page_source
        soup = bs(html, 'html.parser')

        #제목 크롤링
        t = soup.select(
            'li[class=now]' # class가 now인 li 태그 수집
        )

        #가격 크롤링
        p = soup.select(
            'span[class=price]'  # class가 price인 span 태그 수집
        )

        #본문 크롤링
        c = soup.select(
            'div[id=postContent]'  # id가 postContent인 div 태그 수집
        )

        #본문내용 저장
        for j in c:
            p_elements = j.find_all("p")
            result = ""
            for k in p_elements:
                result += k.text
            #예외처리
            result = result.replace("\n", "")
            result = result.replace("\xa0", "")
            result = result.replace("\t", "")
            con = result

        #제목 임시저장
        for j in t:
            ti = j.text.split("\n")[5]

        #가격 저장
        for j in p:
            pri = int(re.findall('\d+', j.text)[0]) * 1000

        index.append(ti)
        index.append(pri)
        index.append(con)
        input.append(index)

    # print(input)
    # print(len(input))
    # print(len(input[0]))

    # print("--- %s seconds ---" % (time.time() - start_time)) 20sec

    naver.driver.close()
    
    return_list = returnKeyword.main(input)

    for r in return_list:
        print(r)