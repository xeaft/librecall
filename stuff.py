import os
import tempfile
import time
import sys
import waylandutil

isWindows: bool = os.name.lower().find("nt") > -1
tmpPath: str = "~/tmp" if not isWindows else tempfile.gettempdir()
dbFileName = "images.db"
info = "-i" in sys.argv
isWayland : bool = False
waylandScreenshotUtil : str = None

if not isWindows:
    isWayland = waylandutil.isWaylandSession()
    if isWayland:
        waylandScreenshotUtil = waylandutil.getScreenshotUtil()

def getLocation(rawPath: str) -> str:
    if isWindows:
        home: str = os.path.expanduser("~")
        rawPath = rawPath.replace("/", "\\")
        rawPath = rawPath.replace("~", home)

    return rawPath

def getTimeMS() -> int:
    return time.time_ns() // 1_000_000