#!/usr/bin/env python

import sys
import time
import os
import serial

def doescape(data):
    return "".join(["%02x" % x for x in data])

def serreadany(ser):
    outdata = b''
    while True:
        data = ser.read(1)
        if len(data) == 0:
            return outdata
        outdata = outdata + data


def serread(ser, nbytes):
    outdata = b''
    while nbytes > 0:
        data = ser.read(1)
        if data:
            outdata = outdata + data
            nbytes = nbytes - 1
    return outdata


if __name__ == '__main__':
    devname = sys.argv[1]
    if len(sys.argv) > 2:
        secswait = float(sys.argv[2])
    else:
        secswait = 10

    sys.stderr.write("opening device: " + devname + "\n")
    ser = serial.Serial()
    ser.port = devname
    ser.baudrate = 4800
    ser.parity = serial.PARITY_NONE
    ser.bytesize = serial.EIGHTBITS
    ser.rtscts = False
    ser.xonxoff = False
    ser.timeout = secswait 
    ser.open()
    sys.stderr.write("open\n")
    while True:
        lastts = int(round(time.time() * 1000))
#        print("---")
#        d = serreadany(ser)
        d = ser.read(1)
        if len(d) == 0:
            break;
        curts = int(round(time.time() * 1000))
        print(f'{curts} {curts-lastts}: {doescape(d)}')

