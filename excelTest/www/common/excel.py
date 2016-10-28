#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import logging
from www.common.other import Dict
import logging
import os
import json   #为了解决控制台打印list&dict时值前面有 u' 字符的问题。

BASE_DIR = os.path.dirname(__file__)
TestData = BASE_DIR + '/../../testdata/httpapi.xlsx'

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        logging.info(str(e))

#读入到dict字典中
def eData(sheetname=u'Sheet1', file = TestData):
    data = open_excel(file)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    excelData = Dict()
    for rownum in range(1,nrows):
        keys = table.cell(rownum,0).value
        values = table.cell(rownum,1).value   #读取第几列，从0开始。
        excelData[keys] = values.encode('utf-8')
        #excelData[keys] = values
    return excelData

#将指定列读入到list中
def eDataList(sheetname=u'Sheet1', file = TestData,colNum=0):
    data = open_excel(file)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    excelCol = []
    for rownum in range(1,nrows):
        excelCol.append(table.cell(rownum,colNum).value)
    return excelCol

def getValue(sheetname, cellname, file = TestData):
    data = eData(sheetname,file)
    return data[cellname]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    #以dict形式读取  键值对为“0列：1列”
    paraNames = eData('Sheet1')
#    print paraNames.keys()
    '''
    print paraNames['couponUseStartTime']
    print paraNames.couponEntityId
    print len(paraNames)
    '''
#    logging.info(UserA.companyName)
#    print UserA.invoiceHeader
#    print getValue('Sheet1', 'couponEntityId')

    #以list形式读取
    paraNamesList= eDataList('Sheet1')
#    print paraNamesList
#    print paraNamesList[0]
#    print len(paraNamesList)
    paraList = ''
    dataList = ''
    pataValue = ''
    for key in range(0,len(paraNamesList)):
        #print paraNamesList[key]+'=None,',
        paraList+=paraNamesList[key]+'=None,'     #制作入参字符串，
        pataValue += paraNamesList[key]+'= self.UsedDealerCouponInfo.'+paraNamesList[key]+','
        #paraNames[paraNamesList[key]]=paraNamesList[key]
        dataList+="\t\""+paraNamesList[key]+"\": "+paraNamesList[key]+",\n"    #制作data的赋值格式

    #print ''
    #print json.dumps(paraNames)
    print paraList
    print '{\n'+dataList+'}'
    print pataValue