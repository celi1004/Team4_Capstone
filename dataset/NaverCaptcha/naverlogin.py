# -*- coding:utf-8 -*-
from sites.naver import Naver
import time
from bs4 import BeautifulSoup as bs

if __name__ == "__main__":
    naver = Naver('', '')
    clubid = "10050146"
    #네이버 로그인
    try:
        naver.clipboard_login("siso9800", "dundunsh!")
    finally:
        time.sleep(5)

    line = []
    title = []
    price = []
    content = []
    page = 1001

    #페이지마다 크롤링
    while(page > 0):
        data = []
        page = page - 1
        print(page)
        #페이지 이동
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
        #print(data)

        # mobile
        temp = []
        #num = 0
        #한 페이지의 15개 게시물 크롤링
        #for i in data:
        for i in range(len(data)):
            #게시글 번호로 접근
            #num = num + 1
            #if(i % 2 == 0):
            #    continue;
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

            #제목 임시저장
            for j in t:
                temp.append(j.text)

            #가격 저장
            for j in p:
                price.append(j.text)

        #제목 저장
        for i in temp:
            title.append(i.split('\n')[5])

    #txt 파일로 저장
    f = open("C:/학교/3-2/캡스톤 디자인/여성상의.txt", 'w', encoding='UTF8')
    n = 0
    for i in range(len(title)):
        if(n == 10000):
            break;
        #본문내용 없는 것 제외
        if content[i] != "":
            n = n + 1
            f.write(title[i] + "\n")
            f.write(content[i] + "\n")
            f.write(title[i] + "\n")
    print(n)
    f.close()

    naver.driver.quit()