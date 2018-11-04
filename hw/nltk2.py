import re
from nltk.corpus import gutenberg as gu
import nltk
import re
import pandas as pd
import numpy as np
from numpy.linalg import svd
import matplotlib.pyplot as plt


hamlet = gu.words('shakespeare-hamlet.txt')
macbeth = gu.words('shakespeare-macbeth.txt')
caesar = gu.words('shakespeare-caesar.txt')
shakespeare = hamlet+macbeth+caesar
milton = gu.words('milton-paradise.txt')
jane = gu.words('austen-persuasion.txt')
herman = gu.words('melville-moby_dick.txt')

class Frequency:
    def __init__(self,word_list):
        self.word_list = [w.lower() for w in list(filter(lambda w: re.match(r'[\w]',w), word_list))]
        self.size = len(self.word_list)
        self.smaller_list = []
        self.fdist ={}
        self.doc_term_matrix = pd.DataFrame()

    def smaller(self):
        for i in range(self.size//5000 + 1):
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
        self.doc_term_matrix = doc_term_matrix[doc_term_matrix.sum(axis=1)>0] #로 해야 되나요??? 어찌ㅎ바니까아
        self.word_normalized = self.doc_term_matrix.sub(self.doc_term_matrix.mean(axis=1), axis=0).divide(self.doc_term_matrix.std(axis=1), axis=0)
        self.doc_normalized = (self.doc_term_matrix-self.doc_term_matrix.mean(axis=0))
        self.U = None

    def SVD(self,key=None):
        if key == 'word':
            self.U, _, _ = svd(self.word_normalized)
        elif key == 'doc':
            self.U, _, _ = svd(self.doc_normalized)
        else:
          print('Insert KEY')

    def plot(self, key=None, title = None):
        plt.figure()
        u = pd.DataFrame(self.U)
        X = u[0]
        Y = u[1]
        plt.scatter(X, Y)
        if key == 'word':
            for i, txt in enumerate(self.doc_term_matrix.index):
                plt.annotate(txt, (X[i], Y[i]))
                plt.title(title+' words')
        elif key == 'doc':
            plt.title(title)


S = Frequency(shakespeare)
M = Frequency(milton)
J = Frequency(jane)
H = Frequency(herman)

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

S_svd = SVDProblem(S.doc_term_matrix)
M_svd = SVDProblem(M.doc_term_matrix)
J_svd = SVDProblem(J.doc_term_matrix)
H_svd = SVDProblem(H.doc_term_matrix)

S_svd.SVD('word')
S_svd.plot(key='word',title='Shakespeare')

M_svd.SVD('word')
M_svd.plot(key='word',title='Milton')

J_svd.SVD('word')
J_svd.plot(key='word',title='Jane')

H_svd.SVD('word')
H_svd.plot(key='word',title='Herman')

S_svd.SVD('doc')
S_svd.plot(key='doc',title='Shakespeare')

M_svd.SVD('doc')
M_svd.plot(key='doc',title='Milton')

J_svd.SVD('doc')
J_svd.plot(key='doc',title='Jane')

H_svd.SVD('doc')
H_svd.plot(key='doc',title='Herman')

############
### Ver2 ###
############
#
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

S_svd = SVDProblem(S.doc_term_matrix)
M_svd = SVDProblem(M.doc_term_matrix)
J_svd = SVDProblem(J.doc_term_matrix)
H_svd = SVDProblem(H.doc_term_matrix)

# WORD


S_svd.SVD('word')
S_svd.plot(key='word',title='Shakespeare')

M_svd.SVD('word')
M_svd.plot(key='word',title='Milton')

J_svd.SVD('word')
J_svd.plot(key='word',title='Jane')

H_svd.SVD('word')
H_svd.plot(key='word',title='Herman')

# DOCUMENT

S_svd.SVD('doc')
S_svd.plot(key='doc',title='Shakespeare')

M_svd.SVD('doc')
M_svd.plot(key='doc',title='Milton')

J_svd.SVD('doc')
J_svd.plot(key='doc',title='Jane')

H_svd.SVD('doc')
H_svd.plot(key='doc',title='Herman')