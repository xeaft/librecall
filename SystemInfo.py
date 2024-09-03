import os
import platform
import tempfile
import time
import sys
import subprocess


class SystemInfo:
    _insts = []

    def __new__(cls):
        if SystemInfo._insts:
            return SystemInfo._insts[0]

        sysInfo = super().__new__(cls)
        SystemInfo._insts.append(sysInfo)

        sysInfo.usedOS = platform.system().lower()
        sysInfo.tmpPath: str = tempfile.gettempdir()
        sysInfo.dbFileName = "images.db"
        sysInfo.cwd = os.getcwd()
        sysInfo.fileLocation = os.path.dirname(os.path.abspath(__file__))
        sysInfo.info = "-i" in sys.argv
        sysInfo.dataDir = sysInfo.getLocation(f"{sysInfo.fileLocation}/data")
        sysInfo.dbPath = sysInfo.getLocation(
            f"{sysInfo.dataDir}/{sysInfo.dbFileName}")
        sysInfo.infoFile = sysInfo.getLocation(
            f"{sysInfo.dataDir}/.last.librerecall")
        sysInfo.isWayland: bool = False if sysInfo.usedOS != "linux" else sysInfo.isWaylandSession()
        sysInfo.usingSystemd = False if sysInfo.usedOS != "linux" else sysInfo.checkSystemd()

        return sysInfo

    def checkSystemd(self):
        systemdText = subprocess.run(
            ["systemctl", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        # what a detection..
        return systemdText.find("See the systemctl(1) man page for details.") > -1

    def getLocation(self, unixPath: str) -> str:
        home: str = os.getenv(
            "HOME") if self.usedOS != "windows" else os.getenv("UserProfile")
        unixPath = unixPath.replace("~", home)

        if self.usedOS == "windows":
            unixPath = unixPath.replace("/", "\\")

        return unixPath

    def isWaylandSession(self) -> bool:
        if self.usedOS != "linux":
            return False
        return os.getenv("XDG_SESSION_TYPE") == "wayland"

    @staticmethod
    def getTimeMS(self=None) -> int:
        return time.time_ns() // 1_000_000

    def makeInfoFileIfNotExists(self) -> None:
        file = None
        try:
            file = open(self.infoFile, "r")
        except FileNotFoundError:
            file = open(self.infoFile, "w")
            file.write(str(self.getTimeMS()))
        finally:
            if file:
                file.close()
