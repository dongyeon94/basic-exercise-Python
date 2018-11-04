import pandas as pd
import numpy as np

exam_data = {'name' :['Anastasia','Catherine','Cahill','James','Emily','Michael','Monica','Laura','Kevin','Jordan'],
              'score': [13,9.5,16.5,np.nan, 11,20,17,np.nan,8.5,19],
             'attempts' :[1,3,3,2,2,3,2,3,2,1],
             'qualify': ['yes','no','yes','no','no','yes','yes','no','no','yes']}

labels = ['a','b','c','d','e','f','g','h','i','j']
df = pd.DataFrame(exam_data, index = labels)

print(df)

##1-1
df1 = df[['name','score']]
print(df1)
## 1-2
print(df[:3])

## 1-3
df.iloc[[1,2,5,6]][['name','score']]

## 1-4
df[df['attempts']>2]

## ______________________________________
## 2-1
df[df['score'].isna()]

## 2-2
df[(df['attempts']<2)  &  (df['score']>15)]

## 2-3
df['attempts'].sum()

## 2-4
df['score'].mean()


## 3-1
df.loc['k']=['Saya',17.5,2,'yes']
df
## 3-2
df = df.drop('k', axis=0)
df

## 3-3
df.drop('attempts' , axis = 1)
df

## 3-4
gf = df.groupby(['attempts'])
gf.sum()



##  4
exam2_data = {'name': ['Anastasia','Catherine','Ronaldo','James','Messi','Michael','Monica','Laura','Klassen','Jonas'],
              'score2': [11,20,16.5,np.nan,10,15,20,np.nan,8,8]}
labels2 = ['a','b','c','d','e','f','g','h','i','j']
df2 = pd.DataFrame(exam2_data,index =labels2)

result = pd.merge(df ,df2 , on='name')
result

