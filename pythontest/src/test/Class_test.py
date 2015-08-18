from mhlib import PATH

class Student(object):
    def __init__(self,name,score):
        self.name = name
        self.__score = score
    def __str__(self):
        return 'Student object(name = %s)' %self.name
    def print_score(self):
        print('%s:%s',self.name,self.__score)
    def get_grade(self):
        if self.__score >90:
            return 'A'
        if self.__score >=60:
            return 'B'
        else:
            return 'C'
        
    def set_score(self,score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')
    def __getattr__(self,attr):
        if attr == 'age':
            return lambda: 25
s = Student("michale",89)
print s
def set_age(self,age):
    self.age = age

from types import MethodType

s.set_age = MethodType(set_age,s)

s.set_age(25)
print s.age

s2 = Student("jadan",90)
#error s2 not bind with set_age
#s2.set_age(15)
#print s2.age
Student.set_age = MethodType(set_age,Student)

s2.set_age(15)
print s2.age



class Screen(object):
    
    def check(self,n):
        if not isinstance(n,int):
            raise TypeError('expect int type')
        if 0 > n:
            raise Exception('expect bigger than 0')
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,width):
        self.check(width)
        self._width = width
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self,height):
        self.check(height)
        self._height = height
    @property
    def resolution(self):
        return self._width * self._height
    
s = Screen()
s.width = 1024
s.height = 768
print(s.resolution)
assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution    



class Fib(object):
    def __init__(self):
        self.a, self.b = 0,1
    def __iter__(self):
        return self
    def next(self):
        self.a , self.b = self.b, self.a+self.b
        if self.a > 1000:
            raise StopIteration()
        return self.a
    def __getitem__(self,n):
        if isinstance(n, int):
            a,b=1,1
            for x in range(n):
                a,b=b,a+b
                return a
        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a,b =1,1
            L = []
            for x in range(stop):
                if x>=start:
                    L.append(a)
                a,b=b,a+b
            return L
  



f = Fib()
print f[10]
print f[0:5]   



class Chain(object):
    def __init__(self,path=''):
        self._path = path 
    def __getattr__(self,attr):
        return Chain('%s%s'  % (self._path,attr))
    def __str__(self):
        return self._path
    def __call__(self,name):
        return Chain('GET %s/:%s'% (self._path,name))
print Chain().users('michael').repp