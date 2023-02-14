from machine import ADC,Pin,PWM
import utime

global switch
switch=1



def callback(p):
    global switch
    
    cur_value = p.value()
    active = 0
    while active < 20:
        if p.value() != cur_value:
            active += 1
        else:                                               
            active = 0
        utime.sleep(0.01)
        
    switch=-switch
    print('interrupt',switch)
    #if switch==1:
    pwm0.duty(0)
    #else:
        #switch=1

adc = ADC(0) # create ADC object on ADC pin
pwm0 = PWM(Pin(0))
p2=Pin(2,Pin.IN)
p2.irq(trigger=Pin.IRQ_FALLING,handler=callback)

while True:
    while switch==1:
        pwm0.freq(adc.read()*10)
        pwm0.duty(adc.read()*5)
        utime.sleep(0.1)