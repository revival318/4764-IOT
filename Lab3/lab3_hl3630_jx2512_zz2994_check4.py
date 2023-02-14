from machine import Pin, I2C, ADC, PWM
import ssd1306
import time
import utime
import math

# using default address 0x3C
i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
adc = ADC(0) # create ADC object on ADC pin
pwm = PWM(Pin(2))
p0=Pin(0,Pin.IN)
p14=Pin(14,Pin.IN)
p12=Pin(12,Pin.IN)


global switch,A_value,B_value,C_value
switch=0
A_value = p0.value()
B_value = p14.value()
C_value = p12.value()

def callback0(p):
    
    global switch,A_value
    
    active = 0
    while active < 20:
        print(active)
        if p.value() != A_value:
            active += 1
        else:                                               
            active=0
        print(active)
        utime.sleep(0.01)
    if active==20:
        switch += 1
        if switch >2:
            switch=0
        
def callback14(p):

    global B_value
    
    active = 0
    while active < 20:
        if p.value() != B_value:
            active += 1
        else:                                               
            active = 0
        print(active)
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
    
    global C_value
    print("c")
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
            
p0.irq(trigger=Pin.IRQ_FALLING,handler=callback0)
p14.irq(trigger=Pin.IRQ_FALLING,handler=callback14)
p12.irq(trigger=Pin.IRQ_FALLING,handler=callback12)

alarm=[time.gmtime()[3],time.gmtime()[4]-1,0]
localt=[time.gmtime()[3],time.gmtime()[4],time.gmtime()[5]]
start = time.ticks_ms()

while True:
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
 