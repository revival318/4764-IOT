from machine import Pin, I2C, SPI
import ssd1306
import time
import utime
import math

# using default address 0x3C
i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
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

def displaycontrol_y(z,y):
     i=48
     if (y>60000 and z!=0):
      while (i<128 and i>=0):
        i+=z
        display.text('abds',i,10,1)
        display.show()
        display.fill(0)
     elif (y>45000 and y<60000 and z!=0):
      while (i<128 and i>=0):
        i+=z
        display.text('abds',i,5,1)
        display.show()
        display.fill(0)         
     elif (y>=0 and y<1000 and z!=0):
      while (i<128 and i>=0):
        i+=z
        display.text('abds',i,15,1)
        display.show()
        display.fill(0)   
     elif (y>=1000 and y<10000 and z!=0):
       while (i<128 and i>=0):
        i+=z
        display.text('abds',i,20,1)
        display.show()
        display.fill(0)
     elif (y>=10000 and y<20000 and z!=0):
       while (i<128 and i>=0):
        i+=z
        display.text('abds',i,25,1)
        display.show()
        display.fill(0)
     elif (z==0):
        display.text('abds',48,15,1)
        display.show()
        display.fill(0)
     else:
         i=58

def displaycontrol_x(x):
    if (x<1500 or x>63000):
        displaycontrol_y(0,y_value)
    elif (x>58000 and x<=63000):
        displaycontrol_y(3,y_value)
    elif (x>45000 and x<=58000):
        displaycontrol_y(8,y_value)
    elif (x>1500 and x<=5000):
        displaycontrol_y(-3,y_value)
    elif (x>=5000 and x<20000):
        displaycontrol_y(-8,y_value)
    else:
        print('out of range')
                  
hspi=machine.SPI(1,baudrate=5000000, polarity=1, phase=1)
#k=Pin(14),mosi=Pin(13),miso=Pin(14)
cs = Pin(2, mode=Pin.OUT, value=1)
cs.value(1)
time.sleep_ms(50)
cs.value(0)
#initial hex_value
write_value(b'\x31', b'\x0C')
write_value(b'\x2c', b'\x0a')
write_value(b'\x2e', b'\x00')
write_value(b'\x38', b'\x00')
write_value(b'\x2d', b'\x08')

i=0
while True:
   x0 = read_value(0x32) 
   x1 = read_value(0x33)   
   y0 = read_value(0x34)     
   y1 = read_value(0x35) 
   x_value = x1[1] << 8 | x0[1]
   y_value = y1[1] << 8 | y0[1]  
   print(x_value,y_value)
   displaycontrol_x(x_value)
   
  
       
       
   


  
#display.line(0, 0, 128,0, 1)
#display.fill_rect(2, 2, 128, 32, 1)
