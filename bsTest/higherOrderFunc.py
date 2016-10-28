# !/usr/bin/python
# coding:utf-8
from functools import reduce

#高阶函数：
def add(x,y,f):
    return f(x)+f(y)

# print add(-1,2,abs)  #abs为内建函数，求绝对值


#map:将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回。
def f1(x):
    return x*x
# print map(f1,range(10))
# print list(map(f1,range(10)))
# print map(str,range(10))

#reduce:reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
#reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
def add2(x,y):
    return x+y

# print reduce(add2,range(1,4))  #(1+2)+3

def f3(x,y):
    return x*10+y
# print reduce(f3,range(1,10,2)) #13579


#将字符串转换为整数，相当于int
def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))

# print str2int('26830')



#1.利用map()函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。  自己做出来了哟666
def firstUpper(s):
    sLst=[c.lower() for c in s]
    sLst[0]=sLst[0].upper()
    return ''.join(sLst)
# print firstUpper('ssGH2s')

L1 = ['adam', 'LISA', 'barT']
# print list(map(firstUpper, L1))




# 2.Python提供的sum()函数可以接受一个list并求和，请编写一个prod()函数，可以接受一个list并利用reduce()求积：
def prod(paraList):
    lam=lambda x,y:x*y
    return reduce(lam,paraList)
# print prod(range(1,7,2))  #range取前不取后，所以此处为1*3*5的积



# 3.利用map和reduce编写一个str2float函数，把字符串'123.456'转换成浮点数123.456：
#str2listx为自行作答，不符合题目但满足需求：
def str2floatx(s):
    s2int=map(int,s.split('.'))
    return s2int[0]+s2int[1]*(0.1**len(str(s2int[1])))

# print str2floatx('13.45678')
#参考答案：
def str2float(s):
    def fn(x,y):
        return x*10+y
    n=s.index('.')
    s1=list(map(int,[x for x in s[:n]]))  #0~n-1
    s2=list(map(int,[x for x in s[n+1:]]))   #n+1~末尾
    #return reduce(fn, s1) + reduce(fn, s2) / 10 ** len(s2)  #2.x中用整数除以整数会只取整数部分，最好用乘法
    return reduce(fn,s1)+reduce(fn,s2)*0.1**len(s2)
# print('\'123.4567\'=',str2float('123.45679'))


print float('456')/1000