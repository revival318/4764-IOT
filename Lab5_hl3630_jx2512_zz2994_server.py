import machine, network, urequests, ujson
from machine import Pin, I2C
import ssd1306
import time
import utime
import math
import socket
import network  
from machine import Pin, I2C, SPI
import ssd1306
import time
import utime
import math

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Columbia University')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

do_connect()
addr = ('160.39.217.174',80)
s = socket.socket()
s.bind(addr)
s.listen(1)
s.settimeout(1)

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
res=''
flag=-1
while (1):
    try:
        (conn,address) = s.accept()
    except OSError:
        print('Nothing')
    else:
        rec = conn.recv(2048).split(b'?')[1]
        res =  bytes.decode(rec)
        res = res[1:len(res)-1]
        print(res)
        if 'on' in res:
            flag = 1
            conn.send(b'HTTP/1.1 200 OK\r\n\r\ndisplay on')
        elif 'off' in res:
            flag = 2
            conn.send(b'HTTP/1.1 200 OK\r\n\r\ndisplay off')
        elif 'time' in res:
            flag = 3
            conn.send(b'HTTP/1.1 200 OK\r\n\r\ndisplay time')
        else:
            flag = 4
            conn.send(b"HTTP/1.1 200 OK\r\n\r\ngot it")
    if flag == 1:
        display.poweron()
        display.text('hello world',20,14,1)
    elif flag == 2:
        display.poweroff()
    elif flag == 3:
        display.text(str(time.gmtime()[3])+' : '+str(time.gmtime()[4])+' : '+str(time.gmtime()[5]),20,20,1)
    else:
        display.text(res,0,14,1)
    display.show()
    display.fill(0)
  
            
        