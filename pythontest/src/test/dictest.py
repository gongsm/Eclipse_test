D = {'spam':2,'ham':1,'eggs':3}
print D.get('spam')
print D['spam']
D2 ={'toast':4,'muffin':5}
D.update(D2)
print D


print D.popitem()
print D

for d in D:
    print d,'\t',D[d]


mel = {'jobs':['trainer','writer'],
       'name':'mark',       
       'home':{'state':'c0','zip':80513}}
print mel
D3 = {}
D3 = dict(name='mel',age=45)
D3 = dict([('name','mel'),('age',44)])
print D3

D4 = dict.fromkeys(['a','b'],0)

print D4

D5 = {k:1 for k in ['a','b']}
print D5

D6 = dict.fromkeys('spam')
print D6

K= mel.values()
K.sort()
print K
print mel.has_key('a')