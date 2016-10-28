#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import uuid

class Dict(dict):
    """
    字典对象
    实现一个简单的可以通过属性访问的字典，比如 x.key = value
    """
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def next_id(t=None):
    """
    生成一个唯一id   由 当前时间 + 随机数（由伪随机数得来）拼接得到
    """
    if t is None:
        t = time.time()
    return '%015d%s000' % (int(t * 1000), uuid.uuid4().hex)