import string
key = string.ascii_letters + '1234567890'

verify_arr = [193, 35, 9, 33, 1, 9, 3, 33, 9, 225]
res = {}

for char in key:
    tmp = (((ord(char) << 5) | (ord(char) >> 3)) ^ 111) & 255
    res[tmp] = char

for char in verify_arr:
    print res[char],

