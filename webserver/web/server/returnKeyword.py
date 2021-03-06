import re
import os
from pprint import pprint
from konlpy.tag import Okt
import gensim
import operator

okt = Okt()
model = None
#fastTextModel = gensim.models.FastText.load('./fastTextModel')
#fastTextModel = gensim.models.Word2Vec.load('./ko.bin')

cate = ''
brand_name = ''
size_num = 0
sel_color = ''

name = []
brand = []
color = []

def getName(string_list, docs_list, all_docs_list):
    if cate == '옷':
        return_name = getClothesName(docs_list)
    elif cate == '신발':
        return_name = getShoesName(all_docs_list)
    else:
        return_name = getItName(string_list, all_docs_list)
    return return_name

def getClothesName(docs_list):
    return_name_list = []
    flag = 0

    for t, p in docs_list:
        for c in name:
            if c.split("/")[0] == t:
                if t in return_name_list:
                    flag = 3
                    break
                else:
                    if t == '투맨':
                        t = '맨투맨'
                    if t == '상':
                        t = '야상'
                    if t == '종':
                        t = '블루종'
                    return_name_list.append(t)
                    flag = 1
                    break
        if flag == 1 or flag ==2:
            flag = flag + 1
            continue
        elif flag ==3:
            break
    if len(return_name_list) == 0:
        return '?'        
    else:
        return (" ".join(return_name_list)).strip()

def getShoesName(all_docs_list):
    noun_lists = []
    noun_list = []
    pre_p = ''
    noun_appear = 0
    count = 0
    global brand_name
    global size_num
    global sel_color

    for t, p in all_docs_list:
        if p == 'Noun' or p == 'Alpha' or p == 'Number':
            if p == 'Number':
                int_t = int (re.sub("\D*", "", t)) 
                if int_t <= 300 and int_t > 200 and int_t %5 ==0:
                    size_num = int_t
                    noun_appear = 0
                    count = count + 1
                    if count > 3 :
                        break
                    noun_lists.append(noun_list)
                    noun_list = []
                    continue
            if p == 'Noun' and brand_name == '':
                for b in brand:
                    if b.split("/")[0] == t:
                        brand_name = t
                        break
            if p == 'Noun' and sel_color == '':
                for c in color:
                    if c.split("/")[0] == t:
                        sel_color = t
                        break
            if t not in ["사이즈", "size", "싸이즈", "싸쥬", "mm", "미리"]:
                if t in ["제품", "상품", "정품", "판매", "구매", "상태", "사용감", "가격", "판매가", "택포", "착불", "희망가", "운포", "배송지", "미시", "실착", "착용"]:
                    noun_appear = 0
                    count = count + 1
                    if count > 3 :
                        break
                    noun_lists.append(noun_list)
                    noun_list = []
                    continue
                noun_appear = 1
                pre_p = p
                noun_list.append(t)
            else:
                if pre_p == 'Number':
                    try:
                        tempsize = noun_list.pop()
                    except:
                        print("오잉")
                    if size_num == 0:
                        tempsize = int ((re.split("\D", tempsize)[0])) 
                        if tempsize <= 300 and tempsize > 200 and tempsize %5 ==0:
                            size_num = tempsize
                noun_appear = 0
                count = count + 1
                if count > 3 :
                    break
                noun_lists.append(noun_list)
                noun_list = []
                continue
        elif noun_appear != 0:
            noun_appear = 0
            count = count + 1
            if count > 3 :
                break
            noun_lists.append(noun_list)
            noun_list = []

    return_name = max(noun_lists, key=len) 

    return (" ".join(return_name)).replace(brand_name, "").replace(sel_color, "").strip().replace("  ", " ")

def getItName(string_list, all_docs_list):

    global cate
    if cate == '핸드폰':
        return getPhoneName(string_list, all_docs_list)
    else:
        return getNoteName(string_list, all_docs_list)

def getPhoneName(string_list, all_docs_list):

    name_appear = 0
    alpha_appear_flag = 0
    pre_t = ''
    not_product_name_count = 0
    return_keyword_list = []

    for t, p in all_docs_list:
        if p == 'Alpha':
            if t.lower() == "gb":
                try:
                    return_keyword_list.pop()
                except:
                    print("오잉")
                if name_appear == 0:
                    continue
                else:
                    break

            alpha_appear_flag = 1
            if t.lower() == 'I'.lower():
                pre_t = 'i'
                if name_appear == 1:
                    break
                else:
                    continue
            if t.lower() == 'MAX'.lower():
                return_keyword_list.append(t)
                name_appear = 1
                continue
            if t.lower() == 'pen'.lower():
                return_keyword_list.append(t)
                name_appear = 1
                continue
            return_keyword_list.append(t)
        elif p == 'Number':
            if pre_t != 'i':
                return_keyword_list.append(t)
            else:
                continue
        elif p == 'Noun':
            if t == "기":
                try:
                    return_keyword_list.pop()
                except:
                    print("오잉")
                if name_appear == 0:
                    continue
                else:
                    break
            for n in name:
                if n.split("/")[0] == t:
                    if alpha_appear_flag == 0:
                        return_keyword_list = []
                        alpha_appear_flag = 1
                    if t == '게이':
                        return_keyword_list.append('게이밍')
                        break
                    name_appear = 1
                    return_keyword_list.append(t)
                    break
        elif t == '-':
            return_keyword_list.append(t)
        elif t == '+':
            return_keyword_list.append(t)
        else:
            not_product_name_count = not_product_name_count + 1

        if not_product_name_count > 3:
            break

    return "".join(return_keyword_list)

def getNoteName(string_list, all_docs_list):

    return_keyword_list = []

    first_num = 0
    the_end = 0
    name_appear = 0

    global brand_name

    for t, p in all_docs_list:
        first_num = first_num + 1
        if name_appear == 0 or the_end == 0:
            if t.lower() == 'pen' or t.lower() == 'max':
                return_keyword_list.append(t)
            #이름같은게 안나옴
            if p == 'Noun':
                for n in name:
                    if n.split("/")[0].lower() == t.lower():
                        if t == '게이':
                            return_keyword_list.append('게이밍')
                            break
                        name_appear = 1
                        return_keyword_list.append(t)
                        break
                if name_appear == 1 and the_end == 0:
                    the_end = 1
                    return_keyword_list.append(" ")
        else:
            #나오고 숫자 영어 연달아인것만 출력
            
            if p == 'Alpha':
                if t.lower() == 'i' or t.lower() == 'ssd' or t.lower() == 'hdd':
                    break
                if t.lower() == 'lg':
                    brand_name = 'LG'
                    continue
                if t.lower() == 'hp':
                    brand_name = 'HP'
                    continue
                if t.lower() == 'msi':
                    brand_name = 'MSI'
                    continue
                if t.lower() == 'gb' or t.lower() == 'g' or t.lower() == 'ram':
                    try:
                        return_keyword_list.pop()
                    except:
                        print("오잉")
                    break

                if brand_name == '':
                    for b in brand:
                        if b.split("/")[0].lower() == t.lower():
                            brand_name = t
                            break
                    #여기오는거보면 브랜드가 아닌 영어구나
                    return_keyword_list.append(t)
                else:
                    if brand_name.lower() == t.lower():
                        break
                    else:
                        #브랜드가 아닌 영어구나
                        return_keyword_list.append(t)

            elif p == 'Number':
                if first_num < 3:
                    continue
                temp_list = re.findall("원", t)
                if len(temp_list) > 0:
                    break
                if int (re.sub("\D*", "", t)) > 2000:
                    break
                return_keyword_list.append(t)
            elif t == '-':
                return_keyword_list.append(t)
            elif t == '+':
                return_keyword_list.append(t)
            else:
                break

    return " ".join(return_keyword_list).replace(" ", "")

def getBrand(string_list, docs_list):
    #브랜드 반환
    global brand_name
    flag = 0

    if brand_name == '':
        for t, p in docs_list:
            if flag == 1:
                flag = 2
            for b in brand:
                if b.split("/")[0].lower() == t.lower():
                    if t == '키르':
                        t = '키르시'
                    if t == '노비':
                        t = '노비스'
                    flag = 1
                    brand_name = brand_name +t
                    break
            if flag == 2:
                return brand_name
    else:
        return brand_name
    return '?'

def getPrice(string_list, docs_list):
    find_keyword = re.findall("[0-9일이삼사오육칠팔구십천만천백십/., ]+원",string_list)
    find_keyword = list(filter(('원').__ne__, find_keyword))


    if len(find_keyword) == 1 :
        find_keyword = find_keyword[0].replace(" ", "")
        return find_keyword
    elif len(find_keyword) > 1:
        find_n_distance = getMeanDistance(docs_list, [tuple(wordTokenize(ex_str).split("/")) for ex_str in find_keyword], ['정가', '구입'])
        if find_n_distance == 0 : 
            find_keyword = find_keyword[0]
        else:
            find_keyword = find_keyword[find_n_distance.index(max(find_n_distance))]
    else:
        find_keyword = '?'
        searchList = ["가격", "판매가", "택포", "착불", "희망가", "운포"]
        tempTokenList = getAroundToken(docs_list, searchList)

        tokenList = []
        for t in tempTokenList:
            if t[1] == 'Number':
                tokenList.append(t)

        if len(tokenList) == 1:
            find_keyword = tokenList[0][0]
        elif len(tokenList) > 1:
            find_n_distance = getMeanDistance(docs_list, tokenList, ['정가', '구입'])
            if find_n_distance == 0:
                find_keyword = tokenList[1][0]
            else:
                find_keyword = tokenList[find_n_distance.index(max(find_n_distance))][0]

    find_keyword = find_keyword.replace(" ", "")
    return find_keyword

def getState(string_list, docs_list):
    #상태 반환
    find_keyword = re.findall("\w+급", string_list)
    find_keyword = list(filter(('취급').__ne__, find_keyword))
    find_keyword = list(filter(('발급').__ne__, find_keyword))
    find_keyword = list(filter(('자급').__ne__, find_keyword))
    find_keyword = list(filter(('동급').__ne__, find_keyword))
    find_keyword = list(filter(('지급').__ne__, find_keyword))
    find_keyword = list(filter(('현금지급').__ne__, find_keyword))

    if len(find_keyword) == 1 and len(find_keyword[0]) < 5:
        find_keyword = find_keyword[0]
    elif len(find_keyword) == 1:
        find_keyword = find_keyword[0][-2:]
    elif len(find_keyword) > 1:
        find_keyword = find_keyword[0] 
    else:
        find_keyword = '?'
        prepos = ''

        searchList = ["상태", "사용감", "보관", "퀄"]
        #tODO 사용감일때 있다면 사용감있다

        tokenList= getAroundToken(docs_list, searchList)

        for t in tokenList:
            if t[1] == 'Noun' or t[1] == 'Adjective':
                if t[0] == '이다':
                    continue
                if t[0] == '확인':
                    continue
                if prepos != 'Adjective':
                    find_keyword = t[0][:2]
                    prepos = t[1]

    find_keyword = find_keyword.replace("상품", "새상품")
    find_keyword = find_keyword.replace(" ", "")
    find_keyword = find_keyword.replace("무용", "깨끗")
    find_keyword = find_keyword.replace("미사", "미사용")
    find_keyword = find_keyword.replace("있다", "사용감 O")
    find_keyword = find_keyword.replace("정도", "사용감 O")
    find_keyword = find_keyword.replace("없다", "오염 X")
    find_keyword = find_keyword.replace("하자", "하자 X")
    find_keyword = find_keyword.replace("그대", "보관만")
    find_keyword = find_keyword.replace("한상", "보관만")

    if find_keyword == '?':
        searchList = ['미착용', '새상품', '미개봉', '새제품', '미 착용', '새 상품', '미 개봉', '새 제품', '미사용', '미 사용', '미시착', '미 시착', '새 상태', '새상태']
        #새상태

        for searchToken in searchList:
            if searchToken in string_list:
                find_keyword = '새상태'
                return find_keyword

        searchList = ['실내']
        #새상태

        for searchToken in searchList:
            if searchToken in string_list:
                find_keyword = '실내사용'
                return find_keyword
    
    return find_keyword

def getColor(string_list, docs_list):
    return_name = '?'
    if cate == '옷':
        return_name = getClothesColor(string_list, docs_list)
    else:
        return_name = getColorDic(docs_list)
    return return_name

def getClothesColor(string_list, docs_list):

    global sel_color

    if sel_color == '':
        find_keyword = re.findall("\w+색",string_list)
        find_keyword = list(filter(('배색').__ne__, find_keyword))
        find_keyword = list(filter(('검색').__ne__, find_keyword))
        find_keyword = list(filter(('변색').__ne__, find_keyword))

        if len(find_keyword) == 1 and len(find_keyword[0]) < 5:
            find_keyword = find_keyword[0].replace(" ", "")
            return find_keyword
        elif len(find_keyword) > 1:
            #TODO 베이지(영어를 한국어로)를 예시토큰할지 빨강(그냥 색이라는 단어없는 색깔)을 예시토큰할지 고민
            find_keyword = getMostSimilarityVerString(find_keyword, "베이지")
        else:
            find_keyword = '?'
            searchList = ["색상", "컬러", "색깔"]
            tokenList= getAroundToken(docs_list, searchList)
            find_keyword = getMostSimilarityVerToken(tokenList, "베이지")

        find_keyword = find_keyword.replace("벽돌", "벽돌색")
        find_keyword = find_keyword.replace(" ", "")
        if find_keyword == '?':
            return getColorDic(docs_list)
        else:
            return find_keyword
    else:
        return sel_color

def getColorDic(docs_list):
    #색상 사전에서 일치하는 것 반환
    global sel_color

    if sel_color == '':
        for c in color:
            for t, p in docs_list:
                if c.split("/")[0] == t:
                    sel_color = t
                    return t
    else:
        return sel_color
    return "?"

def getMethod(string_list, docs_list):
    flag = 0

    searchList1 = ['택배', '택비', '택포', '택.포', '택 포', '배송', '운송', '운포', '착불', '택배비', '운송비']
    searchList2 = ['직거래', '직 거래']

    for searchToken in searchList1:
        if searchToken in string_list:
            flag = 1
            break

    for searchToken in searchList2:
        if searchToken in string_list:
            if flag == 1:
                flag = 3
            else:
                flag = 2
            break

    if flag == 0:
        find_keyword = '?'
    elif flag == 1:
        find_keyword = '택배'
    elif flag == 2:
        find_keyword = '직거래'
    else:
        find_keyword = '택배+직거래'

    return find_keyword

def getCount(string_list):
    temp_keyword = re.findall("\d*-*~*\d+ ?[번회]",string_list)

    if len(temp_keyword) == 1 and len(temp_keyword[0]) < 5 :
        find_keyword = temp_keyword[0]
    elif len(temp_keyword) == 1:
        find_keyword = temp_keyword[0][-2:]
    elif len(temp_keyword) > 1 and len(temp_keyword[0]) < 5:
        find_keyword = temp_keyword[0] #'여러개야'
    else:

        searchList = ['미착용', '새상품', '미개봉', '새제품', '미 착용', '새 상품', '미 개봉', '새 제품', '미사용', '미 사용', '미시착', '미 시착'] #완전히 한번도 안입은 거

        for searchToken in searchList:
            if searchToken in string_list:
                find_keyword = '사용안함'
                return find_keyword

        temp_keyword = re.findall("\w*-*~*\w+ ?[번회]",string_list)
        temp_keyword = list(filter(('안심번').__ne__, temp_keyword))
        temp_keyword = list(filter(('즉시번').__ne__, temp_keyword))
        temp_keyword = list(filter(('전화번').__ne__, temp_keyword))
        temp_keyword = list(filter(('후회').__ne__, temp_keyword))
        temp_keyword = list(filter(('첫번').__ne__, temp_keyword))
        temp_keyword = list(filter(('이번').__ne__, temp_keyword))
        temp_keyword = list(filter(('삼번').__ne__, temp_keyword))
        temp_keyword = list(filter(('연주회').__ne__, temp_keyword))

        if len(temp_keyword) == 1 :
            if len(temp_keyword[0])> 4:
                find_keyword = '?'
            else:
                find_keyword = temp_keyword[0]
        elif len(temp_keyword) > 1:
            find_keyword = temp_keyword[0]#'여러개야'
        else:
            find_keyword = '?'

    find_keyword = find_keyword.replace(" ", "")
    return find_keyword

def getSize(string_list, docs_list):

    global size_num
    tempAlphaSize = ''

    if size_num == 0:
        searchList = ["사이즈", "size", "싸이즈", "싸쥬"]

        tokenList = getAroundToken(docs_list, searchList)

        token = 1000000

        for t in tokenList:
            if t[0] == 'free'or t[0] == 'FREE' or t[0] == '프리':
                return t[0]
            if t[1] == 'Alpha':
                tempAlphaSize = t[0]
            if t[1] == 'Number':
                temp_list = re.findall("\D+", t[0])
                compare_token = 0
                if len(temp_list) > 0:
                    temp_list = re.split("\D", t[0])
                    temp_list = list(filter(('').__ne__, temp_list))
                    compare_token = int(temp_list[len(temp_list)-1])
                else:
                    compare_token = int(t[0])
                if token > compare_token:
                    token = compare_token                    
                    
        if token == 1000000:
            if tempAlphaSize != '':
                return tempAlphaSize
            find_keyword = re.findall("\d*.?\d+ ?인치",string_list)
            if len(find_keyword) == 1 :
                find_keyword = find_keyword[0].replace(" ", "")
                return find_keyword
            find_keyword = re.findall("\d+ ?mm",string_list, re.I)
            if len(find_keyword) == 1 :
                find_keyword = find_keyword[0].replace(" ", "")
                return find_keyword
            find_keyword = re.findall("\d+ ?호",string_list)
            if len(find_keyword) == 1 :
                find_keyword = find_keyword[0].replace(" ", "")
                return find_keyword
            return '?'
        else:
            return token
    else:
        return size_num
    return "?"

def getCapacity(string_list, docs_list):
    #용량 반환
    hardtype = 0 # 0 둘 다 없음 1 ssd만 있음 2 hdd만 있음 3 둘 다 있음
    return_keyword_string = ''
    find_keyword = re.findall("ssd", string_list, re.I)
    if len(find_keyword) > 0:
        hardtype = 1
        return_keyword_string = return_keyword_string + "SSD有"
    find_keyword = re.findall("hdd", string_list, re.I)
    if len(find_keyword) > 0:
        if hardtype == 0:
            hardtype = 2
        else:
            hardtype = 3
        return_keyword_string = return_keyword_string + " HDD有"

    find_keyword = re.findall("\d+ ?GB", string_list, re.I)
    find_keyword = find_keyword + re.findall("\d+ ?기가", string_list)
    if len(find_keyword) == 0:
        find_keyword = find_keyword + re.findall("\w+ ?GHz", string_list, re.I)
        if len(find_keyword) == 0:
            find_keyword = find_keyword + re.findall("\w+ ?G", string_list, re.I)
        else:
            if return_keyword_string == '':
                return '?'
            else:
                return return_keyword_string.strip()

    find_keyword = list(filter(('LG').__ne__, find_keyword))
    #LG가 뽑히면 지워줘
    find_keyword = [re.sub("\D*", "", i) for i in find_keyword]
    #숫자가 아닌 것도 지워
    find_keyword = list(filter(('').__ne__, find_keyword))
    find_keyword = [int(i) for i in find_keyword]
    temp_list = []
    for i in find_keyword:
        if i <800 and i > 0:
            temp_list.append(i)
    find_keyword = temp_list

    if len(find_keyword) == 1 :
        return_keyword_string = return_keyword_string + " " + str(find_keyword[0]) + "GB"
        return return_keyword_string
    elif len(find_keyword) > 1:
        if max(find_keyword) == min(find_keyword) :
            find_keyword = str(max(find_keyword)) + "GB"
        else:
            find_keyword = list(set(find_keyword)) # 중복제거하고
            find_keyword.sort()
            return_min_size = 0
            if find_keyword[1] <= find_keyword[0] * 4:
                return_min_size = find_keyword[1]
            else:
                return_min_size = find_keyword[0]
            
            hdd = "HDD " + str(max(find_keyword)) + "GB"
            ssd = "SSD " + str(max(find_keyword)) + "GB"
            all = str(max(find_keyword)) + "GB" + " " + str(return_min_size) + "GB"
            ram = str(return_min_size) + "GB"
            if hardtype == 0:
                find_keyword = ram
            elif hardtype == 1:
                find_keyword = ssd + " " + "RAM " + ram
            elif hardtype == 2:
                find_keyword = hdd + " " + "RAM " + ram
            else:
                find_keyword = all
    else:
        if return_keyword_string == '':
            find_keyword = '?'
        else:
            find_keyword = return_keyword_string

    return find_keyword

def getSpec(string_list, docs_list):
    return_keyword_string = ''
    find_keyword = re.findall("\d*.?\d+ ?인치", string_list, re.I)
    if len(find_keyword) > 0:
        return_keyword_string = return_keyword_string + find_keyword[0].replace(" ", "") + " "

    find_keyword = re.findall("i\d+", string_list, re.I)
    if len(find_keyword) > 0:
        return_keyword_string = return_keyword_string + find_keyword[0].replace(" ", "") + " "
    else:

        searchList = ['펜티엄', '셀레론'] #i3 5 7 아니고 다른 cpu

        for searchToken in searchList:
            if searchToken in string_list:
                return_keyword_string = return_keyword_string + searchToken + " "

    find_keyword = re.findall("\d* ?.?\d+kg", string_list, re.I)
    if len(find_keyword) > 0:
        return_keyword_string = return_keyword_string + find_keyword[0].replace(" ", "") + " "

    return return_keyword_string.strip()

def getTerm(string_list):
    global cate
    #사용기간 반환
    if cate == '노트북' or cate == '핸드폰' :
        find_keyword = re.findall("\d+년|\d+월|\d+일", string_list)
    else:
        find_keyword = re.findall("\d+년|\d+월", string_list)
    find_keyword = list(filter(('파일').__ne__, find_keyword))
    find_keyword = list(filter(('제조년').__ne__, find_keyword))

    if len(find_keyword) == 1 :
        find_keyword = find_keyword[0]
    elif len(find_keyword) > 1:
        #TODO 여러개일때 어떡할까
        find_keyword = find_keyword[0]#'여러개야' 
    else:
        find_keyword = '?'

    find_keyword = find_keyword.replace(" ", "")
    return find_keyword

#토큰 리스트 안에 있는 토큰과 어떤 토큰의 거리 반환 ex) 정가와 멀리 떨어져있는 것 찾기 
def getMeanDistance(token_list,find_token_list, find_str_list):
    #token_list : [(),(),()] 여기 들 중에섯 나온 단어으 ㅣ
    #find_token_list : [('90', 'Number), ('8천', 'Number')]
    #find_str_list : ["정가", "구입"]
    index_num = [0]*len(find_token_list)  #이거로 안에 값이 안바뀌고 거리 찾게 해줘
    mean_dis_list = [0]*len(find_token_list)
    for tl in token_list:
        #이 토큰 리스트안에 내가 찾을 리스트가 있으면 그거랑 우리가 찾아야하는 토큰의 위치 비교
        if tl in find_token_list:
            index_num[find_token_list.index(tl)] = token_list.index(tl)

    count = 0
    col = 0
    temp_col = 0
    for fsl in find_str_list:
        for t, p in token_list:
            if wordTokenize(fsl).split("/")[0] == t:
                count = count + 1
                plus_list = [abs(ftln - col) for ftln in index_num]
                mean_dis_list =[mean_dis_list[i] + plus_list[i] for i in range(len(mean_dis_list))]
            col = col + 1

    if count == 0:
        return 0
    else:
        return [mdl/count for mdl in mean_dis_list]

#검색 토큰 리스트 안에 있는 토큰 근처에 있는 토큰들, 어떤 토큰 근처에있었는지 반환
def getAroundToken(string_list, search_list):
    return_list = []
    for search in search_list:
        for token in string_list:
            if token[0] in search:
                index_num = string_list.index(token)
                if index_num != 0:
                    return_list.append(string_list[index_num-1])
                if index_num != len(string_list)-1:
                    return_list.append(string_list[index_num+1])

    return return_list

#토큰 리스트에서 예시 토큰이랑 가장 비슷한 토큰 반환
def getMostSimilarityVerToken(token_list, ex_str):
    ex_token = wordTokenize(ex_str)
    maxSimilarity = 0
    find_keyword = '?'
    for t in token_list:
        try:
            tempSimilarity = model.wv.similarity(ex_token, '/'.join(t))
        except:
            #내가 만든 모델에 없는 단어
            try:
                tempSimilarity = 0 # fastTextModel.wv.similarity(ex_str, t[0])
            except:
                #더 큰 모델에 없는 단어
                tempSimilarity = 0
        if tempSimilarity > maxSimilarity:
            find_keyword = t[0]
            maxSimilarity = tempSimilarity

    return find_keyword

#스트링 리스트에서 예시 토큰이랑 가장 비슷한 토큰 반환
def getMostSimilarityVerString(string_list, ex_str):
    ex_token = wordTokenize(ex_str)
    maxSimilarity = 0
    find_keyword = '?'
    for s in string_list:
        temp_token = wordTokenize(s)
        try:
            tempSimilarity = model.wv.similarity(ex_token, temp_token)
        except:
            #내가 만든 모델에 없는 단어
            try:
                tempSimilarity = 0 #fastTextModel.wv.similarity(ex_str, temp_token.split('/')[0])
            except:
                #더 큰 모델에 없는 단어
                tempSimilarity = 0
        if tempSimilarity > maxSimilarity:
            find_keyword = temp_token.split('/')[0]
            maxSimilarity = tempSimilarity

    return find_keyword

#들어오는 문장 토크나이징
def tokenize(input_string):
    temp = okt.pos(input_string, norm=True, stem=True)
    return_list = []
    all_return_list = []
    for tempToken in temp:
        all_return_list.append(tempToken)
        if tempToken[1] in ['Noun', 'Adjective', 'Number', 'Alpha', 'Verb']:
            #명사 형용사 숫자 알파벳 동사
            return_list.append(tempToken)
    return return_list, all_return_list

#키워드 선택해주는 함수
def selected_keyword(keyword_list, input_phrases):
    final_return_list = []
    global brand_name
    global sel_color
    global size_num

    #_, _ = tokenize('') #훨씬 더 느려져..

    for input_phrase in input_phrases:
        
        return_list = [] # 반환 할 키워드 목록들

        if cate == '노트북' or cate == '핸드폰':
            if len(input_phrase[2]) > 1000:
                input_phrase[2]= input_phrase[2][:1000]
        else:
            if len(input_phrase[2]) > 500:
                input_phrase[2]= input_phrase[2][:500]
            
        string_list = input_phrase[0] + " | " + input_phrase[2] #한 문장으로 연결

        docs_list, all_docs_list = tokenize(string_list) #원하는 pos의 토큰들만 추출
        #[okt.pos(doc, norm=True, stem=True) for doc in input_strings]

        for keyword in keyword_list[1:]:
            if keyword == '상품명':
                find_keyword = getName(string_list, docs_list, all_docs_list)
            elif keyword =='브랜드':
                find_keyword = getBrand(string_list, docs_list)
            elif keyword =='가격':
                if input_phrase[1] % 1000 == 0 and input_phrase[1] >= 5000:
                    #들어오는 가격이 1000원 단위이면 의미있는 가격이라고 생각하고 반환
                    find_keyword = input_phrase[1]
                else:
                    #아니면 안에 검색
                    find_keyword = getPrice(string_list, docs_list)
            elif keyword =='상태':
                find_keyword = getState(string_list, docs_list)
            elif keyword =='색상':
                find_keyword = getColor(string_list, docs_list)
            elif keyword =='거래방식':
                find_keyword = getMethod(string_list, docs_list)
            elif keyword =='착용횟수':
                find_keyword = getCount(string_list)
            elif keyword =='사이즈':
                find_keyword = getSize(string_list, docs_list)
            elif keyword =='용량':
                find_keyword = getCapacity(string_list, docs_list)
            elif keyword =='사양':
                find_keyword = getSpec(string_list, docs_list)
            elif keyword =='사용기간':
                find_keyword = getTerm(string_list)
            
            return_list.append(find_keyword)
        
        brand_name = ''
        sel_color = ''
        size_num = 0
        
        final_return_list.append(return_list)

    return final_return_list

#카테고리 인식해서 이름, 브랜드 사전 정해주기
def recog_cate(input_list):
    global cate
    global model
    if '착용횟수' in input_list or '사이즈' in input_list:
        model = gensim.models.Word2Vec.load('./model/model30000_20_4')
        if input_list[0].find('남') != -1:
            if input_list[0].find('신발') != -1:
                cate = '신발'
                f = open("./dic/sbrand.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    brand.append(line)
                f.close()
                f = open("./dic/scolor.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    color.append(line)
                f.close()
            else:
                cate = '옷'
                f = open("./dic/mbrand.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    brand.append(line)
                f.close()
                f = open("./dic/mname.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    name.append(line)
                f.close()
                f = open("./dic/ccolor.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    color.append(line)
                f.close()
        else:
            if input_list[0].find('신발') != -1:
                cate = '신발'
                f = open("./dic/sbrand.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    brand.append(line)
                f.close()
                f = open("./dic/scolor.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    color.append(line)
                f.close()
            else:
                cate = '옷'
                f = open("./dic/fbrand.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    brand.append(line)
                f.close()
                f = open("./dic/fname.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    name.append(line)
                f.close()
                f = open("./dic/ccolor.txt", 'r', encoding='utf-8-sig')
                while True:
                    line = f.readline()
                    if not line: break
                    color.append(line)
                f.close()
    elif '용량' in input_list or '사양' in input_list or '사용기간' in input_list:
        if input_list[0].find('노') != -1:
            cate = '노트북'
        else:
            cate = '핸드폰'
        f = open("./dic/ibrand.txt", 'r', encoding='utf-8-sig')
        while True:
            line = f.readline()
            if not line: break
            brand.append(line)
        f.close()
        f = open("./dic/iname.txt", 'r', encoding='utf-8-sig')
        while True:
            line = f.readline()
            if not line: break
            name.append(line)
        f.close()
        f = open("./dic/icolor.txt", 'r', encoding='utf-8-sig')
        while True:
            line = f.readline()
            if not line: break
            color.append(line)
        f.close()
    else:
        if input_list[0].find('신발') != -1:
            cate = '신발'
            f = open("./dic/sbrand.txt", 'r', encoding='utf-8-sig')
            while True:
                line = f.readline()
                if not line: break
                brand.append(line)
            f.close()
            f = open("./dic/scolor.txt", 'r', encoding='utf-8-sig')
            while True:
                line = f.readline()
                if not line: break
                name.append(line)
            f.close()
        else:
            cate = '옷'
            f = open("./dic/fbrand.txt", 'r', encoding='utf-8-sig')
            while True:
                line = f.readline()
                if not line: break
                brand.append(line)
            f.close()
            f = open("./dic/fname.txt", 'r', encoding='utf-8-sig')
            while True:
                line = f.readline()
                if not line: break
                name.append(line)
            f.close()
            f = open("./dic/ccolor.txt", 'r', encoding='utf-8-sig')
            while True:
                line = f.readline()
                if not line: break
                color.append(line)
            f.close()

#단어 하나를 토콘화
def wordTokenize(doc):
    temp = okt.pos(doc, norm=True, stem=True)
    return temp[0][0] + '/' + temp[0][1]

def main(input_args):

    recog_cate(input_args[0])
    return_list = selected_keyword(input_args[0], input_args[1:len(input_args)])
    return return_list