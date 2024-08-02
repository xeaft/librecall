import os
import tempfile
import time
import sys

isWindows: bool = os.name.lower().find("nt") > -1
tmpPath: str = "/tmp" if not isWindows else tempfile.gettempdir()
dbFileName = "images.db"
info = "-i" in sys.argv

def getLocation(rawPath: str) -> str:
    home = os.path.expanduser("~")

    if isWindows:
        if rawPath[0] == "/":
            rawPath = "C:" + rawPath[1:]
        rawPath = rawPath.replace("/", "\\")

    rawPath = rawPath.replace("~", home)
    return rawPath

def getTimeMS() -> int:
    return time.time_ns() // 1_000_000
