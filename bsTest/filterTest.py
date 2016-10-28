# !/usr/bin/python
# coding:utf-8

'''filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。'''


def isOdd(n):
    return n%2==1
# print list(filter(isOdd,range(0,11)))

def notEmpty(l):
    # print l and l.strip()
    return l and l.strip()
# print list(filter(notEmpty,['A', '', 'B', None, 'C', '  ']))



# 用filter求素数,计算素数的一个方法是埃氏筛法
# 先构造一个从3开始的奇数序列
def _odd_iter():
    n=1
    while True:
        n=n+2
        yield n #???
# 定义一个筛选函数
def _not_divisible(n):
    return lambda x: x % n > 1
# 定义一个生成器，不断返回下一个素数：
def primes():
    yield 2
    it = _odd_iter()
    while True:
        n=next(it)
        yield n
        it=filter(_not_divisible(n),it)

for n in primes():
    if n<10:
        print n
    else:
        break
