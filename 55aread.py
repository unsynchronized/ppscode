#!/usr/bin/env python

import sys
import serial
import time

def doescape(data):
    return "".join(["%02x" % x for x in data])

def serreadsome(ser):
    outdata = serread(ser, 1)
    while True:
        data = ser.read(1)
        if len(data) == 0:
            return outdata
        outdata = outdata + data

def serreadany(ser):
    outdata = b''
    while True:
        data = ser.read(1)
        if len(data) == 0:
            return outdata
        outdata = outdata + data

def loopwrite(ser, buf):
    sv = ser.timeout
    ser.timeout = 0.05
    for b in buf:
        ser.write(bytes([b]))
        d = serread(ser, 1)
        if len(d) != 1:
            raise Exception("invalid length")
        if d[0] != b:
            raise Exception(f'expected byte 0x{"%02x" % b}, got 0x{"%02x" % d[0]}')
    ser.timeout = sv
            


def serread(ser, nbytes):
    outdata = b''
    while nbytes > 0:
        data = ser.read(1)
        if data:
            outdata = outdata + data
            nbytes = nbytes - 1
    return outdata


# Send 0xAA (with intervals of ~165ms) until we get an 0x60 response.
def get_attention(ser):
    print("sending 0xaa")
    ser.timeout = 0.025
    d = b''
    while True:
        ser.write(b'\xaa')
        d = ser.read(1)
        if d[0] != 0xaa:
            raise Exception(f'expected byte 0xaa, got 0x{"%02x" % d[0]}')
        d = ser.read(1)
        if len(d) > 0:
            break
        time.sleep(0.140)  # ~165ms total delta
    print("looking for 0x60: " + doescape(d))
    if d[0] != 0x60:
        raise Exception(f'expected byte 0x60, got 0x{"%02x" % d[0]}')



if __name__ == '__main__':
    devname = sys.argv[1]

    sys.stderr.write("opening device: " + devname + "\n")
    ser = serial.Serial()
    ser.port = devname
    ser.baudrate = 9600
    ser.parity = serial.PARITY_NONE
    ser.bytesize = serial.EIGHTBITS
    ser.rtscts = False
    ser.xonxoff = False
    ser.timeout = 5
    ser.open()
    sys.stderr.write("open\n")

#    loopwrite(ser, b'\x01\x01\x0d\x00\x00\x00\x03\x00')
#    d = ser.read(1)
#    print(doescape(d))
#
#    get_attention(ser)
#    loopwrite(ser, b'\x46\x01\x0d\x00\x00\x00\x03\x00')

    ser.write(b'\x00')
    ser.timeout = 0.5
    d = serreadany(ser)
    print(doescape(d))
    ser.write(b'\x01\x00\x01\x00\x01\x00\xa1\x9b\x3f\x61\x20\x02\x00\x00\x9c\x3f\x0e\xa6\x08\xb7\x0f\xc6\x01\x05\xb7\x50\xc6\x10\x00\xa1\x98\x26\x0a\x14\x50\xa6\x84\xb7\x09\xa6\x80\xb7\x08\xcd\x01\xb2\x3f\x51\x00\x50\x02\x20\x18\x1e\x07\xbe\x51\xd6\x02\x00\x97\xb6\x51\xbd\x26\xb6\x51\x4c\xb7\x51\xc1\x01\x06\x26\xea\x3f\x51\x1e\x07\xbe\x51\xa6\x52\xbd\x20\xbe\x51\xb6\x52\xd7\x02\x00\x5c\xbf\x51\xc3\x01\x06\x26\xe9\x5f\xbf\x51\xb6\x11\xbe\x51\x1e\x07\x0f\x10\xfd\xd6\x02\x00\xb7\x11\x5c\xbf\x51\xc3\x01\x06\x26\xec\x0d\x10\xfd\xae\x08\xa6\x38\xbd\x26\xc6\x3f\xfe\xc7\x01\x8c\xc6\x3f\xff\xc7\x01\x8d\xcc\x3f\xfe\x00\x00\x64\x6f\x7b\x57\x8c\x6b\x3f\x00\x00\x00\x7a\x68\x6f\x3f\x68\x7b\xeb\xeb\x8c\x6b\x3f\x00\x01\x02\x03\x0d\x0c\x0b\x0a\x09\x08\x07\x06\x05\xae\x0b\xd6\x01\xa6\xb7\x09\x00\x50\x05\xd6\x01\x8e\x20\x03\xd6\x01\x9a\xb7\x08\x5a\x2a\xeb\x81\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
    ser.timeout = 0.5
    d = serreadany(ser)
    print(doescape(d))
#    
#    d = b''
    #ser.write(b'\xaa')
    #ser.write(b'\xaa\xaa\xaa')
    #ser.write(b'\x01\x01\x0d\x00\x00\x00\x03\x00\xaa\x46\x01\x0d\x00\x00\x00\x03\x00')
#    ser.write(b'\xaa\xaa\xaa')
#    d = ser.read(1)
#    if d != b'\xaa':
#        print("NO: " + doescape(d))
#    ser.write(b'\xaa')
#    d = ser.read(1)
#    if d != b'\xaa':
#        print("NO: " + doescape(d))
#    ser.write(b'\xaa')
#    d = ser.read(1)
#    if d != b'\xaa':
#        print("NO: " + doescape(d))
#    ser.write(b'\x01\x01')
#    d = ser.read(2)
#    if d != b'\x01':
#        print("NO: " + doescape(d))
#    ser.write(b'\x01')
#    d = ser.read(1)
#    if d != b'\x01':
#        print("NO: " + doescape(d))
#
#    while True:
#        d = ser.read(1)
#        if len(d) > 1:
#            raise Exception("too much data")
#        if len(d) == 1:
#            print(doescape(d))
