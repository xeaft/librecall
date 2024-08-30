import customtkinter as ctk
import os
import platform
import shutil
import subprocess
import sys
import PIL

OS = platform.system().lower()
if OS not in ["windows", "linux"]:
    sys.exit(1)

home = os.path.expanduser("~")
scriptPath = os.path.dirname(os.path.abspath(__file__))
CTKPath = os.path.dirname(os.path.abspath(ctk.__file__))
PILPath = os.path.dirname(os.path.abspath(PIL.__file__))

def getPythonPath():
    for arg in sys.argv:
        if arg.startswith("--python="):
            return arg.split("=")[1]

    pythonPath = shutil.which("python")
    if pythonPath:
        return pythonPath

    pythonPath = shutil.which("python3")
    if pythonPath:
        return pythonPath

    pythonPath = "/usr/bin/python"
    if os.path.exists(pythonPath):
        return pythonPath
    
    pythonPath = "/usr/bin/python3"
    if os.path.exists(pythonPath):
        return pythonPath

    raise Exception("No Python interpreter was detected. Please specify the path to your Python interpreter using the --python=python_path argument.")

def makeDesktopFile():
    desktopDir = f"{home}/.local/share/applications"
    desktopFilePath = f"{scriptPath}/AutorunScripts/Librecall.desktop.gen"
    desktopContent = ""

    with open(desktopFilePath, "r") as f:
        desktopContent = f.read()

    pythonPath = getPythonPath()

    desktopContent = desktopContent.replace("<PYTHON_PATH>", pythonPath)
    desktopContent = desktopContent.replace("<SCRIPT_PATH>", f"{scriptPath}/librecall.py")
    desktopContent = desktopContent.replace("<ICON_PATH>", f"{scriptPath}/img/icon.ico")

    with open(f"{desktopDir}/Librecall.desktop", "w") as f:
        f.write(desktopContent)

if __name__ == "__main__":
    if OS == "linux":
        subprocess.run(["python", "-m" "PyInstaller", "-y", "--clean", "-n", "Librecall", "-D", "--add-data", "img:img", "--add-data", f"{CTKPath}:customtkinter", "--add-data", f"{PILPath}:PIL", "librecall.py"])
        if not "--no-desktop" in sys.argv:
            makeDesktopFile()
    else:
        subprocess.run(["python", "-m" "PyInstaller", "-w", "-y", "--clean", "-n", "Librecall", "-D", "-i", "img/icon.ico", "--add-data", "img;img", "--add-data", f"{CTKPath}:customtkinter", "--add-data", f"{PILPath}:PIL", "librecall.py"], shell=True)