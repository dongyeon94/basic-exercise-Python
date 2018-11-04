import  re

# 1 번
string = 'Earth is the third planet from thr sun'
result = re.findall(r'\b.{2}',string)
print(result[0],result[1])

# 2 번
string1 = 'abc.test@gmail.com , xyz@test.in , test.first@analyticsvidhya.com , first.test@rest.biz'
result1 = re.findall(r'[@]\w+[.]\w+',string1)
# print(result1)

# 3 번
string2 = 'Amit 34-3456 12-05-2007, XYZ 56-4532 11-11-2011, ABC 67-8945 12-01-2009'
result2 = re.findall(r'..[-]\w+[-]\w+',string2)
print(result2)

string3 = "Earth's gravity interacts with other objects in space, especially the Sun and the Moon."
result3 = re.findall(r'',string3)
print(result3)


string4 = "Earth's gravity interacts with other objects in space, especially the Sun and the Moon."
result4 = re.findall(r"\b[(^a)|(^e)|(^i)|(^o)|(^u)|(^A)|(^E)|(^I)|(^O)|(^U)]\w+",string4)
print(result4)



string5 = ['010-256-1354','010-1234-5576','070-642-0384','010-290*-4858','0105734123']
dd = []
for i in range(len(string5)):
    SS = re.findall(r"[010]+.[-].[0-9].[-].[0-9]\w+",string5[i])
    if  len(SS) !=0:
        dd.append(SS)
print(dd)




