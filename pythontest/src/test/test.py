#-*- coding: UTF-8 -*-
import sys
import math


zhong = '中文'
print zhong
a = 10/4
line = '%s,eggs,and %s' %('spam','SPAM')
#print line
#print dir(line)
M = [[1,2,3],
     [4,5,6],
     [7,8,9]
     ]

#print M
G = (sum(row) for row in M)
#print next(G)  
#print next(G)
#print int(0.1+0.1+0.1-0.3)

x = 42
y = 42   
#print x is y
#print sys.getrefcount(42)
#z = 42
#print sys.getrefcount(42)
L1 = [2,3,4]
L2 = L1[:]
L1[0]=32
# print L1
# print L2

#p200 String

mantra = """alwayse look
on the burght 
side of life"""
#print mantra

S = '5'
# print S
S = chr(ord(S)+1)
print S

B = "1101"
I = 0
while B !='':
    I = I * 2 +(ord(B[0])-ord('0'))
    B = B[1:]
# print I

# print int('1101',2)


S = 'splot'
S = S.replace('pl', 'pamal')
# print S
# print sys.getrefcount('asdgtasdf')


line = 'aaa bbb ccc'
cols = line.split()
# print cols

line = 'aaa,bbb, ccc'
cols = line.split(',')
# print cols

line = 'the knights who say ni!'
line.rstrip()
# print line

dic1 = {'food':'spam', 'age':40}
# print "%(age)d  %(food)s" %dic1

template = '{0},{1} and {2}'.format('spam', 'ham','egg')

# print template

test = 'my {1[spam]} runs {0.platform}'.format(sys,{'spam':"laptop"})
print test

T = ('a','b','c','d')
T = list(T)
T[0]=1
print T

a = dict()
b = dict()
dskey = "test"
b[dskey] = a
a[dskey] = 5
#print b
n1 = 100
print hex(n1)
def quadratic(a,b,c):
    if a==0:
        if b==0:
            if c==0:
                return("always euqal")
                return
            elif not c==0:
                return("always not equal")
                
        elif not b==0:
            x=-c/b
            return "x=%f" %(x)
           
    else :
        delta = b*b-4*a*c
        if delta<0:
            print("haave no euqal")
            return
        elif delta>=0:
            x1=(-b+math.sqrt(delta)/(2*a))
            x2=(-b-math.sqrt(delta)/(2*a))
            return "x1=%f  x2=%f" %(x1, x2)
#print(quadratic(2, 3, 1))
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum +=n*n
    return sum
print calc(*[1,2,3])

global i
i=1
def move(n,fro,to):   
    global i 
    print ("%d:num%d,%s->%s")%(i,n,fro,to)
    i = i+1
   
def hanoi(n,fro,dep,to):
    if(n==1):
        move(1,fro,to)
    else:
        hanoi(n-1, fro, to, dep)
        move(n,fro,to)
        hanoi(n-1, dep, fro, to)    
#hanoi(3,'a','b','c')
 
L = [x*x for x in range(10)]     
g = (x*x for x in range(10))   
#print next(g)

#
def triangle():
    L=[1]
    yield L
    while True:
        if len(L)!=1:
            L = [L[i]+L[i+1] for i in range(0,len(L)-1)]
            L.insert(0, 1)
        L.append(1)
        yield L  

n=0
for t in triangle():
#    print t     
    n = n+1
    if n==10:
        break


def add(x,y,f):
    return f(x)+f(y)
print add(-4,5,abs)

def add_reduce(x,y):
    return x+y

print list(map(str,[1,2,3,4,5]))

#reduce   reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
print reduce(add_reduce,[1,2,3,4,5])

def fn(x,y):
    return x*10+y

print reduce(fn,[1,2,3,4,5])

def char2num(s):
    return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]

def str2float(s):
    sl=s.split('.')
    strint = reduce(lambda x,y:x*10+y,map(char2num,sl[0]))
    strfloat = reduce(lambda x,y:x*10+y,map(char2num,sl[1]))*0.1**len(sl[1]) 
    return   strint+strfloat    
print str2float('123.4')

def normalize(name):
    return name.lower()    
L1 = ['adam', 'LISA', 'barT']
def captilize(name):    
    return name[0].upper()+name[1:].lower()
    
L2 = map(captilize, L1)
print(L2)

testList={"1":1,"3":30}
#for k,v in testList.items():
#    print v

strtest = "12345"
print strtest[::-1]


def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()
print f1()

L = [("Bob",75),('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(t):
    return t[0]
L2 = sorted(L, key=by_name)
print(L2)
def by_score(t):
    return t[1]
L2 = sorted(L, key=by_score)
print(L2)

