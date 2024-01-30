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