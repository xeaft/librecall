import subprocess
import os
import stuff
import config
import sys

config.loadConfig()

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
    "spectacle": lambda: runCmd(["spectacle", "-nbfo", "/dev/stdout"]).stdout,
    "gnome": gnomeScreenshot,
    "scrot": lambda: runCmd(["scrot", "-"]).stdout,
    "grim": lambda: runCmd(["grim", "-"]).stdout
}

availableScreenshotters = [tool for tool in screenshotters.keys() if hasCmd(tool)]

def getScreenshotUtil() -> str:
    preferredTool = config.get("SCREENSHOT_TOOL")
    if preferredTool != "default":
        return preferredTool

    if availableScreenshotters:
        return availableScreenshotters[0]

    return None


if not stuff.isWindows:
    stuff.isWayland = isWaylandSession()
    stuff.screenshotTool = getScreenshotUtil()

if not availableScreenshotters and stuff.isWayland:
    print("""
        Wayland doesnt support PIL's default ImageGrab.grab() method, and you do
        not have any screenshotting tools compatible with librecall. Please refer
        to the README or use the "--wayland-tools" flag and download a tool that
        works on your compositor.
        """)

    sys.exit(5)