#!/usr/bin/env python

import sys
import serial
import time
import select

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("args: devA devB")
        sys.exit(1)
    devA, devB = sys.argv[1], sys.argv[2]
    sera = serial.Serial()
    sera.port = devA
    sera.parity = serial.PARITY_NONE
    sera.bytesize = serial.EIGHTBITS
    sera.rtscts = False
    sera.xonxoff = False
    sera.nonblocking()
    sera.timeout = 0
    sera.open()
    sys.stderr.write(f'A ({devA}) open\n')
    serb = serial.Serial()
    serb.port = devB
    serb.parity = serial.PARITY_NONE
    serb.bytesize = serial.EIGHTBITS
    serb.rtscts = False
    serb.xonxoff = False
    serb.nonblocking()
    serb.timeout = 0
    serb.open()
    sys.stderr.write(f'B ({devB}) open\n')

    sys.stderr.write("selecting\n")
    curts = 0
    while True:
        ready, _, _ = select.select([sera,serb], [], [])
        lastts = curts
        curts = time.time() * 1000
        for r in ready:
            if r == sera:
                c = sera.read(1)
                serb.write(c)
                print(f'{"%.5f" % curts} A: {"%02x" % c[0]}')
            elif r == serb:
                c = serb.read(1)
                sera.write(c)
                print(f'{"%.5f" % curts} B: {"%02x" % c[0]}')




