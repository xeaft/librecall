import window
import stuff
import sys
import screenshotter

if __name__ != "__main__":
    print("no. why")
    exit(1)

stuff.info = "-i" in sys.argv

if "-c" in sys.argv or "--config" in sys.argv:
    window.doUI()
else:
    screenshotter.doWork()
