import numpy  as n
import scipy
import scipy.linalg

a= n.array([[2,1,1],[4,-6,0],[-2,7,2]])
P,L,U = scipy.linalg.lu(a)

print(P)
print()
print(L)
print()
print(U)