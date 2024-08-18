import AutorunScripts.linuxAutorun as linuxAutorun
import AutorunScripts.windowsAutorun as windowsAutorun
import sys
from SystemInfo import SystemInfo

sysInfo = SystemInfo()

if sysInfo.usedOS == "linux":
    linuxAutorun.doYourThing(sys.argv, sysInfo.usingSystemd)
elif sysInfo.usedOS == "windows":
    windowsAutorun.doYourThing(sys.argv)
else:
    print("This autorun script only supports Windows and Linux (with the systemd init system)")