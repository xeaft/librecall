import os
import subprocess
from SystemInfo import SystemInfo

sysInfo: SystemInfo = SystemInfo()

def runCmd(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def hasCmd(cmd: str) -> bool:
    runcmd: list[str] = ["which", cmd]
    if os.name.lower() == "nt":
        runcmd = ["powershell", "-Command", f"(Get-Command {cmd}).Path"]
    return len(runCmd(runcmd).stdout) > 0


def gnomeScreenshot():
    filename = ".lc-gnome-sc.tmp.png"
    runCmd(["gnome-screenshot", "-f", filename])
    data = None

    with open(filename, "rb") as f:
        data = f.read()
    os.remove(filename)

    return data


tools: dict[str, callable] = {
    "flameshot": lambda: runCmd(["flameshot", "full", "--raw"]).stdout,
    "spectacle": lambda: runCmd(["spectacle", "-nbfo", "/dev/stdout"]).stdout,
    "gnome": gnomeScreenshot,
    "scrot": lambda: runCmd(["scrot", "-"]).stdout,
    "grim": lambda: runCmd(["grim", "-"]).stdout,
    "grimblast": lambda: runCmd(["grimblast", "save", "screen", "-"]).stdout
}

defaultTool = ["Default"] if not sysInfo.isWaylandSession() else []
availableTools: list[str] = defaultTool + [cmd for cmd in tools.keys() if hasCmd(cmd)]
