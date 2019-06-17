# -*- coding: utf-8 -*-
#/usr/bin/env python
import tornado.websocket
import json
import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
import ssl


from tornado.options import define, options
define("port", default=8787, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/wss", WSSHandler),
        ]
        settings = dict(
            debug=True,
            #cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ssl_options=ssl_ctx
            #xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)

class WSSHandler(tornado.websocket.WebSocketHandler):
    controler = {}
    cars = {}
    audience = {}

    def prepare(self):
        logging.info("connected!")
        self.role = ''
        self.user_name = ''
        self.status = ''
        self.roomid = ''

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        pass

    def on_close(self):
        logging.warning("[%s] close connection!"%self.user_name)

    def login(self,data):
        if data['role'] == 'car':
            WSSHandler.cars[data['name']] = self
            self.role = 'car'
            self.roomid = data['roomid']
            logging.info("[%s] car login success"%data['name'])
        elif data['role'] == 'controler':
            WSSHandler.controler[data['name']] = self
            self.role = 'controler'
            logging.info("[%s] controler login success"%data['name'])
            car_list = [{'name':k,'roomid':v.roomid} for k,v in WSSHandler.cars.items()]
            car_list = {'msg_type':'car_list','data':car_list}
            print "car_list:",car_list
            self.write_message(json.dumps(car_list))
        else:
            WSSHandler.audience[data['name']] = self
            self.role = 'audience'
        self.user_name = data['name']

    def command(self,data):
        car = WSSHandler.cars.get(data['car_name'])
        if car:
            logging.info("push message to %s :%s"%(data['car_name'],data))
            car.write_message(json.dumps(data))

    def parse_data(self,data):
        if data['msg_type'] == 'login':
            self.login(data)
        elif data['msg_type'] == 'command':
            if self.role == 'controler':
                self.command(data)

    def on_message(self, message):
        logging.info("recevie message:%s"%message)
        data = json.loads(message)
        logging.info("got message %r", data)
        self.parse_data(data)

    def check_origin(self, origin):
        return True


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

