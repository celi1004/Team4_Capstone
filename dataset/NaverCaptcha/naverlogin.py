# -*- coding:utf-8 -*-
from sites.naver import Naver
import time
from bs4 import BeautifulSoup as bs

if __name__ == "__main__":
    naver = Naver('', '')
    clubid = ""
    #네이버 로그인
    try:
        naver.clipboard_login("", "")
    finally:
        time.sleep(1)

    line = []
    title = []
    price = []
    content = []
    page = 1001
    n = 0

    path = 'C:/Users/CSE6P28/Desktop/dataset/여성신발.txt'
    # with open(path, 'r', encoding='utf-8') as f:
    #     n = len(f.readlines())/3
    #     print(n)
    # f.close()

    #페이지마다 크롤링
    start_time = time.time()
    while(page > 0):
        if n == 10000:
            break
        data = []
        page = page - 1
        print(page)
        #페이지 이동
        start_time = time.time()
        naver.driver.get("https://cafe.naver.com/ArticleList.nhn?search.clubid=" + clubid + "&search.menuid=356&search.boardtype=L&search.totalCount=151&search.page=" + str(page))
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
        f = open("C:/Users/CSE6P28/Desktop/dataset/여성신발.txt", 'a', encoding='UTF8') #이어붙이기
        #f = open("C:/학교/3-2/캡스톤 디자인/여성상의.txt", 'w', encoding='UTF8') #처음부터 쓰기
        for i in range(len(data)):
            if n == 10000:
                continue
            val = 0
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
                content.append(result)
                if result == "" or result == " ":
                    val = 1
                    break
            if val == 1:
                continue

            #제목 임시저장
            for j in t:
                temp.append(j.text)

            for j in temp:
                ti = j.split('\n')[5]

            #가격 저장
            for j in p:
                price.append(j.text)

            f.write(ti + "\n")
            f.write(result + "\n")
            f.write(ti + "\n")
            n += 1

    print("--- %s seconds ---" % (time.time() - start_time))
    f.close()

    with open(path, 'r', encoding='utf-8') as f:
        n = len(f.readlines())/3
        print(n)
    f.close()

    naver.driver.quit()
