#-*- coding: utf-8 -*-
#/usr/bin/env python
import websocket
import json
import logging
import time
from car import *
import sys


try:
    import thread
except ImportError:
    import _thread as thread
import time

live = True
lrang = 80
udang = 80

def on_message(ws, message):
    global lrang
    global udang
    message = json.loads(message)
    print "get message:%s"%message
    if message['target'] == 'wheel':
        pass
        if message['content']['direct'] == 'right':
            right()
        elif message['content']['direct'] == 'left':
            left()
        elif message['content']['direct'] == 'front':
            run()
        elif message['content']['direct'] == 'back':
            back()
        else:
            brake()
    else:
        if message['content']['direct'] == 'right':
            lrang -= 10 
            leftrightservo_appointed_detection(lrang)
        elif message['content']['direct'] == 'left':
            lrang += 10 
            leftrightservo_appointed_detection(lrang)
        elif message['content']['direct'] == 'up':
            udang += 10 
            updownservo_appointed_detection(udang)
        elif message['content']['direct'] == 'down':
            udang -= 10 
            updownservo_appointed_detection(udang)
        elif message['content']['direct'] == 'restoration':
            updownservo_appointed_detection(80)
            leftrightservo_appointed_detection(80)
        else:
            pass
    #print(message)

def on_error(ws, error):
    global live
    print("get_error:",error,type(error))
    logging.error(error)
    if isinstance(error,KeyboardInterrupt):
        print("catch KeyboardInterrupt ")
        live = False
        stop()


def on_close(ws):
    print("closed!")
    logging.error("close connection!")

def on_open(ws):
    #def run(*args):
    #    for i in range(3):
    #        time.sleep(1)
    #        ws.send("Hello %d" % i)
    #    time.sleep(1)
    #    ws.close()
    #    print("thread terminating...")
    #thread.start_new_thread(run, ())
    ws.send(json.dumps({'role':'car','msg_type':'login','name':'EVANGELION','roomid':roomid}))
    pass


if __name__ == "__main__":
    roomid = sys.argv[1]
    print("========================")
    print("roomid:",roomid)
    print("========================")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://www.unaive.com/wss",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    init()
    while True:
        ws.on_open = on_open
        ws.run_forever()
        if not live:
            pwm_ENA.stop()
            pwm_ENB.stop()
            pwm_rled.stop()
            pwm_gled.stop()
            pwm_bled.stop()
            pwm_FrontServo.stop()
            pwm_LeftRightServo.stop()
            pwm_UpDownServo.stop()
            GPIO.cleanup()
            break
        time.sleep(2)
