import board
import neopixel
import time
from matplotlib import pyplot as plt
import smbus2
from smbus2 import i2c_msg

bus = smbus2.SMBus(1)

def time_fill(pixels):
    start_time = time.time()
    pixels.fill((255,255,255))
    end_time = time.time()
    return end_time - start_time

def time_i2c(msg):
    start_time = time.time()
    bus.i2c_rdwr(msg)
    end_time = time.time()
    return end_time - start_time
   
   
count = []
neo_times = []
i2c_times = []
for i in range(0, 601, 100):
    print(i)
    count.append(i)
    with neopixel.NeoPixel(board.D18, i) as pixels:
        neo_times.append(time_fill(pixels))
    
    msg = i2c_msg.write(0x27,[0xAA]*i)
    i2c_times.append(time_i2c(msg))
    
    
    
        
plt.plot(count, neo_times, i2c_times)
plt.show()