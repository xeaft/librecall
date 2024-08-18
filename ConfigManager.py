import config

class ConfigManager:
    _insts = []

    def __new__(cls):
        if ConfigManager._insts:
            return ConfigManager._insts[0]
        
        cfgMgr = super().__new__(cls)
        ConfigManager._insts.append(cfgMgr)
        config.loadConfig()
        return cfgMgr

    def get(self, setting: str):
        return config.get(setting)

    def set(self, setting: str, value) -> bool:
        succ = config.set(setting, value)

        if not succ:
            print("Failed to save settings. (using a backup)")

        return succ

    def reload(self):
        config.loadConfig()
