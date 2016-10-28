# !/usr/bin/python
# coding:utf-8

def func(x,*args):
    print x
    result =x
    print args
    for i in args:
        result+=i
    return result
# print func(1,2,3)

def add(x,y):
    return x+y

bars=(2,3)
# print add(*bars)


def book(author,bookname):
    print "%s wrote %s" % (author,bookname)

bars2={'bookname':"Python",'author':'Kivi'}
# book(**bars2)


def foo(x=None,y=2,*targs,**dargs):
    print "x:",x
    print "y:",y
    print "*targs:",targs
    print '**dargs:',dargs

# foo("1x")
# foo("1x","2y")
# foo(targs=('31','32'))   #*targs: () ，**dargs: {'targs': ('31', '32')}   由于有等于，识别为**dargs参数
# foo(1,2,3,4,5,6,d1='d1',d2='d2') #依次赋给x,y后，多的赋给*targs，有等于的识别为**dargs
# foo(('31','32'),d1='d1',d2='d2') #x: ('31', '32')，*targs: ()，**dargs:  {'d2': 'd2', 'd1': 'd1'}  第一个元组作为x，后面有等于的识别为**dargs参数


#列表生成器
numbers=range(10)
# print [x+3 for x in numbers]

lam =lambda x,y :'x+y='+str(x+y)
n2=[]
for i in numbers:
    n2.append(lam(i,i))

#更简洁的方法：列表生成器  [返回的运算式 循环体 （条件）]
n3=[lam(i,i) for i in range(10)]
n4=[lam(i,i) for i in range(10) if i%2==0]   #在0~10的整数列表中依次取（符合If条件的）值，调用lam函数，返回处理结果
# print n2,'\n',n3,'\n',n4

L = ['Hello', 'World', 18, 'Apple', None]
print L,'\n',[s.lower() for s in L if isinstance(s,str)]
print [s if not isinstance(s,str) else s.lower() for s in L]  #高手答案
print [s*2 for s in L if isinstance(s,int)]