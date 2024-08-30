import os
import subprocess

def runCmd(cmd : list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def hasCmd(cmd : str) -> bool:
    return len(runCmd(["which", cmd]).stdout) > 0

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
    "grim": lambda: runCmd(["grim", "-"]).stdout
}

availableTools: list[str] = [cmd for cmd in tools.keys() if hasCmd(cmd)]