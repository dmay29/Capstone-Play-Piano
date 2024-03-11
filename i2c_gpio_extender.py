
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x27)

pin = mcp.get_pin(0)
pin.direction = digitalio.Direction.OUTPUT
    

if __name__ == '__main__':
    while True:
        try:
            val = bool(int(input("Value: ")))
        except:
            continue
        pin.value = val