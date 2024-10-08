import shutil
import platform
import sys
import os
import subprocess

def doYourThing(argv, systemd):
    OS = platform.system().lower()
    if OS != "linux":
        raise OSError("This script is designed to run on Linux systems only.")

    def getArgv(txt):
        for index, value in enumerate(argv):
            if value.find(txt) > -1:
                return index

        return None

    def disableAutorunService():
        subprocess.run(["systemctl", "--user", "stop", "librecall"])
        subprocess.run(["systemctl", "--user", "disable",  "librecall"])

    overrideSystemdCheck = (getArgv("--systemd-override") is not None)

    if (not systemd and (not overrideSystemdCheck)):
        raise OSError("This autorun script requires the systemd init system and has detected that you dont use it. If you are using systemd, please use the --systemd-override flag. Otherwise, configure your own autorun system.")

    homePath = os.path.expanduser("~")
    filePath = os.path.dirname(os.path.abspath(__file__))
    scriptPath = os.path.abspath(os.path.join(filePath, '..'))
    runner = f"{scriptPath}/dist/Librecall"
    pythonPath = None
    serviceDir = f"{homePath}/.config/systemd/user"
    servicePath = f"{serviceDir}/librecall.service"

    if (getArgv("-r") is not None) or getArgv("--remove") is not None:
        if os.path.exists(servicePath):
            disableAutorunService()
            os.remove(servicePath)
            print("Librecall autorun service successfully removed.")
        else:
            print("Librecall autorun service does not exist; nothing to remove.")
        sys.exit(0)

    pythonPathArg = getArgv("--python=")
    if pythonPathArg is not None:
        pythonPath = argv[pythonPathArg].split("=")[1]

    def getPythonPath():
        pythonPath = shutil.which("python")
        if not pythonPath:
            pythonPath = shutil.which("python3")
            if not pythonPath:
                raise Exception("Neither 'python' nor 'python3' was found in your PATH. Please specify the path to your Python interpreter using the --python=python_path argument.")

        return pythonPath

    if not pythonPath:
        pythonPath = getPythonPath()

    data = ""
    with open(f"{filePath}/Service/librecall.service.gen", "r") as f:
        data = f.read()

    data = data.replace("<PYTHON_PATH>", pythonPath)
    data = data.replace("<SCRIPT_PATH>",  scriptPath + "/librecall.py")

    if not os.path.exists(serviceDir):
        os.makedirs(serviceDir)

    with open(servicePath, "w") as f:
        f.write(data)

    subprocess.run(["systemctl", "--user", "daemon-reload"])
    disableAutorunService()
    subprocess.run(["systemctl", "--user", "enable", "--now", "librecall"])
    print("Started librecall service successfully")