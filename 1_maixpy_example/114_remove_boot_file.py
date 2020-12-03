import sensor
import image
import time
import os
import sys
import time

sys.path.append('')
sys.path.append('.')
os.chdir("/flash")
sys.path.append('/flash')

print(os.listdir())
try:
    os.remove("main.py")
except Exception:
    pass
try:
    os.remove("boot.py")
except Exception:
    pass

print(os.listdir())
