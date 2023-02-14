import machine, network, urequests, ujson
from machine import Pin, I2C
import ssd1306
import time
import utime
import math

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('bruceX', '19991104')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

do_connect()
i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
url = "http://ip-api.com/json"
header = {"Content-Type": "application/json"}
request = {"considerIp": "true"}
res = urequests.post(url, headers = header,  data = ujson.dumps(request))
latitude = ujson.loads(res.content)["lat"]
longitude = ujson.loads(res.content)["lon"]

print(latitude)
print(longitude)

display.fill(0)
display.text("lat:"+str(latitude), 0, 10)
display.text("lon:"+str(longitude), 0, 20)
display.show()

