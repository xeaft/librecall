import sys
import WindowComponents
from SystemInfo import SystemInfo
from WindowComponents.WindowComponentBase import Base

pages = [
    {
        "title": "Welcome to librecall",
        "image": "settingsUI.png",
        "desc": "This window will guide you through the use of librecall.\nYou can skip this at any time."
    },
    {
        "title": "How it works",
        "image": "timeSetting.png",
        "desc": "Every X minutes, librecall takes a picture of your screen and stores it in a\ndatabase on your device. The frequency of screenshots can be modified in the\nsettings"
    },
    {
        "title": "The settings",
        "image": "settingsUI.png",
        "desc": "The settings page has a lot of options that you can configure. Upon running again,\nlibrecall will start its screenshotting process. To open the settings menu again, run\nlibrecall with the \"-c\" flag"
    },
    {
        "title": "Viewing your timeline",
        "image": "timeline.png",
        "desc": "What would be the point of a recall tool without the ability to view your timeline.\nSo, in order to view your timeline, you can simply press the \"View timeline\"\nbutton on the bottom of the settings."
    },
    {
        "title": "Delete the history",
        "image": "deleteScreenshots.png",
        "desc": "Sometimes, you might want to delete the history. Librecall makes it very simple to\ndo so - you can just click on the \"Delete screenshots\" button."
    },
    {
        "title": "Share your moments",
        "image": "extractScreenshots.png",
        "desc": "Would your friends be interested in a specific part of your history, or do you just\nwant to externally save your images? Do not worry, the big \"Export screenhots\"\nbutton allows you to do exactly that! It exports all your screenshots and saves\nthem into a sub-folder in the main directory."
    }
]

pageAmt = len(pages)
sysInfo = SystemInfo()

def updateContent(window, page, isNext=False):
    if window["nextPage"].buttonText == "Finish" and isNext:
        return True

    cPage = pages[page]
    window["title"].setText(cPage["title"])
    window["image"].renderImage(sysInfo.getLocation(f"{sysInfo.fileLocation}/img/{cPage['image']}"))
    window["desc"].setText(cPage["desc"])

    if page == pageAmt - 1:
        window["nextPage"].setText("Finish")
    else:
        window["nextPage"].setText("Next")
    if page == 0:
        window["prevPage"].button.configure(state="disabled")
    else:
        window["prevPage"].button.configure(state="normal")

def handleFirstPageLoad(window):
    succ = True
    try:
        updateContent(window, 0)
    except ValueError:
        succ = False

    if succ:
        return

    Base.app.after(50, handleFirstPageLoad, window)

page = 0
font = None
returnFlag = "quit"

def doUI():
    global font
    things = {}

    Base.app = Base.ctk.CTk()
    Base.app.geometry("650x450")
    Base.app.title("Librecall")
    Base.app.resizable(False, False)
    WindowComponents.Base.screenSize = (WindowComponents.Base.app.winfo_screenwidth(), WindowComponents.Base.app.winfo_screenheight())

    def nextPage():
        global page, returnFlag
        page += 1
        returnVal = updateContent(things, page, True) 
        if returnVal:
            returnFlag = "finish"
            Base.app.quit()
            Base.app.destroy()
            Base.app = None

    def prevPage():
        global page
        page -= 1
        updateContent(things, page)
    
    def skip():
        global returnFlag
        returnFlag = "finish"
        Base.app.quit()
        Base.app.destroy()
        Base.app = None

    blankSpace = WindowComponents.TextLabel("", _app=Base.app)
    blankSpace.label.configure(font=(None, 2))
    Base.app.grid_rowconfigure(0, pad=5)
    font = Base.ctk.CTkFont(None, 16)

    things["title"] = WindowComponents.TextLabel("Librecall Welcome (placeholder page)", align="center")
    things["title"].label.configure(font=(None, 18))

    things["image"] = WindowComponents.ImagePreview(app=Base.app)

    things["desc"] = WindowComponents.TextLabel("(if you actually see this, click \"next\", and then \"previous\"...)", _row=2)

    things["nextPage"] = WindowComponents.Button("Next", nextPage, _row=5, _col=3, _stick="e")
    things["skip"] = WindowComponents.Button("Skip", skip, _row=5, _stick="w")
    
    things["prevPage"] = WindowComponents.Button("Previous", prevPage, _row=5, _col=1, _stick="e")

    Base.app.after(50, handleFirstPageLoad, things)
    Base.app.mainloop()
    return returnFlag
