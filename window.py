import screenshotters
import timeline
import WindowComponents
from ConfigManager import ConfigManager
from SystemInfo import SystemInfo
from DatabaseHandler import DatabaseHandler

def createWindow():
    WindowComponents.Base.app = WindowComponents.Base.ctk.CTk()
    WindowComponents.Base.app.geometry("650x405")
    WindowComponents.Base.app.title("Librecall")
    WindowComponents.Base.app.resizable(False, False)

def createSettingsWindow():
    if not WindowComponents.Base.app:
        createWindow()
    
    WindowComponents.BaseSetting.elements[WindowComponents.Base.app] = []

    configManager = ConfigManager()
    sysInfo = SystemInfo()
    databaseHandler = DatabaseHandler()

    WindowComponents.Base.ctk.set_appearance_mode("dark")  
    WindowComponents.Base.ctk.set_default_color_theme("blue")
    WindowComponents.Base.screenSize = (WindowComponents.Base.app.winfo_screenwidth(), WindowComponents.Base.app.winfo_screenheight())

    def toggle_enableScreenshots(value):
        configManager.set("ENABLED", value)

    def slider_screenshotFrequency(value):
        configManager.set("SCREENSHOT_FREQUENCY_MS", value * 60000)

    def dropdown_autoDeleteMethod(value):
        configManager.set("AUTO_DELETE_TYPE", value)

    def slider_autoDeleteInterval(value):
        configManager.set("DELETE_AFTER_PERIOD", value)

    def textbox_directory(value):
        configManager.set("SAVE_LOCATION", value)

    def textbox_dateFormat(value):
        configManager.set("DATE_FORMAT", value)

    def dropdown_screenshottingTool(value):
        configManager.set("SCREENSHOT_TOOL", value)

    def button_viewTimeline():
        timeline.createTimelineWindow()

    def button_deleteScreenshots():
        databaseHandler.makeConnection()
        databaseHandler.deleteAll()
        databaseHandler.endConnection()

    def button_exportScreenshots():
        databaseHandler.makeConnection()
        databaseHandler.exportAll(sysInfo.getLocation(sysInfo.fileLocation) + "/ExtractedImages")
        databaseHandler.endConnection()

    enableScreenshotsCheckbox = WindowComponents.Checkbox("Enable screenshots", configManager.get("ENABLED"), "Enabled", "Disabled", toggle_enableScreenshots)
    screenshotFrequencySlider = WindowComponents.Slider("Screenshot frequency (min)", configManager.get("SCREENSHOT_FREQUENCY_MS") / 1000 / 60, 1, 1440, True, slider_screenshotFrequency)

    autoDeleteMethodDropdown = WindowComponents.Dropdown("Auto delete method", ["Disabled", "Hours", "Minutes"], configManager.get("AUTO_DELETE_TYPE"), dropdown_autoDeleteMethod)
    autoDeleteIntervalSlider = WindowComponents.Slider("Auto delete interval", configManager.get("DELETE_AFTER_PERIOD"), 1, 30, slider_autoDeleteInterval)

    dbDirectoryTextbox = WindowComponents.TextInput("Directory", configManager.get("SAVE_LOCATION"), textbox_directory, "[a-zA-Z0-9_/\\-. s]")

    dateTimeFormatTextbox = WindowComponents.TextInput("Timeline date format", configManager.get("DATE_FORMAT"), textbox_dateFormat)

    screenshottingToolDropdown = WindowComponents.Dropdown("Screenshotting tool", screenshotters.availableTools, None, dropdown_screenshottingTool)

    viewTimelineButton = WindowComponents.FullWidthButton("View Timeline", button_viewTimeline)
    exportScreenshotsButton = WindowComponents.FullWidthButton("Export screenshots", button_exportScreenshots)
    deleteScreenshotsButton = WindowComponents.FullWidthButton("Delete screenshots", button_deleteScreenshots)

    WindowComponents.Base.app.grid_columnconfigure(1, weight=1)
    WindowComponents.Base.app.mainloop()