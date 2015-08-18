import os
from re import search

def search(s,dir = '.'):
    __file = []
    __path = ['.']
    for i in __path:
#        os.chdir(i)
        for x in os.listdir(i):
            if os.path.isdir(os.path.join(i,x)):
                __path.append(os.path.join(i,x))
            else :
                if s in x:
                    x = os.path.join(i,x)
                    if os.path.isfile(x):
                       __file.append(x)
                
                
    return __file
            
   
ret = []           
ret = search('ile')   
print ret

