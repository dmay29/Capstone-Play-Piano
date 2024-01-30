'''
Comms signal plan
-------------------------------------------------------------

Composer Mode - PI initiates a strip to start counting down

Opcode = 0x0

Byte Makeup (bytes sorted in received order)

|--------------------------|-----------------|
|       Data Byte 0        |   Data Byte 1   |
|--------------------------|-----------------|
| Bits 0-3 |    Bits 4-7   |    Bits 0-7     |
|--------------------------|-----------------|
|  Opcode  | First 4 Notes |  Other 8 Notes  |
|--------------------------|-----------------|

Ex.
Data bytes: 0b00000100, 0b00001000

Would initiate a waterfall on keys 2 and 9

--------------------------------------------------------------
Individual LED Control - PI sets every LED individually, one byte per pixel, starting at pixel n

Opcode = 0b1xxx

Byte Makeup (bytes sorted in received order)

|---------------------------|--------------------------------|
|       Data Byte 0         |        Data Byte 1 -> n        |
|---------------------------|--------------------------------|
|  Bit 0  |     Bits 1-7    | Bits 0-2 | Bits 3-4 | Bits 5-7 |
|---------------------------|--------------------------------|
|    1    | First LED index |    Red   |   Green  |   Blue   |
|---------------------------|--------------------------------|

Ex.
Data bytes: 0b10000000, 0b11100000, 0b00011000, 0b00000111,

Would set the first 3 pixels to be red, green, blue


'''

import smbus2
from smbus2 import i2c_msg
from time import sleep

bus = smbus2.SMBus(1)
I2C_ADDR = 0x27

'''
Write a message over i2c

- addr(int): i2c address to send to
- data(list[byte]): list of 8 bit data to send

'''
def i2c_write(addr, data):
    msg = i2c_msg.write(addr,data)
    bus.i2c_rdwr(msg)
    sleep(.001)

'''
Write a compose message over i2c

- addr(int): i2c address to send to
- notes(12 bit int): 12 bit number, one bit per note in octave

'''
def compose(addr, notes):
    data = [notes >> 8, notes & 0xff]
    i2c_write(addr, data)

def main():
    compose(I2C_ADDR, 0b100000000000)
    compose(I2C_ADDR, 0b000000010000)
    compose(I2C_ADDR, 0b000010000000)
    compose(I2C_ADDR, 0b000000000010)
    compose(I2C_ADDR, 0b001000000000)
    compose(I2C_ADDR, 0b000000000001)
    compose(I2C_ADDR, 0b000000000000)
    compose(I2C_ADDR, 0b000000000000)
    compose(I2C_ADDR, 0b000000000000)
    compose(I2C_ADDR, 0b000000000000)
    compose(I2C_ADDR, 0b000000000000)
    compose(I2C_ADDR, 0b000000000000)