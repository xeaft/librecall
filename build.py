import customtkinter as ctk
import os
import platform
import subprocess
import sys

OS = platform.system().lower()
if OS not in ["windows", "linux"]:
    sys.exit(1)

CTKPath = os.path.dirname(os.path.abspath(ctk.__file__))

if OS == "linux":
    subprocess.run(["python", "-m" "PyInstaller", "-y", "--clean", "-n", "Librecall", "-D", "--add-data", "img:img", "--add-data", f"{CTKPath}:customtkinter", "librecall.py"])
else:
    subprocess.run(["python", "-m" "PyInstaller", "-w", "-y", "--clean", "-n", "Librecall", "-D", "-i", "img/icon.ico", "--add-data", "img;img", "--add-data", f"{CTKPath}:customtkinter", "librecall.py"])