import os
import sys

print("main.py-------------->%s" % r"D:\00-python")
print("os.path.abspath('')--->%s" % os.path.abspath(''))
print("os.path.abspath('.')-->%s" % os.path.abspath('.'))
print("os.path.abspath('./')->%s" % os.path.abspath('./'))
print("sys.path[0]----------->%s" % sys.path[0])
print("sys.argv[0]----------->%s" % sys.argv[0])
print("os.getcwd()----------->%s" % os.getcwd())
