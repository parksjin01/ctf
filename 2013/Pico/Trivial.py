#!/usr/bin/env python
import sys
import binascii

alphaL = "abcdefghijklnmopqrstuvqxyz"
alphaU = "ABCDEFGHIJKLMNOPQRSTUVQXYZ"
num    = "0123456789"
keychars = num+alphaL+alphaU

ciphertext = "Bot kmws mikferuigmzf rmfrxrwqe abs perudsf! Nvm kda ut ab8bv_w4ue0_ab8v_DDU"
res = ''
key = [55, 0, 25, 54, 3, 12, 27, 14, 7, 20, 14, 34]
for i in range(len(ciphertext)):
    if ciphertext[i] in alphaL:
        rotate_amount = key[i%len(key)]%26
        enc_char = ord(ciphertext[i]) - rotate_amount
        if enc_char < ord('a'):
            enc_char = -ord('a') + ord('z') + enc_char +1
    elif ciphertext[i] in alphaU:
        rotate_amount = key[i%len(key)]%26
        enc_char = ord(ciphertext[i]) - rotate_amount
        if enc_char < ord('A'):
            enc_char = -ord('A') + ord('Z') + enc_char +1
    elif ciphertext[i] in num:
        rotate_amount = key[i%len(key)]%10
        enc_char = ord(ciphertext[i]) - rotate_amount
        if enc_char < ord('0'):
            enc_char = -ord('0') + ord('9') + enc_char +1
    else:
        enc_char = ord(ciphertext[i])


    res += chr(enc_char)
print res, binascii.hexlify(res)
