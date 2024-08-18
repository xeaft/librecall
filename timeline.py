import datetime
import imageModifier
import PySimpleGUI as sg
from DatabaseHandler import DatabaseHandler
from copy import deepcopy
from ConfigManager import ConfigManager
from SystemInfo import SystemInfo

def doUI():
    configManager = ConfigManager()
    dbHandler = DatabaseHandler()
    sysInfo = SystemInfo()

    dbHandler.makeConnection()
    images = dbHandler.getImages()
    dbHandler.endConnection()
    imageCount = len(images)
    screenSize = sg.Window.get_screen_size()
    screenAR = imageModifier.getAspectRatio(screenSize)
    dateTimeForamt = configManager.get("DATE_FORMAT")

    def getDate(ms, format):
        seconds = ms / 1000 
        date = datetime.datetime.fromtimestamp(seconds)
        return date.strftime(format)


    def getElementSize(element):
        tkWidget = element.Widget
        return tkWidget.winfo_width(), tkWidget.winfo_height()

    def renderImage(window, image):
        targetSize = getElementSize(window["Image"])
        origImageBin = images[image]["bin"]
        imageBin = imageModifier.resizeImage(origImageBin, targetSize, screenSize, targetSize)
        window["Image"].update(data=imageBin)
        imgDate = int(images[image]["date"])
        window["ImageDate"].update(getDate(imgDate, dateTimeForamt))

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
        [sg.Push(), sg.Text("Timeline", key="Timeline_Text"), sg.Push()],
        [sg.Push(), sg.Text("test", key="ImageDate"), sg.Push()],
        [sg.Text(f"1/{imageCount}", key="Image_Index"), sg.Slider(range=(0, imageCount - 1), orientation="h", disable_number_display=True, key="Timeline_Slider", enable_events=True, default_value=0, expand_x=True), sg.Button("Delete Image", key="Delete_Image")],
        [sg.Image(key="Image", expand_x=True, expand_y=True)]
    ]

    imageCount = len(images)
    framesSinceResize = 0

    if imageCount == 0:
        return
    
    dateTimeForamt = configManager.get("DATE_FORMAT")
    windowSize = (screenSize[0] // 2, screenSize[1] // 2)
    window = sg.Window("LibreCall - Timeline", deepcopy(layout), size=windowSize, icon=sysInfo.getLocation(f"{sysInfo.fileLocation}/img/icon_transparent.ico"), resizable=True, finalize=True)
    window.refresh()
    window.bind('<Configure>',"Event")
    renderImage(window, 0)

    while True:
        event, values = window.read()
        eventValue = values[event] if (values and event in values) else None
        if event == sg.WIN_CLOSED:
            break
        
        if framesSinceResize > 0:
            framesSinceResize += 1
            sliderValue = int(values["Timeline_Slider"])
            renderImage(window, int(sliderValue))
            if framesSinceResize == 5:
                framesSinceResize = 0

        if event == "Event":
            if window.size != windowSize:
                window.Size = imageModifier.adjustAspectRatio(window.size, screenAR, screenSize)
                windowSize = window.size
                sliderValue = int(values["Timeline_Slider"])
                renderImage(window, int(sliderValue))
                framesSinceResize = 1

        elif event == "Timeline_Slider":
            if eventValue is not None:
                renderImage(window, int(eventValue))
                window["Image_Index"].update(f"{int(eventValue) + 1}/{imageCount}")
                print(eventValue)

        elif event == "Delete_Image":
            dbHandler.makeConnection()
            sliderVal = int(values["Timeline_Slider"])
            
            imageID = images[sliderVal]["id"]
            dbHandler.deleteImage(imageID)
            images = dbHandler.getImages()
            imageCount = len(images)

            if sliderVal >= len(images):
                window["Timeline_Slider"].update(value=imageCount - 1)
                renderImage(window, imageCount - 1)
                window["Image_Index"].update(f"{imageCount}/{imageCount}")
            else:
                renderImage(window, sliderVal)
                window["Image_Index"].update(f"{sliderVal + 1}/{imageCount}")

            window["Timeline_Slider"].update(range=(0, imageCount - 1))

            dbHandler.endConnection()
