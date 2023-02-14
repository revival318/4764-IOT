from machine import Pin
import utime
builtin_led = Pin(0, Pin.OUT)
builtin_led.value(1) # Built in LED - 1 is off
#S
for i in range(3):
    builtin_led.value(0)
    utime.sleep(0.5)
    builtin_led.value(1)
    utime.sleep(1)
#O
for i in range(3):
    builtin_led.value(0)
    utime.sleep(1)
    builtin_led.value(1)
    utime.sleep(1)
#S
for i in range(3):
    builtin_led.value(0)
    utime.sleep(0.5)
    builtin_led.value(1)
    utime.sleep(1)