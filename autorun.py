import stuff
import linuxAutorun
import windowsAutorun
import sys

if stuff.usedOS == "linux":
    linuxAutorun.doYourThing(sys.argv)
elif stuff.usedOS == "windows":
    windowsAutorun.doYourThing(sys.argv)
else:
    print("This autorun script only supports Windows and Linux (with the systemd init system)")