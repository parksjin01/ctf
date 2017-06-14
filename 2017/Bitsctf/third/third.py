from pwn import *

proc1 = process('/home/knight/ctf/exploit/time')
key = proc1.recvuntil('END')
key = key.split(',')[:-1]
proc2 = process('/home/knight/ctf/exploit/third')
for i in range(30):
        proc2.sendline(key[i])
flag = proc2.recvuntil('\n').split(' : ')[-1]
print flag.lstrip('congrats you are rewarded with the flag ')
