'''
Author: ShAn_3003
Date: 2024-01-05 16:09:23
LastEditTime: 2024-01-05 21:42:55
LastEditors: ShAn_3003
Description: 这部分是将前后端分离
FilePath: \ForecastSecondHandHouse\web.py
'''

import tornado.web
import lianjia
import analyse
import linearmodel
import recomand

provinces=lianjia.get_provinces()
province_code=None
citys=None
rooms = None
areas = None
price = None
recommand =None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",provinces=provinces)
    def post(self):
        global province_code,citys
        province_code=int(self.get_argument('province_code'))
        citys = lianjia.get_city(index=province_code)
        print(province_code)
        print(citys)
        self.redirect('/craw')
        
        
class SecondHandler(tornado.web.RequestHandler):
    def get(self):
        global citys
        self.render("city.html",citys=citys)

    def post(self):
        city_idx = int(self.get_argument('city_idx'))
        # lianjia.craw_data(city_idx)
        self.redirect('/analyse')

class ThirdHandler(tornado.web.RequestHandler):
    def get(self):
        analyse.analyse()
        self.render('predict.html',rooms = rooms,areas = areas, price=price,recommand=recommand)
    def post(self):
        global price,rooms,areas,recommand
        rooms = int(self.get_argument('Rooms'))
        areas = float(self.get_argument("Areas"))
        price = linearmodel.predict(rooms,areas)
        recommand = recomand.recomand(rooms,areas)
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
