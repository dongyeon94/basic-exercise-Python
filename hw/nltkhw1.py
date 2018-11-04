from nltk.corpus import gutenberg
import  nltk
import pandas as pd
import re
import pandas as pd
import matplotlib.pyplot as plt



for file in gutenberg.fileids():
      pass

shakespeare = gutenberg.words('shakespeare-hamlet.txt') + gutenberg.words('shakespeare-macbeth.txt') + gutenberg.words('shakespeare-caesar.txt')
milton      = gutenberg.words('milton-paradise.txt')
austen      = gutenberg.words('austen-persuasion.txt')
melville    = gutenberg.words('melville-moby_dick.txt')[:80000]

shakespeare_word  = [word.lower() for  word in shakespeare  if word.isalpha()] ## 제거 한게 69340 개 6만개.
milton_word       = [word.lower() for  word in milton if word.isalpha()]
austen_word       = [word.lower() for  word in austen if word.isalpha()]
melville_word     = [word.lower() for  word in melville if word.isalpha()]

shakespeare_list, milton_list, austen_list, melville_list = [], [], [], []
for i in range(0, len(shakespeare_word), 5000):
      shakespeare_list.append(shakespeare_word[i:i + 5000])

for i in range(0, len(milton_word), 5000):
      milton_list.append(milton_word[i:i + 5000])

for i in range(0, len(austen_word), 5000):
      austen_list.append(austen_word[i:i + 5000])

for i in range(0, len(melville_word), 5000):
      melville_list.append(melville_word[i:i + 5000])


shakespeare_list_final, milton_list_final, austen_list_final, melville_list_final = [], [], [], []
for i in range(0, len(shakespeare_list)):
      shakespeare_list_final.append(nltk.FreqDist(shakespeare_list[i]))

for i in range(0, len(milton_list)):
      milton_list_final.append(nltk.FreqDist(milton_list[i]))

for i in range(0, len(austen_list)):
      austen_list_final.append(nltk.FreqDist(austen_list[i]))

for i in range(0, len(melville_list)):
      melville_list_final.append(nltk.FreqDist(melville_list[i]))



shakespeare_matrix,milton_matrix,austen_matrix,melville_matrix = [],[],[],[]
for i in range(len(shakespeare_list_final)):
      shakespeare_matrix.append(pd.Series(shakespeare_list_final[i], index=shakespeare_list_final[i].keys()))

for i in range(len(milton_list_final)):
      milton_matrix.append(pd.Series(milton_list_final[i], index=milton_list_final[i].keys()))

for i in range(len(austen_list_final)):
      austen_matrix.append(pd.Series(austen_list_final[i], index=austen_list_final[i].keys()))

for i in range(len(melville_list_final)):
      melville_matrix.append(pd.Series(melville_list_final[i], index=melville_list_final[i].keys()))




shakespeare_df, milton_df, austen_df,melville_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

for i in range(len(shakespeare_matrix)):
      shakespeare_df[i] = shakespeare_matrix[i]

for i in range(len(milton_matrix)):
      milton_df[i] = milton_matrix[i]

for i in range(len(austen_matrix)):
      austen_df[i] = austen_matrix[i]

for i in range(len(melville_matrix)):
      melville_df[i] = melville_matrix[i]




shakespeare_df , milton_df  =   shakespeare_df.fillna(0) , milton_df.fillna(0)
austen_df , melville_df     = austen_df.fillna(0) , melville_df.fillna(0)
shakespeare_mean, milton_mean =shakespeare_df.sum(axis=1)/len(shakespeare_list) , milton_df.sum(axis=1)/len(milton_list)
austen_mean , melville_mean   =austen_df.sum(axis=1)/len(austen_list),  melville_df.sum(axis=1)/len(melville_list)
shakespeare_df_sort , milton_df_sort = shakespeare_mean.sort_values(ascending=False), milton_mean.sort_values(ascending=False)
austen_df_sort , melville_df_sort    = austen_mean.sort_values(ascending=False)  ,melville_mean.sort_values(ascending=False)



plt.plot(range(50),shakespeare_df_sort[:50],color='red')
plt.plot(range(50),milton_df_sort[:50],color='black')
plt.plot(range(50),austen_df_sort[:50],color='green')
plt.plot(range(50),melville_df_sort[:50],color='blue')
plt.show()