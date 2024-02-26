
from smbus2 import i2c_msg, SMBus
from time import sleep


bus = SMBus(1)


def i2c_write(addr, data):
    msg = i2c_msg.write(addr,data)
    bus.i2c_rdwr(msg)
    sleep(.001)

AMP_ADDR = 0x4b

def set_volume(level):
    level = max(0,min(level, 63))
    i2c_write(AMP_ADDR, [level])
    

if __name__ == '__main__':
    while True:
        try:
            level = int(input("Volume: "))
        except:
            continue
        set_volume(level)