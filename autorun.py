import shutil
import sys
import os
import subprocess

if os.name.lower() == "nt":
    raise OSError("This script is designed to run on Linux systems only.")

def getArgv(txt):
    for index, value in enumerate(sys.argv):
        if value.find(txt) > -1:
            return index

    return None

def isSystemd():
    systemdText = subprocess.run(["systemctl", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
    return  systemdText.find("See the systemctl(1) man page for details.") > -1 # what a detection..

def disableAutorunService():
    subprocess.run(["systemctl", "--user", "stop", "librecall"])
    subprocess.run(["systemctl", "--user", "disable",  "librecall"])

overrideSystemdCheck = (getArgv("--systemd-override") is not None)
usingSystemd = isSystemd()

if (not usingSystemd and (not overrideSystemdCheck)):
    raise OSError("This autorun script requires the systemd init system and has detected that you dont use it. If you are using systemd, please use the --systemd-override flag. Otherwise, configure your own autorun system.")

homePath = os.path.expanduser("~")
filePath = os.getcwd()
pythonPath = None
servicePath = f"{homePath}/.config/systemd/user/librecall.service"

if (getArgv("-r") is not None) or getArgv("--remove") is not None:
    if os.path.exists(servicePath):
        disableAutorunService()
        os.remove(servicePath)
        print("Librecall autorun service successfully removed.")
    else:
        print("Librecall autorun service does not exist; nothing to remove.")
    exit(0)

pythonPathArg = getArgv("--python=")
if pythonPathArg is not None:
        pythonPath = sys.argv[pythonPathArg].split("=")[1]

def getPythonPath():
    pythonPath = shutil.which("python")
    if not pythonPath:
        pythonPath = shutil.which("python3")
        if not pythonPath:
            raise Exception("Neither 'python' nor 'python3' was found in your PATH. Please specify the path to your Python interpreter using the --python=python_path argument.")

    return pythonPath

if not pythonPath:
    pythonPath = getPythonPath()

data = ""
with open("serv/librecall.service.gen", "r") as f:
    data = f.read()

data = data.replace("<PYTHON_PATH>", pythonPath)
data = data.replace("<SCRIPT_PATH>",  filePath + "/main.py")

with open(servicePath, "w") as f:
    f.write(data)

subprocess.run(["systemctl", "--user", "daemon-reload"])
disableAutorunService()
subprocess.run(["systemctl", "--user", "enable", "--now", "librecall"])