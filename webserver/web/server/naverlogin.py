# -*- coding:utf-8 -*-
from .naver import Naver
import time
from bs4 import BeautifulSoup as bs
import re
from . import returnKeyword

from multiprocessing import Pool

#if __name__ == "__main__":
def naverStart(category, keyword, number):
    naver = Naver('', '')
    # naver2 = Naver('', '')
    clubid = "10050146"

    #네이버 로그인
    try:
        naver.clipboard_login("siso9800", "dundunsh!")
        # naver2.clipboard_login("siso9800", "dundunsh!")
    finally:
        time.sleep(0.5)

    input = []
    keyword = keyword.replace(",", "")
    keyword = keyword.replace("[", "")
    keyword = keyword.replace("]", "")
    # print(keyword)
    key = keyword.split(" ")
    key.insert(0, category)
    input.append(key)
    #input.append([category, '이름', '브랜드', '가격', '색상', '거래방식', '착용횟수', '사이즈'])
    # index = []
    # ti = ""
    # pri = 0
    # con = ""

    number = number.replace(",", "")
    number = number.replace("[", "")
    number = number.replace("]", "")
    data = number.split(" ")

    # link=[]
    # for i in range(len(data)/2):
    #     #게시글 번호로 접근
    #     naver.driver.get('https://m.cafe.naver.com/ArticleRead.nhn?clubid=' + clubid + '&articleid=' + data[i])
    #     naver2.driver.get('https://m.cafe.naver.com/ArticleRead.nhn?clubid=' + clubid + '&articleid=' + data[len(data)-i-1])
    #     html = naver.driver.page_source
    #     html2 = naver.driver.page_source
    #     link.append(html)
    #     link.append(html2)
    # naver.driver.close()

    # start_time = time.time()
    # pool = Pool(processes=4)
    # pool.map(imsipool, link)
    # print("--- %s seconds ---" % (time.time() - start_time))

    # mobile
    temp = []
    #한 페이지의 15개 게시물 크롤링
    for i in range(len(data)):
        index = []
        ti = ""
        pri = 0
        con = ""
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

    naver.driver.close()
    
    return_list = returnKeyword.main(input)
    
    temp = ""
    return_dict = {}
    for i in range(len(data)):
        temp = ""
        for j in range(len(return_list[0])):
            temp += key[j+1] + " : " + str(return_list[i][j]) + " | "
        return_dict[int(data[i])] = temp
    
    # for key, value in return_dict.items():
    #     print(type(key), type(value))
    
    return return_dict

def imsipool(link):

    index = []
    ti = ""
    pri = 0
    con = ""
    # #게시글 번호로 접근
    # naver.driver.get('https://m.cafe.naver.com/ArticleRead.nhn?clubid=' + clubid + '&articleid=' + link)
    # html = naver.driver.page_source
    soup = bs(link, 'html.parser')

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
    print(index)
    # naver.driver.close()
    # input.append(index)