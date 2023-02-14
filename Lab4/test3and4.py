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
twitter_key ="VA5BD5C96J0YJHTQ"
twitter_url ="https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key="+twitter_key+"&status="

header = {"Content-Type": "application/json"}
request = {"considerIp": "true"}
res = urequests.post(url, headers = header,  data = ujson.dumps(request))
latitude = ujson.loads(res.content)["lat"]
longitude = ujson.loads(res.content)["lon"]
print(latitude)
print(longitude)

weather_key = "6f96e61d87eeaeb132cd6ec84743f781"
weather_url = "https://api.openweathermap.org/data/2.5/weather?lat="+str(latitude)+"&lon="+str(longitude)+"&appid="+weather_key
weather_res = urequests.post(weather_url)
weather = ujson.loads(weather_res.content)
print(weather)
temp = weather['main']['temp']
weatherdisplay= weather['weather'][0]['description']
print(temp)
print(weatherdisplay)

status = "the_temp_is"+str(temp)+"K"
print(status)
twitter_url += status
print(twitter_url)
twitter_res = urequests.post(twitter_url)
print(twitter_res)
twitter_posted = ujson.loads(twitter_res.content)
print(twitter_posted)

display.fill(0)
display.text("temp:"+str(temp)+"k", 0,0,1)
display.text(str(weatherdisplay),0,10,1)
display.show()
print("done")
