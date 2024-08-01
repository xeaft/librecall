import os
import tempfile
import time
import sys

isWindows: bool = os.name.lower().find("nt") > -1
tmpPath: str = "~/tmp" if not isWindows else tempfile.gettempdir()
dbFileName = "images.db"
info = "-i" in sys.argv

def getLocation(rawPath: str) -> str:
    if isWindows:
        home: str = os.path.expanduser("~")
        rawPath = rawPath.replace("/", "\\")
        rawPath = rawPath.replace("~", home)

    return rawPath

def getTimeMS() -> int:
    return time.time_ns() // 1_000_000