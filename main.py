import firstTimeDialogue
import os
import screenshotter
import stuff
import sys
import window

if __name__ != "__main__":
    print("no. why")
    exit(1)

stuff.info = "-i" in sys.argv
openCfg = "-c" in sys.argv or "--config" in sys.argv
firstTimeLockFile = f"{stuff.fileLocation}/.firsttime.lck"
firstTime = not os.path.exists(firstTimeLockFile)

if firstTime and not "-s" in sys.argv:
    firstTimeResponse = firstTimeDialogue.doUI()
    if firstTimeResponse == "Closed":
        exit()
    with open(firstTimeLockFile, "w"):
        pass
    openCfg = True

if openCfg:
    window.doUI()
else:
    screenshotter.doWork()
