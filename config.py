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
    "SAVE_LOCATION": stuff.getLocation(f"./{stuff.dbFileName}")
}

config: dict[str, Any] = {}

def makeConfigIfNotExists() -> None:
    try:
        file = open("./settings.json", "r")
    except:
        if stuff.info:
            print("No existing configuration file. (created)")

        file = open("./settings.json", "w")
        file.write(json.dumps(defaultConfig))
    finally:
        if file:
            file.close()

def loadConfig() -> dict:
    global config

    makeConfigIfNotExists()
    with open("./settings.json", "r") as settingsFile:
        settings = settingsFile.read()
        config = json.loads(settings)

def saveConfig() -> bool:
    shutil.copyfile("./settings.json", "./settings.json.bak")
    fileSaved: bool = _saveConfigFile()

    if not fileSaved:
        shutil.move("./settings.json.bak", "./settings.json")
        return False
    else:
        os.remove("./settings.json.bak")
    
    return True


def _saveConfigFile() -> bool:
    succ: bool = False

    try:
        with open("./settings.json", "w") as f:        
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