import os
import PySimpleGUI as sg
import screenshotDB
import timeline
from ConfigManager import ConfigManager
from screenshotters import availableTools
from SystemInfo import SystemInfo

def doUI():
    configManager = ConfigManager()
    sysInfo = SystemInfo()

    scDelay = str(configManager.get("SCREENSHOT_FREQUENCY_MS"))
    enabled = configManager.get("ENABLED")
    autoDeleteType = configManager.get("AUTO_DELETE_TYPE")
    autoDeleteOptions = ["Hours", "Days", "Disabled"]
    autoDeleteFrequency = configManager.get("DELETE_AFTER_PERIOD")
    dateFormat = configManager.get("DATE_FORMAT")
    sep = "\\" if sysInfo.usedOS == "windows" else "/"
    currentImageLoc = configManager.get("SAVE_LOCATION").replace(f"{sep}{sysInfo.dbFileName}", "")

    screenshotTool = configManager.get("SCREENSHOT_TOOL")
    screenshotTools = (["default"] if not sysInfo.isWayland else []) + availableTools

    sg.theme_add_new(
        "theme", 
        {
            "BACKGROUND": "#1e1e1e", 
            "TEXT": "#b9b9b9", 
            "INPUT": "#5c5c5c", 
            "TEXT_INPUT": "#b9b9b9", 
            "SCROLL": "#5c5c5c", 
            "BUTTON": ("#b9b9b9", "#5c5c5c"), 
            "PROGRESS": ("#5c5c5c", "#b9b9b9"), 
            "BORDER": 0, 
            "SLIDER_DEPTH": 0, 
            "PROGRESS_DEPTH": 0, 
        }
    )

    sg.theme("theme")

    layout = [
        [sg.Text("Save screenshots "), sg.Push(), sg.Text("On" if enabled else "Off", key="Save_Screenshots_Toggle_Text"), sg.Checkbox(text="", default=enabled, key="Save_Screenshots_Toggle", enable_events=True)],
        [sg.Text("Screenshot frequency (ms) "), sg.Push(), sg.Slider((300_000, 86_400_000), orientation="h", disable_number_display=True, key="Librecall_Screenshot_Interval", enable_events=True, default_value=scDelay), sg.Text("{:02}".format(int(scDelay)), key="Screenshot_Interval_Text")],

        [sg.Text("Auto delete method "), sg.Push(), sg.Combo(autoDeleteOptions, default_value=autoDeleteType, key="Librecall_Auto_Delete_Method", enable_events=True, readonly=True)],
        [sg.Text("Auto delete interval "), sg.Push(), sg.Slider((1, 30), orientation="h", disable_number_display=True, key="Librecall_Auto_Delete_Frequency", enable_events=True, default_value=autoDeleteFrequency), sg.Text("{:02}".format(int(autoDeleteFrequency)), key="Librecall_Auto_Delete_Frequency_Text")],

        [sg.Text("Screenshot DB location "), sg.Push(), sg.In(sysInfo.dbPath, key="Librecall_Save_Location_Text", enable_events=True, readonly=True, disabled_readonly_background_color=("#5C5C5C")), sg.FolderBrowse("Select", initial_folder=".", target="Librecall_Save_Location_Text")],
        [sg.Text("Timeline date format "), sg.Push(), sg.In(f"{dateFormat}", key="Librecall_Timeline_Date_Format", enable_events=True, disabled_readonly_background_color=("#5C5C5C"))],

        [sg.Text("Screenshotting tool "), sg.Push(), sg.Combo(screenshotTools, default_value=screenshotTool, key="Librecall_Screenshot_Tool", enable_events=True, readonly=True)],

        [sg.Button("Extract screenshots", key="Extract_All", expand_x=True)],
        [sg.Button("View timeline", key="View_Timeline", expand_x=True)],

        [sg.Button("Delete screenshots", key="Delete_All", expand_x=True, pad=(5, 20))],

    ]

    window = sg.Window("LibreCall - Settings", layout, size=(650, 370), icon=sysInfo.getLocation(f"{sysInfo.fileLocation}/img/icon_transparent.ico"))
    window.refresh()

    while True:
        event, values = window.read()
        eventValue = values[event] if (values and event in values) else None
        if event == sg.WIN_CLOSED:
            break
        
        elif event == "Librecall_Screenshot_Interval":
            text = "{:08}".format(int(eventValue))
            window["Screenshot_Interval_Text"].update(text)
            configManager.set("SCREENSHOT_FREQUENCY_MS", int(eventValue))

        elif event == "Save_Screenshots_Toggle":
            window["Save_Screenshots_Toggle_Text"].update("On" if eventValue else "Off")
            configManager.set("ENABLED", eventValue)

        elif event == "Delete_All":
            screenshotDB.makeConnection()
            screenshotDB.deleteAll()
            screenshotDB.end()
        
        elif event == "Extract_All":
            screenshotDB.makeConnection()
            screenshotDB.extractAll(f"{sysInfo.fileLocation}/ExtractedImages")
            screenshotDB.end()

        elif event == "Librecall_Auto_Delete_Method":
            configManager.set("AUTO_DELETE_TYPE", eventValue)

        elif event == "Librecall_Auto_Delete_Frequency":
            text = "{:02}".format(int(eventValue))
            window["Librecall_Auto_Delete_Frequency_Text"].update(text)
            configManager.set("DELETE_AFTER_PERIOD", eventValue)

        elif event == "Librecall_Save_Location_Text":
            location = eventValue
            fullFileLoc = os.path.join(eventValue, sysInfo.dbFileName)
            if location != currentImageLoc:
                configManager.set("SAVE_LOCATION", fullFileLoc)
                currentImageLoc = location
                window[event].update(fullFileLoc)

        elif event == "View_Timeline":
            timeline.doUI()

        elif event == "Librecall_Timeline_Date_Format":
            configManager.set("DATE_FORMAT", eventValue)

        elif event == "Librecall_Screenshot_Tool":
            configManager.set("SCREENSHOT_TOOL", eventValue)

    window.close()
