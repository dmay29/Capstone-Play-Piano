'''
Comms signal plan

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


'''