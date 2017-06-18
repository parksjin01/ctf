from pwn import *
import re
import base64

instruction = raw_input("Enter your linux command: ")
pattern = re.compile("[/|$|-|_|&|>|`|'|\"|%|;]|(cat)|(flag)|(bin)|(sh)|(bash)")
if (pattern.search(instruction) != None):
        print "You can't use that command"
        exit(0)
proc = process("./babymisc")
proc.recvuntil(">")
proc.sendline("TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oih=")
proc.recvuntil("[+] Input 1 ")
proc.sendline("TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oih=")
proc.recvuntil("[+] Input 2 ")
proc.sendline("TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oih==")
proc.recvuntil(">")
proc.sendline(base64.b64encode(instruction))
proc.sendline('\n')
proc.sendline('\n')
proc.recv(1024)
proc.recv(1024)
try:
        while True:
                print proc.recvuntil("\n"),
except:
        pass
