import sys



a = '1'
a_utf8 = a.encode('utf-8')
print(a_utf8)

int(a)

int.from_bytes(b'1', sys.byteorder)

int.from_bytes(, sys.byteorder)
