import sys, marshal, dis

pyc_file = 'miaw_chal.cpython-313.pyc'

with open(pyc_file, 'rb') as f:
    f.read(16)  # skip header (Python 3.7+)
    code = marshal.load(f)

dis.dis(code)
