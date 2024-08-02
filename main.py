import librecallUI
import os
import stuff
import sys
import screenshotter

if __name__ != "__main__":
    print("no. why")
    exit(1)

stuff.info = "-i" in sys.argv

if stuff.info:
    print("debug info enabled")

if "-c" in sys.argv or "--config" in sys.argv:
    librecallUI.doUI()
else:
    screenshotter.doWork()
