import stuff
import json
import shutil
import os
from typing import Any

defaultConfig : dict[str, Any] = {
    "ENABLED": True,
    "AUTO_DELETE_TYPE": "Disabled",
    "DELETE_AFTER_PERIOD": 1,
    "SCREENSHOT_FREQUENCY_MS": 3_600_000, # once per hour
    "SAVE_LOCATION": stuff.getLocation(f"{stuff.fileLocation}/{stuff.dbFileName}"),
    "DATE_FORMAT": r"%d.%m. %Y %H:%M.%S"
}

config: dict[str, Any] = {}
savePath = f"{stuff.fileLocation}/settings.json"

def makeConfigIfNotExists() -> None:
    try:
        file = open(savePath, "r")
    except:
        if stuff.info:
            print("No existing configuration file. (created)")

        file = open(savePath, "w")
        file.write(json.dumps(defaultConfig))
    finally:
        if file:
            file.close()

def loadConfig() -> dict:
    global config
    data = {}
    makeConfigIfNotExists()
    with open(savePath, "r") as settingsFile:
        settings = settingsFile.read()
        data = json.loads(settings)
    
    targetKeys = list(defaultConfig.keys())
    for i in targetKeys:
        if i not in data:
            data[i] = defaultConfig[i]

    config = data
    

def saveConfig() -> bool:
    shutil.copyfile(savePath, f"{savePath}.bak")
    fileSaved: bool = _saveConfigFile()

    if not fileSaved:
        shutil.move(f"{savePath}.bak", savePath)
        return False
    else:
        os.remove(f"{savePath}.bak")
    
    return True


def _saveConfigFile() -> bool:
    succ: bool = False

    try:
        with open(savePath, "w") as f:        
            f.write(json.dumps(config))
            succ = True
    except:
        succ = False

    return succ

def get(setting: str) -> Any:
    if setting in config:
        return config[setting]
    
def set(setting: str, value: Any) -> None:
    config[setting] = value
    saveConfig()