# !/usr/bin/python
# coding:utf-8

def func(x,*args):
    print x
    result =x
    print args
    for i in args:
        result+=i
    return result


print func(1,2,3)