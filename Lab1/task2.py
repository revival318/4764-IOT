from machine import Pin
import utime
builtin_led = Pin(0, Pin.OUT)
antenna_led = Pin(2, Pin.OUT)
builtin_led.value(1) # Built in LED - 1 is off
antenna_led.value(1) # Antenna LED - 0 is on
while True:
    #100ms
    builtin_led.value(1)
    antenna_led.value(0)
    utime.sleep(0.1)
    #200ms
    builtin_led.value(1)
    antenna_led.value(1)
    utime.sleep(0.1)
    #300ms
    builtin_led.value(1)
    antenna_led.value(0)
    utime.sleep(0.1)
    #400ms
    builtin_led.value(1)
    antenna_led.value(1)
    utime.sleep(0.1)
    #500ms
    builtin_led.value(1)
    antenna_led.value(0)
    utime.sleep(0.1)
    #600ms
    builtin_led.value(0)
    antenna_led.value(1)
    utime.sleep(0.1)
    #700ms
    builtin_led.value(0)
    antenna_led.value(0)
    utime.sleep(0.1)
    #800ms
    builtin_led.value(0)
    antenna_led.value(1)
    utime.sleep(0.1)
    #900ms
    builtin_led.value(0)
    antenna_led.value(0)
    utime.sleep(0.1)
    #1000ms
    builtin_led.value(0)
    antenna_led.value(1)
    utime.sleep(0.1)

