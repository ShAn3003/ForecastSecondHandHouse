'''
Author: ShAn_3003
Date: 2024-01-05 16:09:23
LastEditTime: 2024-01-06 11:48:27
LastEditors: ShAn_3003
Description: 这部分是将前后端分离
FilePath: \ForecastSecondHandHouse\web.py
'''

import tornado.web
import tornado.websocket
import src.lianjia as lianjia
import src.analyse as analyse
import src.linearmodel as linearmodel
import src.recomand as recomand
import time
import sys
sys.path.append("./src")


"""
1. 改进第一步：将变量和相应的函数塞到类里面
2. 改进第二步：利用if结构重新布局html
3. 改进第三步：修改爬虫部分，爬取更精确有效的数据，加快爬取的速度
"""

class MyWeb(object):
    def __init__(self):
        self.provinces=lianjia.get_provinces()
        self.province_code=None
        self.citys = None
        self.city_idx = None
        self.craw = False
        self.rooms = None
        self.areas = None
        self.price = None
        self.recommand = None

shan = MyWeb()
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",shan=shan)
    def post(self):
        global shan
        shan.province_code=int(self.get_argument('province_code'))
        shan.citys = lianjia.get_city(shan.province_code)
        self.redirect('/')
        

class SecondHandler(tornado.web.RequestHandler):
    def post(self):
        global shan
        shan.city_idx = int(self.get_argument('city_idx'))
        shan.craw = True
        if len(sys.argv) > 1 and sys.argv[1] == 'craw_data':
            lianjia.craw_data(shan.city_idx)
        time.sleep(2)
        shan.craw = False
        self.redirect('/analyse')

class ThirdHandler(tornado.web.RequestHandler):
    def get(self):  
        self.render('predict.html',shan = shan)
        analyse.analyse()

    def post(self):
        global shan
        shan.rooms = int(self.get_argument('Rooms'))
        shan.areas = float(self.get_argument("Areas"))
        shan.price = linearmodel.predict(shan.rooms,shan.areas)
        shan.recommand = recomand.recomand(shan.rooms,shan.areas)
        self.redirect('/analyse')


application = tornado.web.Application(
    [
        (r'/',MainHandler),
        (r'/process',MainHandler),
        (r'/craw',SecondHandler),
        (r'/try',SecondHandler),
        (r'/analyse',ThirdHandler),
    ],template_path='templates'
)

if __name__  == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
