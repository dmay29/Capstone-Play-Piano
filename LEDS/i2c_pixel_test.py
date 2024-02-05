import smbus2
from smbus2 import i2c_msg
from time import sleep

i2c_addr = 0x27

bus = smbus2.SMBus(1)
white = [255, 255, 255]
off = [0,0,0]
black = off
red = [255,0,0]
orange = [255,100,0]
yellow = [255,255,0]
green = [0,255,0]
teal = [0,255,255]
blue = [0,0,255]
purple = [100, 0, 255]
magenta = [255, 0, 255]

def i2c_write(addr, data):
    msg = i2c_msg.write(addr,data)
    bus.i2c_rdwr(msg)
    sleep(.001)
    
def write_one_led(index: int, color: list[int, int, int]):
    i2c_write(i2c_addr,[index] + color)
    
def write_many_leds(led_array:list[list[int,int,int]], start:int = 0):
    msg_list = [start]
    for led in led_array:
        msg_list += led
    i2c_write(i2c_addr, msg_list)

def dim(color, factor):
    return [min(int(i*factor),255) for i in color]

color_list = [dim(red, .05), dim(red,.1), red, dim(red,.1),dim(red,.05),off,off,off]*6

while(1):
    write_many_leds(color_list)
    color_list = [color_list[-1]]+color_list[0:-1]
    sleep(.5)
