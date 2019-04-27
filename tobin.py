#!/usr/bin/env python

import sys
import os

strbuf = ''
while True:
    c = sys.stdin.read(1)
    if len(c) == 0:
        break
    if c.isspace():
        continue
    strbuf = strbuf + c
    if len(strbuf) == 2:
        b = bytes.fromhex(strbuf)
        strbuf = ''
        sys.stdout.buffer.write(b)
