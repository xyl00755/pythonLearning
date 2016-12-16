#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
from www.common.other import Dict
from xlutils.copy import copy
import logging
from www.common.other import Dict
import logging
import os

BASE_DIR = os.path.dirname(__file__)
TestData = BASE_DIR + '/../../testdata/userdata.xls'
TestDataWS = BASE_DIR + '/../../testdata/userdata_ws.xls'

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        logging.info(str(e))

def eData(sheetname=u'Sheet1', file = TestData):
    data = open_excel(file)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    excelData = Dict()
    for rownum in range(1,nrows):
        keys = table.cell(rownum,0).value
        values = table.cell(rownum,1).value
        if values is not None and values != '':
            if values[0] == '[' and values[-1] == ']':
                excelData[keys] = eval(values)


            elif '{' in values and '}' in values:
                dictData = eval(values.encode('utf-8'))
                dictKeys = []
                dictValues = []
                for (k, v) in dictData.iteritems():
                    dictKeys.append(k)
                    dictValues.append(v)
                excelData[keys] = Dict(dictKeys, dictValues)
            else:
                excelData[keys] = values.encode('utf-8')
        elif values == '':
            excelData[keys] = ''
    return excelData




def wsData(sheetname=u'Sheet1', file = TestDataWS):
    return eData(sheetname, file)

def write_excel(sheetname=u'Sheet1',rowkey=1, rowvalue=1, file = TestDataWS):
    rb = xlrd.open_workbook(file, formatting_info=True)
    table = rb.sheet_by_name(sheetname)
    i = 0
    for sheet in rb.sheets():
        if sheetname == sheet.name:
            wb = copy(rb)
            ws = wb.get_sheet(i)
            nrows = table.nrows
            for rownum in range(1, nrows):
                if table.cell(rownum, 0).value == rowkey:
                    ws.write(rownum, 1, rowvalue)
                    wb.save(file)
                    break
        else:
            i+=1
    return wsData(sheetname)

def getValue(sheetname, cellname, file = 'C:\\Users\\Roy\\PycharmProjects\\dltest\\testdata\\userdata.xls'):
    data = eData(sheetname,file)
    return data[cellname]




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # wsData('TmlShop')
    teststr = wsData('TmlShop').orderCodSeparatSub
    print teststr
    print teststr[0]

    # UserA = eData('TmlShop')
    #print UserA.orderCodWaitDeliver.paymentNo
    # print type(UserA.orderCodWaitDeliver)
    # print UserA.orderCodWaitDeliver
    # print UserA.orderCodWaitDeliver.orderNo
    UserA = wsData('')
    #print UserA.orderCodWaitDeliver.paymentNo
    print UserA
    #UserA_new = write_excel('TmlShop', 'orderOnlineWaitPay', "test")
    # print UserA_new
    # print UserA_new.orderOnlineWaitPay
    # write_excel(sheetname='TmlShop', rowkey='test',rowvalue='1')