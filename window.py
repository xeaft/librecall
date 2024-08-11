import config
import PySimpleGUI as sg
import stuff
import screenshotDB
import timeline

config.loadConfig()
scDelay = str(config.get("SCREENSHOT_FREQUENCY_MS"))
enabled = config.get("ENABLED")
autoDeleteType = config.get("AUTO_DELETE_TYPE")
autoDeleteOptions = ["Hours", "Days", "Disabled"]
autoDeleteFrequency = config.get("DELETE_AFTER_PERIOD")

sep = "\\" if stuff.isWindows else "/"
currentImageLoc = config.get("SAVE_LOCATION").replace(f"{sep}{stuff.dbFileName}", "")

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

    [sg.Text("Screenshot DB location "), sg.Push(), sg.In(f"{currentImageLoc}{sep}{stuff.dbFileName}", key="Librecall_Save_Location_Text", enable_events=True, readonly=True, disabled_readonly_background_color=("#5C5C5C")), sg.FolderBrowse("Select", initial_folder=".", target="Librecall_Save_Location_Text")],

    [sg.Button("Delete screenshots", key="Delete_All", expand_x=True, pad=(0, 20))],

    [sg.Button("Extract screenshots", key="Extract_All", expand_x=True)],
    [sg.Button("View timeline", key="View_Timeline", expand_x=True)]


]

def doUI():
    global currentImageLoc

    window = sg.Window("LibreCall", layout, size=(650, 370))
    window.refresh()

    while True:
        event, values = window.read()
        eventValue = values[event] if (values and event in values) else None
        if event == sg.WIN_CLOSED:
            break
        
        elif event == "Librecall_Screenshot_Interval":
            text = "{:08}".format(int(eventValue))
            window["Screenshot_Interval_Text"].update(text)
            config.set("SCREENSHOT_FREQUENCY_MS", int(eventValue))

        elif event == "Save_Screenshots_Toggle":
            window["Save_Screenshots_Toggle_Text"].update("On" if eventValue else "Off")
            config.set("ENABLED", eventValue)

        elif event == "Delete_All":
            screenshotDB.makeConnection()
            screenshotDB.deleteAll()
            screenshotDB.end()
        
        elif event == "Extract_All":
            screenshotDB.makeConnection()
            screenshotDB.extractAll(f"{stuff.fileLocation}/ExtractedImages")
            screenshotDB.end()

        elif event == "Librecall_Auto_Delete_Method":
            config.set("AUTO_DELETE_TYPE", eventValue)

        elif event == "Librecall_Auto_Delete_Frequency":
            text = "{:02}".format(int(eventValue))
            window["Librecall_Auto_Delete_Frequency_Text"].update(text)
            config.set("DELETE_AFTER_PERIOD", eventValue)

        elif event == "Librecall_Save_Location_Text":
            location = stuff.getLocation(eventValue + f"/{stuff.dbFileName}").replace(f"{sep}{stuff.dbFileName}", "")
            fullFileLoc = f"{location}{sep}{stuff.dbFileName}"
            if location != currentImageLoc:
                config.set("SAVE_LOCATION", fullFileLoc)
                currentImageLoc = location
                window[event].update(fullFileLoc)
        elif event == "View_Timeline":
            timeline.doUI()

    window.close()
