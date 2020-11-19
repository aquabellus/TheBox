import time
import getpass

tgl = time.strftime("%d %b", time.localtime())
bln = time.strftime("%b %Y", time.localtime())
thn = time.strftime("%Y", time.localtime())
jam = time.strftime("%H:%M:%S", time.localtime())
full = time.strftime("%Y/%m/%d", time.localtime())
nama = getpass.getuser()

