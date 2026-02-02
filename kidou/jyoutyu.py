# jyoutyu.py
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

subprocess.Popen([
    sys.executable,
    os.path.join(BASE_DIR, "main.py")
])
