import sys

if __name__ != "__main__":
    print("no. why")
    sys.exit(1)

if "--wayland-tools" in sys.argv:
    print("""
        List of screenshotting tools on wayland supported by librecall:

        - flameshot
        - grim
        - spectacle
        - scrot
        - gnome-screenshot

        You can download any of these with your package manager, and
        make sure it actually works under your compositor.

        gnome-screenshot does a shutter sound effect each screenshot.
        This is preventable, but would require root access. Maybe in
        the future, ok?
    """)
    sys.exit(0)

import firstTimeDialogue
import os
import screenshotProcess
import shutil
import window
from SystemInfo import SystemInfo

sysInfo = SystemInfo()


if not os.path.exists(sysInfo.dataDir):
    os.makedirs(sysInfo.dataDir)

legacyPaths: list[str] = [
    os.path.join(sysInfo.fileLocation, ".last.librerecall"),
    os.path.join(sysInfo.fileLocation, ".firsttime.lck"),
    os.path.join(sysInfo.fileLocation, "settings.json"),
    os.path.join(sysInfo.fileLocation, "images.db")
]

for path in legacyPaths:
    if os.path.exists(path):
        ind = path.rindex("/")
        file = path[ind+1:]
        newPath = os.path.join(sysInfo.dataDir, file)

        if sysInfo.info:
            print(f"Moving old file to data directory\t{file} -> data/{file}")

        shutil.move(path, newPath)

openCfg = "-c" in sys.argv or "--config" in sys.argv
firstTimeLockFile = f"{sysInfo.dataDir}/.firsttime.lck"
firstTime = not os.path.exists(firstTimeLockFile)

if firstTime and not "-s" in sys.argv:
    firstTimeResponse = firstTimeDialogue.doUI()
    if firstTimeResponse == "quit":
        sys.exit(0)
    with open(firstTimeLockFile, "w"):
        pass
    openCfg = True

if openCfg:
    window.createSettingsWindow()
else:
    screenshotProcess.doWork()
