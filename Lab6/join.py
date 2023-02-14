import ssd1306
import time
import utime
import math
import socket
import network
import machine, network, urequests, ujson
from machine import Pin, I2C, ADC, PWM, SPI


# hardware
def inithardware():
    global switch,A_value,B_value,C_value,cs,hspi,adc,pwm,switch,display
    switch = -1
    i2c = I2C(sda=Pin(4), scl=Pin(5))
    display = ssd1306.SSD1306_I2C(128, 32, i2c)
    adc = ADC(0) # create ADC object on ADC pin
    pwm = PWM(Pin(15))
    p0=Pin(0,Pin.IN)
    p13=Pin(13,Pin.IN)
    p12=Pin(12,Pin.IN)

    A_value = p0.value()
    B_value = p13.value()
    C_value = p12.value()
    
    p0.irq(trigger=Pin.IRQ_FALLING,handler=callback0)
    p13.irq(trigger=Pin.IRQ_FALLING,handler=callback13)
    p12.irq(trigger=Pin.IRQ_FALLING,handler=callback12)
    #hspi
    hspi=machine.SPI(1,baudrate=5000000, polarity=1, phase=1)
    cs = Pin(2, mode=Pin.OUT, value=1)
    cs.value(1)
    time.sleep_ms(50)
    cs.value(0)
    
    write_value(b'\x31', b'\x0C')
    write_value(b'\x2c', b'\x0a')
    write_value(b'\x2e', b'\x00')
    write_value(b'\x38', b'\x00')
    write_value(b'\x2d', b'\x08')

#interrupts:0,13,12,14
def callback0(p):
    
    global switch,A_value
    
    active = 0
    while active < 20:
        if p.value() != A_value:
            active += 1
        else:                                               
            active=0
        utime.sleep(0.01)
    if active==20:
        switch += 1
        if switch >2:
            switch=0
        
def callback13(p):

    global B_value,switch,alarm,localt
    
    active = 0
    while active < 20:
        if p.value() != B_value:
            active += 1
        else:                                               
            active = 0
        utime.sleep(0.01)
    if active==20:
        if switch ==1:
            alarm[1]+=1
            if alarm[1]==60:
                alarm[0]+=1
                alarm[1]=0
            if alarm[0]==24:
                alarm[0]=0
        if switch==2:
            localt[1]+=1
            if localt[1]==60:
                localt[0]+=1
                localt[1]=0
            if localt[0]==24:
                localt[0]=0
            
def callback12(p):
    
    global C_value,switch
    active = 0
    while active < 20:
        if p.value() != C_value:
            active += 1
        else:                                               
            active = 0
        print(active)
        utime.sleep(0.01)
    if active==20:
        if switch ==1:
            alarm[0]+=1
            if alarm[0]==24:
                alarm[0]=0
        if switch==2:
            localt[0]+=1
            if localt[0]==24:
                localt[0]=0

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Columbia University')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    return wlan.ifconfig()[0]
    
def socket_init(addr):
    addr = (addr,80)
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    s.settimeout(1)
    return s
    
#hspi func
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

def time_display():
    global switch,alarm,localt
    alarm=[time.gmtime()[3],time.gmtime()[4]-1,0]
    localt=[time.gmtime()[3],time.gmtime()[4],time.gmtime()[5]]
    #start = time.ticks_ms()
    if switch==0:
        if time.gmtime()[3:6]==tuple(alarm):
           pwm.freq(1000)
           pwm.duty(50)
        if time.gmtime()[5]>=  5:
           pwm.freq(1)
           pwm.duty(0)
        display.text(str(time.gmtime()[0])+'/'+str(time.gmtime()[1])+'/'+str(time.gmtime()[2]), 30, 10, 1)
        display.text(str(time.gmtime()[3])+' : '+str(time.gmtime()[4])+' : '+str(time.gmtime()[5]), 20, 20, 1)
        display.contrast(adc.read()+10)
        display.show()
        display.fill(0)
    if switch ==1:
        display.text('Setting alarm',20, 5, 2)
        display.text(str(alarm[0])+' : '+str(alarm[1]),40, 15, 1)
        display.show()
        display.fill(0)
    if switch ==2:
        add=time.ticks_diff(time.ticks_ms(), start)/1000
        total_time=(add+localt[0]*3600+localt[1]*60+localt[2])%(24*3600)
        display.text('Local time',30, 5, 2)
        display.text(str(int(total_time/3600))+' : '+str(int(total_time%3600/60))+' : '+str(int(total_time%60)),20, 15, 1)
        display.show()
        display.fill(0)

def twitters():
    url = "http://ip-api.com/json"
    twitter_key ="VA5BD5C96J0YJHTQ"
    twitter_url ="https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key="+twitter_key+"&status="

    header = {"Content-Type": "application/json"}
    request = {"considerIp": "true"}
    res = urequests.post(url, headers = header,  data = ujson.dumps(request))
    latitude = ujson.loads(res.content)["lat"]
    longitude = ujson.loads(res.content)["lon"]


    weather_key = "6f96e61d87eeaeb132cd6ec84743f781"
    weather_url = "https://api.openweathermap.org/data/2.5/weather?lat="+str(latitude)+"&lon="+str(longitude)+"&appid="+weather_key
    weather_res = urequests.post(weather_url)
    weather = ujson.loads(weather_res.content)
    temp = weather['main']['temp']
    weatherdisplay= weather['weather'][0]['description']


    status = "the_temp_is"+str(temp)+"K"
    twitter_url += status
    twitter_res = urequests.post(twitter_url)
    twitter_posted = ujson.loads(twitter_res.content)

    display.fill(0)
    display.text("temp:"+str(temp)+"k", 0,0,1)
    display.text(str(weatherdisplay),0,10,1)
    display.show()
    print("done")

def speech_reg(s):
    res=''
    flag=-1
    try:
        (conn,address) = s.accept()
    except OSError:
        pass
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
    return res


def light_display():
    global adc,pwm
    pwm.freq(adc.read()*10)
    pwm.duty(adc.read()*5)
    utime.sleep(0.1)
            
def gesture_rec():
    url = "http://54.227.89.15:5000/"
    cursor = 0
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

inithardware()
addr = do_connect()
s = socket_init(addr)

mode = ''




while True:
    res = speech_reg(s)
    if 'light' in res:
        mode = 'light'
    if 'time' in res:
        mode = 'time'
    if 'message' in res:
        mode = 'twitter'
    if 'gesture' in res:
        mode = 'gesture'
    if mode == 'light':
        print('light mode')
        light_display()
    if mode == 'time':
        print('time mode')
        time_display()
    if mode == 'twitter':
        twitters()
        mode = 'time'
    if mode == 'gesture':
        print('gesture mode')
        gesture_rec()

        
