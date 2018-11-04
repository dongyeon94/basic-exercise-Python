import pandas as pd
import numpy as np
# import  matplotlib.pyplot as plt


# s = pd.Series([1,3,5,np.nan,6,8])
# print(s)

# d = {'a': 0. ,'b':1.,'c':2.}
# a= pd.Series(d)
# print(a)

######## df indexing 가능
np   = np.array([1,2,3],float)
pd = pd.Series(np)
print(pd)
sal_sta = {'day ':[1,2,3,4,5,6],
            'Visitors':[43,45,33,43,78,44],
           'Revenue':[64,73,62,64,53,66]}
df = pd.DataFrame(sal_sta,index=range(1,7))
print(df)

#
# dd ={'Visitors': [43, 45, 33, 43, 78, 44],
#      'Revenue': [64, 73, 62, 64, 53, 66]}
# df2 = pd.DataFrame(dd,index = ['a','b','c','d','e','f'])
# print(df2)