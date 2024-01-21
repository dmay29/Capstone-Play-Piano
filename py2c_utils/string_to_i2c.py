import argparse
from smbus2 import SMBus, i2c_msg

def main():
    parser = argparse.ArgumentParser(prog="py2c_string", description="send a string over i2c")
    parser.add_argument("--addr", help="i2c addr", required=True)
    parser.add_argument("--bus", help="i2c bus", required=True)
    parser.add_argument("--str", help="string to send over i2c", required=True)
    args = parser.parse_args()
    i2c_addr = int(args.addr, 0)
    i2c_bus = int(args.bus)
    msg_str = args.str

    bus = SMBus(i2c_bus)
    msg = i2c_msg.write(i2c_addr, msg_str.encode())
    bus.i2c_rdwr(msg)

if __name__ ==  '__main__':
    main()