import os
import shutil
import subprocess
import sys

def doYourThing(argv):
    directory = os.getcwd() + "\\dist\\Librecall"
    if len(argv) > 1 and argv[1].startswith("directory="):
        directory = argv[1].split("directory=")[1]

    executable = f"{directory}\\Librecall.exe"
    shortcut = f"{directory}\\librecall.lnk"

    if not os.path.isdir(directory):
        print("Default build directory doesnt exist, specifiy your executable's directory with --directory=DIR")
        sys.exit(1)

    if not os.path.isfile(executable):
        print("Executable 'Librecall.exe' not found. Specifiy your executable's directory with --directory=DIR")
        sys.exit(2)

    powershellScript = f'''
    $targetPath = "<EXEC>"
    $shortcutPath = "<SHORTCUT>"
    $shell = New-Object -COM WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $targetPath
    $shortcut.Arguments = "-s"
    $shortcut.Save()
    '''
    powershellScript = powershellScript.replace("<EXEC>", executable).replace("<SHORTCUT>", shortcut)

    result = subprocess.run(['powershell', '-Command', powershellScript], capture_output=True, text=True)
    if not result.stdout and not result.stderr:
        print("Created shortcut successfully")
    else:
        sys,exit(3)


    startFolder = os.getenv("APPDATA") + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    try:
        shutil.move(shortcut, startFolder)
    except shutil.Error as e:
        e = str(e)
        if e.find("Destination path") > -1 and e.find("already exists") > -1:
            print("Startup shortcut already exist. Deleting")
            os.remove(startFolder + "\\librecall.lnk")
            print("Removed existing shortcut")
            try:
                shutil.move(shortcut, startFolder)
            except shutil.Error as e2:
                print("Failed to move the shortcut - " + str(e2))
                sys.exit(4)

    print("Added librecall to startup successfully")
