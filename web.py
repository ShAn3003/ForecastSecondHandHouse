'''
Author: ShAn_3003
Date: 2024-01-05 16:09:23
LastEditTime: 2024-01-05 17:40:13
LastEditors: ShAn_3003
Description: 这部分是将前后端分离
FilePath: \ForecastSecondHandHouse\web.py
'''

import tornado.web
import lianjia

provinces=lianjia.get_provinces()
province_code=None
citys=None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",provinces=provinces)
    def post(self):
        global province_code,citys
        province_code=int(self.get_argument('province_code'))
        citys = lianjia.get_city(index=province_code)
        self.redirect('/craw')
        print(province_code)
        print(citys)
        
class SecondHandler(tornado.web.RequestHandler):
    def get(self):
        global citys
        self.render("city.html",citys=citys)

    def post(self):
        city_idx = int(self.get_argument('city_idx'))
        lianjia.craw_data(city_idx)
        self.redirect('/craw')

application = tornado.web.Application(
    [
        (r'/',MainHandler),
        (r'/process',MainHandler),
        (r'/craw',SecondHandler),
        (r'/try',SecondHandler)
    ],template_path='templates'
)

if __name__  == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
