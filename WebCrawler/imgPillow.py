# -*- coding:utf-8 -*-
from PIL import Image,ImageDraw,ImageFont,ImageGrab
# from pytesser import *



# https://my.oschina.net/jhao104/blog/647326?fromerr=xJxwPW5X
# im = Image.open('1.jpg')
# # im.show()
# imgry = im.convert('L')
# # imgry.show()

#二值化图象的时候把大于某个临界灰度值的像素灰度设为灰度极大值，把小于这个值的像素灰度设为灰度极小值
# 固定阈值：
# threshold = 100
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# out = imgry.point(table, '1')
# out.show()


# 写入文字，生成图片
# text = u"my test 123"
# im = Image.new("RGBA",(640,480),(255, 255, 255))
# dr = ImageDraw.Draw(im)
# # font = ImageFont.truetype(os.path.join("fontsmmsyh.ttf"), 14)
# font = ImageFont.truetype("arial.ttf", 14)
# dr.text((10, 5), text, font=font, fill="#000000")
#
# im.show()
# im.save("t.png")


# screen shot截屏生成图片
#im = ImageGrab.grab()这行代码实现截图功能，可以带参数，指定要截取图片的坐标位置，不带参数默认全屏截图
im = ImageGrab.grab()
# im.save(addr,'jpeg')是保存截取的图片，第一个参数是保存路径，第二个参数是图片格式
im.save('2.jpeg')
