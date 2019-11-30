import re
import os
from pprint import pprint
from konlpy.tag import Okt
import gensim
import operator
from gensim.test.utils import datapath

okt = Okt()

model = gensim.models.Word2Vec.load("./model30000_20_4")
# model = gensim.models.Word2Vec.load_word2vec_format('model30000_20_4.bin', binary=True)
# model = gensim.models.KeyedVectors.load_word2vec_format(datapath('model30000_20_4'), binary=False)
#fastTextModel = gensim.models.FastText.load('./fastTextModel')
#fastTextModel = gensim.models.Word2Vec.load('./ko.bin')
word_vectors = model.wv

name = []
brand = []

def getName(docs_list):
    return_name = ""
    flag = 0
    appearance_dis = 0

    for t, p in docs_list:
        for c in name:
            if c.split("/")[0] == t:
                return_name = return_name + t + " "
                flag = 1
        if flag == 1:
            flag = flag + 1
            continue
        elif flag ==2:
            break
    return return_name

def getBrand(docs_list):
    #브랜드 반환
    for b in brand:
        for t, p in docs_list:
            if b.split("/")[0] == t:
                return t
    return "?"

def getPrice(string_list, docs_list):
    find_keyword = re.findall("[0-9일이삼사오육칠팔구십천만천백십/., ]*원",string_list)

    if len(find_keyword) == 1 :
        find_keyword = find_keyword[0].replace(" ", "")
        return find_keyword
    elif len(find_keyword) > 1:
        find_n_distance = getMeanDistance(docs_list, [wordTokenize(ex_str)for ex_str in find_keyword], ['정가', '구입'])
        if len(find_n_distance) == 0:
            find_keyword = find_keyword[0]
        else:
            find_keyword = find_keyword[find_n_distance.index(max(find_n_distance))]
    else:
        find_keyword = '?'
        searchList = ["택포", "판매가", "가격", "착불", "희망가", "운포"]
        tempTokenList = getAroundToken(docs_list, searchList)

        tokenList = []
        for t in tempTokenList:
            if t[1] == 'Number':
                tokenList.append(t)

        if len(tokenList) == 1:
            find_keyword = tokenList[0][0]
        elif len(tokenList) > 1:
            find_n_distance = getMeanDistance(docs_list, tokenList, ['정가', '구입'])
            if len(find_n_distance) == 0:
                find_keyword = tokenList[1][0]
            else:
                find_keyword = tokenList[find_n_distance.index(max(find_n_distance))][0]

    find_keyword = find_keyword.replace(" ", "")
    return find_keyword

def getState(string_list, docs_list):
    #상태 반환
    find_keyword = re.findall("\w+급"," ".join(string_list))

    if len(find_keyword) == 1 :
        find_keyword = find_keyword[0]
    elif len(find_keyword) > 1:
        #TODO 여러개일때 어떡할까
        find_keyword = '여러개야' 
    else:
        find_keyword = '?'

        searchList = ["상태", "사용감"]

        tokenList= getAroundToken(docs_list, searchList)

        for t in tokenList:
            if t[1] == 'Noun':
                find_keyword = t[0]

    find_keyword = find_keyword.replace(" ", "")
    return find_keyword

def getColor(string_list, docs_list):
    find_keyword = re.findall("\w+ ?색",string_list)

    if len(find_keyword) == 1 :
        find_keyword = find_keyword[0].replace("색", "")
        find_keyword = find_keyword.replace(" ", "")
        return find_keyword
    elif len(find_keyword) > 1:
        #TODO 베이지(영어를 한국어로)를 예시토큰할지 빨강(그냥 색이라는 단어없는 색깔)을 예시토큰할지 고민
        find_keyword = getMostSimilarityVerString(find_keyword, "베이지")
    else:
        find_keyword = '?'
        searchList = ["색상", "컬러"]
        tokenList= getAroundToken(docs_list, searchList)
        find_keyword = getMostSimilarityVerToken(tokenList, "베이지")

    find_keyword = find_keyword.replace(" ", "")
    return find_keyword

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
    searchList = ['미착용', '새상품', '미개봉', '새제품', '미 착용', '새 상품', '미 개봉', '새 제품'] #완전히 한번도 안입은 거

    for searchToken in searchList:
        if searchToken in string_list:
            find_keyword = '사용안함'
            return find_keyword

    temp_keyword = re.findall("\w*-*~*\w+ ?[번회]",string_list)

    if len(temp_keyword) == 1 :
        find_keyword = temp_keyword[0]
    elif len(temp_keyword) > 1:
        find_keyword = '여러개야'
    else:
        find_keyword = '?'

    find_keyword = find_keyword.replace(" ", "")
    return find_keyword

def getSize(docs_list):
    searchList = ["사이즈", "size", "싸이즈", "싸쥬"]

    tokenList = getAroundToken(docs_list, searchList)

    token = 1000000

    for t in tokenList:
        if t[0] == 'free'or t[0] == 'FREE' or t[0] == '프리':
            return t[0]
        if t[1] == 'Alpha':
            return t[0]
        if t[1] == 'Number':
            try:
                if token > int(t[0]):
                    token = int(t[0])
            except:
                return t[0]
                
    if token == 1000000:
        return '?'
    else:
        return token

def getCapacity(string_list):
    #용량 반환
    find_keyword = re.findall("\w+ ?GB"," ".join(string_list))

    if len(find_keyword) == 1 :
        find_keyword = find_keyword[0]
    elif len(find_keyword) > 1:
        #TODO 여러개일때 어떡할까
        find_keyword = '여러개야' 
    else:
        find_keyword = '?'

    find_keyword = find_keyword.replace(" ", "")
    return find_keyword
  
def getTerm(string_list):
    #사용기간 반환
    find_keyword = re.findall("\w+년|\w+월|\w+일"," ".join(string_list))

    if len(find_keyword) == 1 :
        find_keyword = find_keyword[0]
    elif len(find_keyword) > 1:
        #TODO 여러개일때 어떡할까
        find_keyword = '여러개야' 
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
    mean_dis_list = []
    for tl in token_list:
        #이 토큰 리스트안에 내가 찾을 리스트가 있으면 그거랑 우리가 찾아야하는 토큰의 위치 비교
        if tl in find_token_list:
            index_num[find_token_list.index(tl)] = token_list.index(tl)

    count = 0
    col = 0
    for fsl in find_str_list:
        for t, p in token_list:
            if wordTokenize(fsl).split("/")[0] == t:
                count = count + 1
                mean_dis_list = mean_dis_list + [abs(ftln - col) for ftln in index_num]
            col = col + 1

    if count == 0:
        return list(range(len(mean_dis_list)))
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
    for tempToken in temp:
        if tempToken[1] in ['Noun', 'Adjective', 'Number', 'Alpha', 'Verb']:
            #명사 형용사 숫자 알파벳 동사
            return_list.append(tempToken)
    return return_list

#키워드 선택해주는 함수
def selected_keyword(keyword_list, input_phrases):
    final_return_list = []

    for input_phrase in input_phrases:
        return_list = [] # 반환 할 키워드 목록들

        string_list = input_phrase[0] + " " + input_phrase[2] #한 문장으로 연결

        docs_list = tokenize(string_list) #원하는 pos의 토큰들만 추출
        #[okt.pos(doc, norm=True, stem=True) for doc in input_strings]
        find_keyword = ""
        for keyword in keyword_list[1:]:
            if keyword == '이름':
                find_keyword = getName(docs_list)
            elif keyword =='브랜드':
                find_keyword = getBrand(docs_list)
            elif keyword =='가격':
                if input_phrase[1] % 1000 == 0 and input_phrase[1] >= 5000:
                    #들어오는 가격이 1000원 단위이면 의미있는 가격이라고 생각하고 반환
                    find_keyword = input_phrase[1]
                else:
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
                find_keyword = getSize(docs_list)
            elif keyword =='용량':
                find_keyword = getCapacity(docs_list)
            elif keyword =='사양':
                find_keyword = getSpec(string_list, docs_list)
            elif keyword =='사용기간':
                find_keyword = getTerm(string_list)
            
            return_list.append(find_keyword)
        
        final_return_list.append(return_list)

    return final_return_list

#카테고리 인식해서 이름, 브랜드 사전 정해주기
def get_dic(input_list):
    if '착용횟수' or '사이즈' in input_list:
        if input_list[0].find('남') != -1:
            f = open("./mbrand.txt", 'r', encoding='UTF8')
            while True:
                line = f.readline()
                if not line: break
                brand.append(line)
            f.close()
            f = open("./mname.txt", 'r', encoding='UTF8')
            while True:
                line = f.readline()
                if not line: break
                name.append(line)
            f.close()
        else:
            f = open("./fbrand.txt", 'r', encoding='UTF8')
            while True:
                line = f.readline()
                if not line: break
                brand.append(line)
            f.close()
            f = open("./fname.txt", 'r', encoding='UTF8')
            while True:
                line = f.readline()
                if not line: break
                name.append(line)
            f.close()
    elif '용량' or '사양' or '사용기간' in input_list:
        f = open("./ibrand.txt", 'r', encoding='UTF8')
        while True:
            line = f.readline()
            if not line: break
            brand.append(line)
        f.close()
        f = open("./iname.txt", 'r', encoding='UTF8')
        while True:
            line = f.readline()
            if not line: break
            name.append(line)
        f.close()
    else:
        f = open("./fbrand.txt", 'r', encoding='UTF8')
        while True:
            line = f.readline()
            if not line: break
            brand.append(line)
        f.close()
        f = open("./fname.txt", 'r', encoding='UTF8')
        while True:
            line = f.readline()
            if not line: break
            name.append(line)
        f.close()


#단어 하나를 토콘화
def wordTokenize(doc):
    temp = okt.pos(doc, norm=True, stem=True)
    return temp[0][0] + '/' + temp[0][1]

def main(input_args):

    get_dic(input_args[0])

    return_list = selected_keyword(input_args[0], input_args[1:len(input_args)])

    return return_list