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
    ser.baudrate = 4800
    ser.parity = serial.PARITY_NONE
    ser.bytesize = serial.EIGHTBITS
    ser.rtscts = False
    ser.xonxoff = False
    ser.timeout = 5
    ser.open()
    sys.stderr.write("open\n")
    get_attention(ser)


    loopwrite(ser, b'\x01\x01\x0d\x00\x00\x00\x03\x00')
    d = ser.read(1)
    print(doescape(d))

    get_attention(ser)
    loopwrite(ser, b'\x46\x01\x0d\x00\x00\x00\x03\x00')
    timeout = 5
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
