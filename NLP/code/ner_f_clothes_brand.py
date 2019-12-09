from konlpy.tag import Okt #customized twitter
import kss #문장분리 라이브러리

okt = Okt()

import gensim
from pprint import pprint

word2vec = gensim.models.Word2Vec.load('./f_clothes_model50000_40_4')

def read_data(filename):
    with open(filename, 'r', encoding='UTF8') as f:
        data = f.read().splitlines()
    return data

def sentenceSlice(phrase_list):
    sentence_list = []
    for phrase in phrase_list:
        sentence_list.extend(kss.split_sentences(phrase))
    return sentence_list

#들어오는 문장 토크나이징
def tokenize(docs):
    row = 0
    return_list = []
    for doc in docs:
        temp = okt.pos(doc, norm=True, stem=True)
        temp_list = []
        for tempToken in temp:
            if tempToken[1] in ['Adjective', 'Adverb', 'Conjunction', 'Determiner', 'Eomi', 'Josa', 'Noun', 'Suffix', 'Verb']:
                #명사 형용사 숫자 알파벳 동사
                temp_list.append('/'.join(tempToken))
        return_list.append(temp_list)
        row += 1
    return return_list

comments = read_data('./data/ftop.txt')
comments += read_data('./data/fbottom.txt')
comments += read_data('./data/ftop2.txt')
comments += read_data('./data/fbottom2.txt')
comments += read_data('./data/ftop3.txt')

comments = sentenceSlice(comments)
comments = tokenize(comments)

from collections import defaultdict

#단어를 스캔하고 사전 만들어
def scan_vocabulary(sents, min_count, verbose=False):
    counter = defaultdict(int)
    for i, sent in enumerate(sents):
        if verbose and i % 100000 == 0:
            print('\rscanning vocabulary .. from %d sents' % i, end='')
        for word in sent:
            counter[word] += 1
    counter = {word:count for word, count in counter.items()
               if count >= min_count}
    idx_to_vocab = [vocab for vocab in sorted(counter,
                    key=lambda x:-counter[x])]
    vocab_to_idx = {vocab:idx for idx, vocab in enumerate(idx_to_vocab)}
    idx_to_count = [counter[vocab] for vocab in idx_to_vocab]
    if verbose:
        print('\rscanning vocabulary was done. %d terms from %d sents' % (len(idx_to_vocab), i+1))
    return vocab_to_idx, idx_to_vocab, idx_to_count
# vocab_to_idx : str:int 형식의 indexer
# idx_to_vocab : index 별 단어
# idx_to_count : index 별 나온 횟수
# dataset에 일정 빈도 이상으로 나오는 단어 인덱스 붙여놓기

vocab_to_idx, idx_to_vocab, idx_to_count = scan_vocabulary(
    comments, min_count=40, verbose=True)

print(idx_to_vocab[:5]) # ['영화', '이', '관람', '객', '의']
print(idx_to_count[:5]) # [1128809, 866305, 600351, 526070, 489950]

######################feature로 사용할 것들 정의해줘######################################3

#윈도우를 사용해서 앞뒤의 단어를 feature로 이용
#피쳐를 feature index로 incode / feature index 출력
def feature_to_idx(i, j, vocab_idx, window, n_terms):
    #현재 단어 x[0]의 위치 i
    #앞뒤 단어인 -1 이나 1인 위치 j
    #j위치의 단어의 index
    if j < i:
        return n_terms * (j - i + window) + vocab_idx
    else:
        return n_terms * (j - i + window - 1) + vocab_idx

#feature index를 feature로 decode
def idx_to_feature(feature_idx, idx_to_vocab, window):
    # 몫
    position = feature_idx // len(idx_to_vocab)
    if position < window:
        feature = 'X[-%d] = ' % (window - position)
    else:
        feature = 'X[%d] = ' % (position - window + 1)
    # 나머지
    vocab_idx = feature_idx % len(idx_to_vocab)
    feature += idx_to_vocab[vocab_idx]
    return feature

######################window classification 데이터 만들어#######################333

import numpy as np
from scipy.sparse import csr_matrix

#가운데를 기준으로 앞뒤 두개의 co occurrence를 계산하는 매트릭스
#sparse 니까 row와 column을 따로
#scan vocabulary에 없으면 건너띄고 context word범위는 맨앞에서 맨뒤가 되도록 index범위 확인
def create_window_cooccurrence_matrix(vocab_to_idx, sentences, window=4, verbose=True):

    n_terms = len(vocab_to_idx)

    rows = []
    cols = []
    words = []

    row_idx = 0
    col_idx = window * 2 * n_terms

    for i_sent, sent in enumerate(sentences):

        if verbose and i_sent % 10000 == 0:
            print('\rcreating train dataset {} rows from {} sents'.format(row_idx, i_sent), end='')

        n_words = len(sent)

        for i, word in enumerate(sent):
            #사전에 없으면 건너뜀
            if not (word in vocab_to_idx):
                continue
            
            #각 row column을 따로 모음
            b = max(0, i - window)
            e = min(i + window + 1, n_words)

            #피처에다가 피처인덱스들을 넣어놓음
            features = []
            for j in range(b, e):
                if i == j:
                    continue
                j_idx = vocab_to_idx.get(sent[j], -1)
                if j_idx == -1:
                    continue
                features.append(feature_to_idx(i, j, j_idx, window, n_terms))

            if not features:
                continue

            # sparse matrix element
            for col in features:
                rows.append(row_idx)
                cols.append(col)

            # words element
            words.append(word)

            row_idx += 1

    if verbose:
        print('\rtrain dataset {} rows from {} sents was created    '.format(row_idx, i_sent))

    # to csr matrix
    rows = np.asarray(rows, dtype=np.int)
    cols = np.asarray(cols, dtype=np.int)
    data = np.ones(rows.shape[0], dtype=np.int)
    X = csr_matrix((data, (rows, cols)), shape=(row_idx, col_idx))

    return X, words

window = 2

#co-occurence matrix와 각 row에 해당하는 단어 학습
X, words = create_window_cooccurrence_matrix(
    vocab_to_idx, comments, window)

print(X.shape) #(42981576, 278164)

f = open("f_brand_name_ner_40_4.txt", 'w')

#아 기억났다 _는 버리는 변수명으로 잘 쓰인댔어
#seed_words 타입은 set이야 집합!!
p_seed_list = ['나이키/Noun', '데상트/Noun', '디스커버리/Noun', '휠라/Noun', '퓨마/Noun', '에이치/Noun', '미우미우/Noun', '에르메스/Noun', '럭키/Noun'
        , '티니/Noun', '타미힐피거/Noun']

pseed_words = {word for word, _ in word2vec.wv.most_similar(p_seed_list[0], topn=20) if word.split('/')[1] == 'Noun'}
for pword in p_seed_list[1:]:
    pseed_words.update({word for word, _ in word2vec.wv.most_similar(pword, topn=20) if word.split('/')[1] == 'Noun'})

pseed_words = pseed_words | set(p_seed_list)
print(len(pseed_words)) 

n_seed_list = ['사이즈/Noun', '자켓/Noun', '바람막이/Noun', '한정판/Noun', '숏/Noun', '수세미/Noun', '수면/Noun', '야상패딩/Noun', '디자이너/Noun'
        , '수면/Noun', '등산/Noun', '눕다/Verb', '검다/Adjective', '네이비/Noun', '블랙/Noun', '신민아/Noun', '연아/Noun', '도트/Noun', '뽀글이/Noun', '동전지갑/Noun']

nseed_words = {word for word, _ in word2vec.wv.most_similar(n_seed_list[0], topn=20) if word.split('/')[1] == 'Noun'}
for nword in n_seed_list[1:]:
    nseed_words.update({word for word, _ in word2vec.wv.most_similar(nword, topn=20) if word.split('/')[1] == 'Noun'})

nseed_words = nseed_words | set(n_seed_list)
print(len(nseed_words))

seed_words = pseed_words - nseed_words
#78 역도 등산 하이브리드 눕다 동사 이동수 바람막이

print(seed_words)
print(len(seed_words))

for word in seed_words:
    f.write(word + '\n')

print(len(seed_words)) # 172

real_n_seed_list = ['화이트/Noun', '핑크/Noun']

real_nseed_words = {word for word, _ in word2vec.wv.most_similar(real_n_seed_list[0], topn=20) if word.split('/')[1] == 'Noun'}
for nword in real_n_seed_list[1:]:
    real_nseed_words.update({word for word, _ in word2vec.wv.most_similar(nword, topn=20) if word.split('/')[1] == 'Noun'})

print(real_nseed_words)

############Word2Vec의 유사어를 이용해서 label vector만들기##################

#위위 에서 만든 X의 row에 해당되는 단어가 seed_words 에 포함되면 1 안되면 0
y = np.zeros(X.shape[0], dtype=np.int)
for i, word in enumerate(words):
    if word in seed_words:
        y[i] = 1

y.sum() # 361394
#partially positive labeled imbalanced data 파지티브의 비율이 적음

############로지스틱 리그레이션을 이용해서 window classifier###################3333

#seed words를 positive class로 예측
#0 1로 되어있긴한데 사실 맞는데 0인거 있지만 예측 확률값은 높겠지?
#training error를 named entity의 힌트로 이용
from sklearn.linear_model import LogisticRegression

logistic = LogisticRegression()
logistic.fit(X, y)
y_pred = logistic.predict(X)
y_prob = logistic.predict_proba(X)[:,1]

#seed words에 포함되지않아도 0.05보다 높은 prediction probability를 받으면
#named entity score가 1에 가깝에 정해짐
from collections import Counter

# word count
word_counter = Counter(words)

# prediction count
pred_pos = defaultdict(int)
for row in np.where(y_prob >= 0.05)[0]:
    pred_pos[words[row]] += 1
pred_pos = {word:pos/word_counter[word] for word, pos in pred_pos.items()}

#############결과확인################
#named entity score이 큰 순서대로 상위 1000->500의 단어 선택 (seed words 제외)

for word, prob in sorted(pred_pos.items(), key=lambda x:-x[1])[:800]:
    if word.split('/')[1] != 'Noun':
        continue
    if word in seed_words:
        continue
    if word in real_nseed_words:
        continue
    idx = vocab_to_idx[word]
    count = idx_to_count[idx]
    f.write(str(word)+'\n')
    print(str(word))

f.close()