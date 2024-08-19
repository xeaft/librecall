import datetime
import imageModifier
import WindowComponents
from copy import deepcopy
from ConfigManager import ConfigManager
from DatabaseHandler import DatabaseHandler
from SystemInfo import SystemInfo

images = []
imageRenderer = None
lastResizeTimeMS = SystemInfo.getTimeMS()
datetimeText = None
oldSliderVal = 0

def getDate(ms, format):
    seconds = ms / 1000 
    date = datetime.datetime.fromtimestamp(seconds)
    return date.strftime(format)


def getElementSize(widget):
    return widget.winfo_width(), widget.winfo_height()

def resizeWindow(width, height):
    WindowComponents.Base.timeline.geometry(f"{width}x{height}")
    WindowComponents.Base.timelineWidth = width
    WindowComponents.Base.timelineHeight = height

def handleResize(event):
    global lastResizeTimeMS

    width = event.width
    height = event.height

    def render():
        newWidth = WindowComponents.Base.timeline.winfo_width()
        newHeight = WindowComponents.Base.timeline.winfo_height()

        if newWidth == width and newHeight == height and imageRenderer:
            imageRenderer.renderImageFromBin(images[WindowComponents.Base.timelineCurrentImage]["bin"])


    if width != WindowComponents.Base.timelineWidth or height != WindowComponents.Base.timelineHeight:
        WindowComponents.Base.timelineWidth = width
        WindowComponents.Base.timelineHeight = height
        WindowComponents.Base.timeline.after(75, render)

def createToplevel():
    WindowComponents.Base.timelineWidth = WindowComponents.Base.screenSize[0] // 2
    WindowComponents.Base.timelineHeight = WindowComponents.Base.screenSize[1] // 2

    WindowComponents.Base.timeline = WindowComponents.Base.ctk.CTkToplevel()
    WindowComponents.Base.timeline.title("Librecall - Timeline")

    WindowComponents.Base.timeline.geometry(f"{WindowComponents.Base.timelineWidth}x{WindowComponents.Base.timelineHeight}")
    WindowComponents.Base.timeline.focus()

    WindowComponents.Base.timeline.bind("<Configure>", handleResize)

def onImageRender():
    image = images[WindowComponents.Base.timelineCurrentImage]
    datetimeFormat = ConfigManager().get("DATE_FORMAT")
    time = int(image["date"])

    if datetimeText:
        datetimeText.setText(getDate(time, datetimeFormat))

def handleSlider(val):
    oldimg = WindowComponents.Base.timelineCurrentImage
    WindowComponents.Base.timelineCurrentImage = val
    if oldimg != val:
        imageRenderer.renderImageFromBin(images[WindowComponents.Base.timelineCurrentImage]["bin"])

def createTimelineWindow():
    global images, imageRenderer, datetimeText
    if WindowComponents.Base.timeline and WindowComponents.Base.timeline.winfo_exists():
        return

    configManager = ConfigManager()
    dbHandler = DatabaseHandler()
    sysInfo = SystemInfo()

    dbHandler.makeConnection()
    images = dbHandler.getImages()
    dbHandler.endConnection()

    imageCount = len(images)

    if not imageCount:
        WindowComponents.Notification("No images", "You don't have any screenshots stored that can be viewed here.")
        return

    createToplevel()
    screenAR = imageModifier.getAspectRatio(WindowComponents.Base.screenSize)

    toplevel = WindowComponents.Base.timeline
    ctk = WindowComponents.Base.ctk

    blankSpace = WindowComponents.TextLabel("", _app=toplevel)
    blankSpace.label.configure(font=(None, 2))
    toplevel.grid_rowconfigure(0, pad=1)

    titleText = WindowComponents.TextLabel("Timeline", _app=toplevel, align="center")
    titleText.label.configure(font=(None, 18))

    datetimeText = WindowComponents.TextLabel("datetime", _app=toplevel, align="center")
    datetimeText.label.configure(font=(None,  14))

    slider = WindowComponents.Slider("Image", 0, 0, imageCount - 1, _app=toplevel, _callback=handleSlider)

    imageRenderer = WindowComponents.ImagePreview(app=toplevel, onImageRender=onImageRender)
    
    def deleteImage():
        global imageCount, images

        dbHandler.makeConnection()
        sliderVal = slider.getValue()
        
        imageID = images[sliderVal]["id"]
        dbHandler.deleteImage(imageID)
        images = dbHandler.getImages()
        imageCount = len(images)

        if not imageCount:
            toplevel.destroy()
        elif imageCount == 1:
            slider.slider.configure(state="disabled")
            slider.valueText.configure(text="0 (only value)")
        else:
            slider.slider.configure(from_=0, to=imageCount - 1)

        if sliderVal >= imageCount and imageCount:
            slider.slider.set(imageCount - 1)
            slider._callback(imageCount - 1)
        else:
            if imageCount:
                imageRenderer.renderImageFromBin(images[sliderVal]["bin"])

        dbHandler.endConnection()

    deleteImageButton = WindowComponents.FullWidthButton("Delete this image", deleteImage, _app=toplevel)
