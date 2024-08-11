import PySimpleGUI as sg
import screenshotDB
import config
import time
import imageModifier

config.loadConfig()
screenshotDB.makeConnection()
images = screenshotDB.getImages()
screenshotDB.end()
imageCount = len(images)
screenSize = sg.Window.get_screen_size()
screenAR = imageModifier.getAspectRatio(screenSize)

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
    [sg.Slider((0, imageCount - 1), orientation="h", disable_number_display=True, key="Timeline_Slider", enable_events=True, default_value=0, expand_x=True)],
    [sg.Image(key="Image", expand_x=True, expand_y=True)]
]


def getElementSize(element):
    tkWidget = element.Widget
    return tkWidget.winfo_width(), tkWidget.winfo_height()

def renderImage(window, image):
    targetSize = getElementSize(window["Image"])
    origImageBin = images[image]["bin"]
    imageBin = imageModifier.resizeImage(origImageBin, targetSize, screenSize, targetSize)
    window["Image"].update(data=imageBin)

def doUI():
    global currentImageLoc

    screenshotDB.makeConnection()
    images = screenshotDB.getImages()
    screenshotDB.end()
    imageCount = len(images)
    framesSinceResize = 0

    if imageCount == 0:
        return
    
    windowSize = (screenSize[0] // 2, screenSize[1] // 2)
    window = sg.Window("LibreCall - Timeline", layout, size=windowSize, resizable=True, finalize=True)
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
            if framesSinceResize == 5:
                sliderValue = int(values["Timeline_Slider"])
                renderImage(window, int(sliderValue))
                framesSinceResize = 0

        if event == "Event":
            if window.size != windowSize:
                window.Size = imageModifier.adjustAspectRatio(window.size, screenAR, screenSize)
                windowSize = window.size
                sliderValue = int(values["Timeline_Slider"])
                renderImage(window, int(sliderValue))
                framesSinceResize = 1

        if event == "Timeline_Slider":
            if eventValue:
                renderImage(window, int(eventValue))