import machine, network, urequests, ujson
from machine import Pin, I2C, SPI
import ssd1306
import time
import utime
import math
import socket
import network


# using default address 0x3C
i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
hspi=machine.SPI(1,baudrate=5000000, polarity=1, phase=1)
p14=Pin(14,Pin.IN)
cs = Pin(2, mode=Pin.OUT, value=1)
cs.value(1)
time.sleep_ms(50)
cs.value(0)

global switch,p_value
switch = -1
p_value = p14.value() 
def callback14(p):
    
    global switch,p_value
    
    active = 0
    while active < 20:
        if p.value() != p_value:
            active += 1
        else:                                               
            active=0
        utime.sleep(0.01)
    if active==20:
        switch = -switch
 
def write_value(Hex,Reset_value):
    global cs,hspi
    cs.value(0)
    hspi.write(Hex)
    hspi.write(Reset_value)
    cs.value(1)

def read_value(Hex):
    global cs,hspi
    cs.value(0)
    buffer=bytearray(2)
    code=1<<7
    answer=code|Hex
    hspi.readinto(buffer, answer)
    cs.value(1)
    return buffer

def trans_to_g(x):
    if x < 32768:
        y = x/16384
    else:
        y = -(65536 - x)/16384
    return y

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
url = "http://54.227.89.15:5000/"


#initial hex_value
write_value(b'\x31', b'\x0C')
write_value(b'\x2c', b'\x0a')
write_value(b'\x2e', b'\x00')
write_value(b'\x38', b'\x00')
write_value(b'\x2d', b'\x08')
p14.irq(trigger=Pin.IRQ_FALLING,handler=callback14)

cursor = 0
display.poweron()
while True:
    if switch == 1:
        for i in range(8):
            data = {}
            header = {"Content-Type": "application/json"}
            print('READY')
            for i in range(5):
                print(5-i)
                utime.sleep(1)
            print('GO')

            for k in range(20):
                x0 = read_value(0x32) 
                x1 = read_value(0x33)   
                y0 = read_value(0x34)     
                y1 = read_value(0x35) 
                x_value = x1[1] << 8 | x0[1]
                y_value = y1[1] << 8 | y0[1]
                data[str(k+1)] = [x_value,y_value]
                utime.sleep(0.2)
            response = urequests.get(url, headers = header,  data = ujson.dumps(data))
            result_str = response.content.decode('utf-8')
            result_json = ujson.loads(result_str)
            letter = result_json["res"]
            print('letter %s' % letter)
            response.close()
            display.text(letter,cursor,20,1)
            display.show()
            cursor = cursor + 10
