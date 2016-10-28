#!/usr/bin/env python
# -*- coding: utf-8 -*-

def list_all_dict(dict_a):
    if isinstance(dict_a,dict) :   #使用isinstance检测数据类型
        keyList =[]
        for x in range(0,len(dict_a)):
            temp_key = dict_a.keys()[x]
            temp_value = dict_a[temp_key]
            keyList.append(temp_key)
            print"\"%s\" : %s" %(temp_key,temp_value)
            list_all_dict(temp_value) #自我调用实现无限遍历
        print keyList



if __name__ == '__main__':
    data=\
        {
            "dealerCouponDto":{
                "dealerCouponName":"lulu酒业送券活动",
                "dealerCouponType":"11",
                "dealerName":"lulu酒业",
                "dealerId":"7d8f02016bc141efb9d4c2a67d4bedff",
                "totalNum":100,
                "totalAmount":10000,
                "effectiveTime":"1474861112",
                "uneffectiveTime":"1474861112",
                "availableChannel":"S012,S014",
                "goodsId":"cac55daa5a0d41bc9e1d1dc6da3962e6",
                "goodsName":"茅台 500ml",
                "areaLimit":"code1,code2",
                "platformLimit":"WEB,APP",
                "createPersonName":"system",
                "createPerson":"7d8f02016bc141efb9d4c2a67d4bedff",
                "dealerCouponImgUrl":"http://www.danlu.com/images/12324234342.jpg",
                "dealerCouponAmounts":[
                    {
                        "couponMinAmt":100,
                        "effectiveAmt":10,
                        "couponPriority":1,
                        "packageAmount":2,
                        "packageAmt":200
                    },
                    {
                        "couponMinAmt":100,
                        "effectiveAmt":10,
                        "couponPriority":1,
                        "packageAmount":2,
                        "packageAmt":200
                    }
                ]
            },
            "activityType":"10",
            "issueWay":0,
            "autoEnable":"1474861112",
            "autoDisable":"1474861112",
            "approvalAutoEnable":1,
            "releaseCompletionDisable":0,
            "limitNum":2,
            "showWay":"0,1,2",
            "getWay":"0,1",
            "createPersonName":"system",
            "createPerson":"7d8f02016bc141efb9d4c2a67d4bedff",
            "notice":"01,02"
        }

    list_all_dict(data)
    #print data.keys()