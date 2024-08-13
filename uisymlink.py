import sys
import os
import stuff
import subprocess

if stuff.usedOS != "linux":
    raise OSError("This script is designed to run on linux systems only")

def getArgv(txt):
    for i, v in enumerate(sys.argv):
        if v.find(txt) > -1:
            return i
    return None

directory = os.getcwd() + "/dist/Librecall"
overrideDir = getArgv("--directory")
if overrideDir:
    directory = sys.argv(overrideDir)

wrapperTxt = \
"""#!<SHELL>
"<ABSPATH>/Librecall" -c
"""

wrapper = wrapperTxt.replace("<SHELL>", os.getenv("SHELL")).replace("<ABSPATH>", directory)
wrapperLoc = f"{directory}/wrapper.sh"

with open(wrapperLoc, "w") as f:
    f.write(wrapper)
print("Created wrapper.sh successfully")

subprocess.run(["chmod", "+x", wrapperLoc])
print("Made wrapper.sh executable successfully")

res = subprocess.run(["ln", "-s", wrapperLoc, f"{directory}/UI_SYMLINK"], stderr=subprocess.PIPE, text=True).stderr
if not res:
    print(f"Created symlink successfully - UI_SYMLINK for {wrapperLoc}")
    sys.exit()

if res.find("File exists") > -1:
    print(f"Symlink already exists. deleting..")
    subprocess.run(["rm", f"{directory}/UI_SYMLINK"])
    print("Deleted old symlink")
    res = subprocess.run(["ln", "-s", wrapperLoc, f"{directory}/UI_SYMLINK"], stderr=subprocess.PIPE, text=True).stderr
    if not res:
        print(f"Created symlink successfully - UI_SYMLINK for {wrapperLoc}")
    else:
        print(f"Failed to create the symlink - {res[4:-1]}")
else:
    print(f"Failed to create the symlink - {res[4:-1]}")