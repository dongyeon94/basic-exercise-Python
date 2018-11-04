###########################
### BeautifulSoup Module###
###########################


#################
### RE MODULE ###
#################
import re

# 1
string ="Earth is the third planet from the Sun"
for i in string.split(' '):
    print(re.findall(r'^[\w]{2}',i)[0])

# 2
string = 'abc.test@gmail.com, xyz@test.in, test.first@analyticsvidhya.com, first.test@rest.biz'
for i in string.split(', '):
    domain = re.search(r'@[\w.]+',i)
    # sub으로 하기
    print(domain.group())

# 3
string = 'Amit 34-3456 12-05-2007, XYZ 56-4532 11-11-2011, ABC 67-8945 12-01-2009'
for i in string.split(', '):
    date = re.search(r'\d{2}-\d{2}-\d{4}', i)
    print(date.group())

# 4
string = "Earth's gravity interacts with other objects in space, especially the Sun and the Moon."
for i in string.split(' '):
    vowel = re.match(r'\b[aeiouAEIOU]\w*',i)
    if vowel:
        print(vowel.group())

# 5
lst = ['010-256-1354', '010-1234-5576', '070-642-0384', '010-290*-4858', '0105734123']
for num in lst:
    phone = re.match(r'010-\d{3,4}-\d{4}',num)
    if phone:
        print("yes")
    else:
        print("no")

################
# NLTK PROJECT #
################
"""
각 작가 별로 term-doc를 따로 만든 경우로 했습니다.
뒤에 작가들의 term-doc을 모두 합친 경우도 첨부되어 있습니다.
"""

"""
편의를 위해 stopword를 제거하지 않은 상태에서 NLTK PROJECT 1,2를 한번에 진행하고,
stopword를 제고하고 NLTK PROJECT 1,2를 한번에 진행하였습니다.
"""

from nltk.corpus import gutenberg as gu
import nltk
import re
import pandas as pd
import numpy as np
from numpy.linalg import svd
import matplotlib.pyplot as plt

for file in gu.fileids():
    print(file)

hamlet = gu.words('shakespeare-hamlet.txt')
macbeth = gu.words('shakespeare-macbeth.txt')
caesar = gu.words('shakespeare-caesar.txt')
shakespeare = hamlet+macbeth+caesar
milton = gu.words('milton-paradise.txt')
jane = gu.words('austen-persuasion.txt')
herman = gu.words('melville-moby_dick.txt')

#########################
# VER 2 : stopword 포함 #
########################
class Frequency:

    def __init__(self,word_list):
        self.word_list = [w.lower() for w in list(filter(lambda w: re.match(r'[\w]',w), word_list))]
        self.size = len(self.word_list)
        self.smaller_list = []
        self.fdist ={}
        self.doc_term_matrix = pd.DataFrame()

    def smaller(self):
        for i in range(self.size//5000 + 1):
            # print(self.word_list[5000*i:5000*(i+1)])
            self.smaller_list.append(self.word_list[5000*i:5000*(i+1)])

    def frequency(self,freqWords):
        self.doc_term_matrix = pd.DataFrame()
        for i in range(len(self.smaller_list)):
            temp = nltk.FreqDist(self.smaller_list[i])
            temp_fdist = [temp[key] for key in freqWords]
            self.doc_term_matrix['%d'%i] = pd.Series(temp_fdist,index=freqWords)
        self.doc_term_matrix.index = freqWords

    def average(self):
        return self.doc_term_matrix.mean(axis=1)

class SVDProblem:
    def __init__(self,doc_term_matrix):
        self.doc_term_matrix = doc_term_matrix[doc_term_matrix.sum(axis=1)>0]
        self.word_normalized = self.doc_term_matrix.sub(self.doc_term_matrix.mean(axis=1), axis=0).divide(self.doc_term_matrix.std(axis=1), axis=0)
        # self.doc_normalized = (self.doc_term_matrix-self.doc_term_matrix.mean(axis=0))
        self.U = None

    def SVD(self,key=None):
        if key == 'word':
            self.U, _, _ = svd(self.word_normalized)
        elif key == 'doc':
            _, _, self.U = svd(self.word_normalized)
        else:
            print('Insert KEY')

    def plot(self, key=None, color = None):
        if key == 'word':
            u = pd.DataFrame(self.U)
            X = u[0]
            Y = u[1]
            plt.scatter(X, Y, c = color)
            for i, txt in enumerate(self.doc_term_matrix.index):
                plt.annotate(txt, (X[i], Y[i]))
        elif key == 'doc':
            u = pd.DataFrame(self.U.transpose())
            X = u[0]
            Y = u[1]
            plt.scatter(X, Y, c = color)
            # plt.title(title)

S = Frequency(shakespeare)
M = Frequency(milton)
J = Frequency(jane)
H = Frequency(herman)

# 셰익스피어 작품의 경우 'have'가 'haue'로 표기되어 있어 이에 대한 전처리가 필요함
for i,word in enumerate(S.word_list):
    if word == 'haue':
        S.word_list[i] = 'have'

total = S.word_list + M.word_list + J.word_list + H.word_list

fdist = nltk.FreqDist(total)
fdist
freqList = fdist.most_common(50)
freqWords = [w for w,_ in freqList]

S.smaller()
S.frequency(freqWords)
S.doc_term_matrix

M.smaller()
M.frequency(freqWords)
M.doc_term_matrix

J.smaller()
J.frequency(freqWords)
J.doc_term_matrix

H.smaller()
H.frequency(freqWords)
H.doc_term_matrix

df_avg = pd.DataFrame()
df_avg['Shakespeare'] = S.average()
df_avg['Milton'] = M.average()
df_avg['Jane'] = J.average()
df_avg['Herman'] = H.average()
df_avg.index = list(range(50))

df_avg.plot()
for i, txt in enumerate(freqWords):
    plt.annotate(txt, (df_avg.index[i],df_avg.Herman[i]))
plt.title('means')
plt.show()

S_svd = SVDProblem(S.doc_term_matrix)
M_svd = SVDProblem(M.doc_term_matrix)
J_svd = SVDProblem(J.doc_term_matrix)
H_svd = SVDProblem(H.doc_term_matrix)

# WORD

plt.figure()
S_svd.SVD('word')
S_svd.plot(key='word',color='red')
M_svd.SVD('word')
M_svd.plot(key='word',color='blue')
J_svd.SVD('word')
J_svd.plot(key='word',color='green')
H_svd.SVD('word')
H_svd.plot(key='word',color='orange')
plt.show()

# DOCUMENT

plt.figure()
S_svd.SVD('doc')
S_svd.plot(key='doc', color='red')
M_svd.SVD('doc')
M_svd.plot(key='doc', color='blue')
J_svd.SVD('doc')
J_svd.plot(key='doc', color='green')
H_svd.SVD('doc')
H_svd.plot(key='doc', color='orange')
plt.show()

#########################
# VER 2 : stopword 제외 #
########################

from nltk.corpus import stopwords
stop = stopwords.words('english')

total2 = list(filter(lambda w: w not in stop, total))
fdist2 = nltk.FreqDist(total2)
freqList2 = fdist2.most_common(50)
freqWords2 = [w for w,_ in freqList2]

S.frequency(freqWords2)
S.doc_term_matrix

M.frequency(freqWords2)
M.doc_term_matrix

J.frequency(freqWords2)
J.doc_term_matrix

H.frequency(freqWords2)
H.doc_term_matrix

df_avg = pd.DataFrame()
df_avg['Shakespeare'] = S.average()
df_avg['Milton'] = M.average()
df_avg['Jane'] = J.average()
df_avg['Herman'] = H.average()
df_avg.index = list(range(50))

df_avg.plot()
for i, txt in enumerate(freqWords2):
    plt.annotate(txt, (df_avg.index[i],df_avg.Herman[i]))
plt.title('means')
plt.show()

S_svd = SVDProblem(S.doc_term_matrix)
M_svd = SVDProblem(M.doc_term_matrix)
J_svd = SVDProblem(J.doc_term_matrix)
H_svd = SVDProblem(H.doc_term_matrix)

# WORD

plt.figure()
S_svd.SVD('word')
S_svd.plot(key='word',color='red')
M_svd.SVD('word')
M_svd.plot(key='word',color='blue')
J_svd.SVD('word')
J_svd.plot(key='word',color='green')
H_svd.SVD('word')
H_svd.plot(key='word',color='orange')
plt.show()

# DOCUMENT

plt.figure()
S_svd.SVD('doc')
S_svd.plot(key='doc', color='red')
M_svd.SVD('doc')
M_svd.plot(key='doc', color='blue')
J_svd.SVD('doc')
J_svd.plot(key='doc', color='green')
H_svd.SVD('doc')
H_svd.plot(key='doc', color='orange')
plt.show()

"""
모든 작가들의 term-doc를 한번에 한 경우
"""

#########################
# VER 1 : stopword 포함 #
########################

S.frequency(freqWords)
S.doc_term_matrix
M.frequency(freqWords)
M.doc_term_matrix
J.frequency(freqWords)
J.doc_term_matrix
H.frequency(freqWords)
H.doc_term_matrix

total_doc_term = pd.DataFrame()
total_doc_term = total_doc_term.append(S.doc_term_matrix.transpose(), ignore_index=True) # 14
total_doc_term = total_doc_term.append(M.doc_term_matrix.transpose(),ignore_index=True) # 17
total_doc_term = total_doc_term.append(J.doc_term_matrix.transpose(), ignore_index=True) # 17
total_doc_term = total_doc_term.append(H.doc_term_matrix.transpose(), ignore_index=True) # 44

norm = (total_doc_term-total_doc_term.mean(axis=0))/total_doc_term.std(axis=0)
norm = norm.sub(norm.mean(axis=1),axis=0)

doc, _, word = svd(norm)
word = word.transpose()

plt.figure()
X = word[:, 0]
Y = word[:, 1]
plt.scatter(X,Y)
plt.show()

plt.figure()
X = doc[:14, 0]
Y = doc[:14, 1]
plt.scatter(X,Y, color = 'red')
X = doc[14:31, 0]
Y = doc[14:31, 1]
plt.scatter(X,Y, color = 'blue')
X = doc[31:49, 0]
Y = doc[31:49, 1]
plt.scatter(X,Y, color = 'orange')
X = doc[49:, 0]
Y = doc[49:, 1]
plt.scatter(X,Y, color = 'green')
for i, txt in enumerate(total_doc_term.columns):
    plt.annotate(txt, (X[i], Y[i]))
plt.show()

#########################
# VER 2 : stopword 제외 #
########################

S.frequency(freqWords2)
S.doc_term_matrix
M.frequency(freqWords2)
M.doc_term_matrix
J.frequency(freqWords2)
J.doc_term_matrix
H.frequency(freqWords2)
H.doc_term_matrix

total_doc_term = pd.DataFrame()
total_doc_term = total_doc_term.append(S.doc_term_matrix.transpose(), ignore_index=True) # 14
total_doc_term = total_doc_term.append(M.doc_term_matrix.transpose(),ignore_index=True) # 17
total_doc_term = total_doc_term.append(J.doc_term_matrix.transpose(), ignore_index=True) # 17
total_doc_term = total_doc_term.append(H.doc_term_matrix.transpose(), ignore_index=True) # 44

norm = (total_doc_term-total_doc_term.mean(axis=0))/total_doc_term.std(axis=0)
norm = norm.sub(norm.mean(axis=1),axis=0)

doc, _, word = svd(norm)
word = word.transpose()

plt.figure()
X = word[:, 0]
Y = word[:, 1]
plt.scatter(X,Y)
for i, txt in enumerate(total_doc_term.columns):
    plt.annotate(txt, (X[i], Y[i]))
plt.show()

plt.figure()
X = doc[:14, 0]
Y = doc[:14, 1]
plt.scatter(X,Y, color = 'red')
X = doc[14:31, 0]
Y = doc[14:31, 1]
plt.scatter(X,Y, color = 'blue')
X = doc[31:49, 0]
Y = doc[31:49, 1]
plt.scatter(X,Y, color = 'orange')
X = doc[49:, 0]
Y = doc[49:, 1]
plt.scatter(X,Y, color = 'green')
plt.show()
