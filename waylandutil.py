import subprocess
import os

def isWaylandSession() -> bool:
    return os.getenv("XDG_SESSION_TYPE") == "wayland"

def runCmd(cmd : list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def hasCmd(cmd : str) -> bool:
    return len(runCmd(["which", cmd]).stdout) > 0

def gnomeScreenshot():
    filename = ".lc-gnome-sc.tmp.png"
    runCmd(["gnome-screenshot", "-f", filename], True)
    data = None

    with open(filename, "rb") as f:
        data = f.read()
    os.remove(filename)

    return data

screenshotters = {
    "flameshot": lambda: runCmd(["flameshot", "full", "--raw"]).stdout,
    "gnome": gnomeScreenshot,
    "scrot": lambda: runCmd(["scrot", "-"]).stdout,
}

def getScreenshotUtil() -> str:
    for i in screenshotters:
        if hasCmd(i):
            return i
    return None