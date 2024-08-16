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
import screenshotter
import stuff
import window

stuff.info = "-i" in sys.argv
openCfg = "-c" in sys.argv or "--config" in sys.argv
firstTimeLockFile = f"{stuff.fileLocation}/.firsttime.lck"
firstTime = not os.path.exists(firstTimeLockFile)

if firstTime and not "-s" in sys.argv:
    firstTimeResponse = firstTimeDialogue.doUI()
    if firstTimeResponse == "Closed":
        sys.exit(0)
    with open(firstTimeLockFile, "w"):
        pass
    openCfg = True

if openCfg:
    window.doUI()
else:
    screenshotter.doWork()
