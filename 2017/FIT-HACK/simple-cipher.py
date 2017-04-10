#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
tmp_mes = binascii.unhexlify('0c157e2b7f7b515e075b391f143200080a00050316322b272e0d525017562e73183e3a0d564f6718')
tmp = list(tmp_mes)
idx = len(tmp)/8
for i in range(len(tmp)/idx):
    for ids in range(idx):
        tmp[i+8*ids] = tmp_mes[i*idx+ids]
mes = ''.join(tmp)

key = "J2msBeG8"

m = []
idx = 0
for i in mes:
    print ord(i), ord(key[idx%len(key)]), chr(ord(i)^ord(key[idx%len(key)]))
    m.append(ord(i)^ord(key[idx%len(key)]))
    idx += 1

enc_mes = ""
for j in range(len(m)):
    enc_mes += "%c" % chr(m[j])

print enc_mes
