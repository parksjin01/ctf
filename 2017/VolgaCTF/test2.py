# -*-encoding:utf-8 -*-
#
# from PIL import Image
#
# ima = Image.open('/Users/Knight/Desktop/세종 말뭉치/A.png')
# imb = Image.open('/Users/Knight/Desktop/세종 말뭉치/B.png')
#
# la = ima.load()
# lb = imb.load()
# cnt = 0
#
# for x in range(370):
#     for y in range(370):
#         if la[x, y] != lb[x, y]:
#             la[x, y] = 0
#         else:
#             la[x, y] = 255
# ima.show()
# print cnt

import subprocess

def input(num):
    tmp1 = num
    tmp2 = 0
    res = ''
    a = '2FuMlX%3kBJ:.N*epqA0Lh=En/diT1cwyaz$7SH,OoP;rUsWv4g\\Z<tx(8mf>-#I?bDYC+RQ!K5jV69&)G'
    for i in range(17):
        tmp1 *= 0x40f7
        tmp1 += 0x7cc8b
        tmp1, tmp2 = tmp1%0x7fffffff, tmp1%0x7fffffff
        res += a[tmp2%0x52]
    return res

for i in range(150000):
    a = input(i)
    subprocess.call(['openssl', 'aes-128-cbc', '-d', '-base64', '-in', '/Users/Knight/Desktop/세종 말뭉치/flag.zip.enc', '-pass', 'pass:'+a, '-out', '/Users/Knight/Desktop/세종 말뭉치/plain.txt'])
# i = 0
# while True:
#     a = input(i)
#     if 'flag' == a[:4].lower():
#         print a
#         break
#     else:
#         i += 1

