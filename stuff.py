import os
import platform
import tempfile
import time
import sys
import subprocess

def checkSystemd():
    systemdText = subprocess.run(["systemctl", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
    return  systemdText.find("See the systemctl(1) man page for details.") > -1 # what a detection..

isWindows: bool = os.name.lower().find("nt") > -1
usedOS = platform.system().lower()
tmpPath: str = tempfile.gettempdir()
dbFileName = "images.db"
cwd = os.getcwd()
fileLocation = os.path.dirname(os.path.abspath(__file__))
info = "-i" in sys.argv
isWayland : bool = False
screenshotTool : str = None
usingSystemd = False

if usedOS == "linux":
    usingSystemd = checkSystemd()



def getLocation(rawPath: str) -> str:
    if isWindows:
        home: str = os.path.expanduser("~")
        rawPath = rawPath.replace("/", "\\")
        rawPath = rawPath.replace("~", home)

    return rawPath

def getTimeMS() -> int:
    return time.time_ns() // 1_000_000