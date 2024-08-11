import PySimpleGUI as sg
import stuff

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
    [sg.Text("")],
    [sg.Push(), sg.Text("Welcome to librecall", key="Title", font=("Helvetica", 18)), sg.Push()],
    [sg.Text("")],
    [sg.Image(stuff.getLocation(f"{stuff.fileLocation}/img/settingsUI.png"), key="Image", expand_x=True, expand_y=True)],
    [sg.Text("")],
    [sg.Text("This window will guide you through the use of librecall. You can skip this at any time.", size=(64, None), key="Description", font=("Helvetica", 12)) ],
    [sg.Text("")],
    [sg.Button("Skip", key="SkipIntro"), sg.Push(), sg.Button("Previous", key="PreviousPage"), sg.Button("Next", key="NextPage")]
]

def getDistro():
    try:
        with open('/etc/os-release') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('NAME='):
                return line.split('=')[1].strip().strip('"')
    except FileNotFoundError:
        return None


pages = [
    {
        "title": "Welcome to librecall",
        "image": "settingsUI.png",
        "desc": "This window will guide you through the use of librecall. You can skip this at any time."
    },
    {
        "title": "How it works",
        "image": "timeSetting.png",
        "desc": "Every X milliseconds, librecall takes a picture of your screen and stores it in a database on your device. The frequency of screenshots can be modified in the settings"
    },
    {
        "title": "The settings",
        "image": "settingsUI.png",
        "desc": "The settings page has a lot of options that you can configure. Upon running again, librecall will start its screenshotting process. To open the settings menu again, run librecall with the \"-c\" flag"
    },
    {
        "title": "Viewing your timeline",
        "image": "timeline.png",
        "desc": "What would be the point of a recall tool without the ability to view your timeline. So, in order to view your timeline, you can simply press the \"View timeline\" button on the bottom of the settings."
    },
    {
        "title": "Delete the history",
        "image": "deleteScreenshots.png",
        "desc": "Sometimes, you might want to delete the history. Librecall makes it very simple to do so - you can just click on the \"Delete screenshots\" button. It's even spaced out a little bit to make it easy to find, and not press on accident."
    },
    {
        "title": "Share your moments",
        "image": "extractScreenshots.png",
        "desc": "Would your friends be interested in a specific part of your history, or do you just want to externally save your images? Do not worry, the big \"Extract screenhots\" button allows you to do exactly that! It extracts all your screenshots and saves them into a sub-folder in the main directory."
    },
]

if stuff.usedOS == "linux":
    distro = getDistro()
    addText = " Unfortunately not the exact distribution."
    if distro:
        addText = f" Specifically, {distro}."

    if stuff.usingSystemd:
        page = {
            "title": "Auto start",
            "image": "tux.png",
            "desc": f"Librecall has detected that you are on (GNU+)Linux.{addText} Also, you are using the systemd init system. For systemd, librecall offers a service that allows you to automatically run librecall on user login. If you would like to use that, run the \"autorun.py\" script in the same directrory."
        }
        pages.append(page)
        
pageAmt = len(pages)

def updateContent(window, page):
    cPage = pages[page]
    window["Title"].update(cPage["title"])
    window["Image"].update(stuff.getLocation(f"{stuff.fileLocation}/img/{cPage['image']}"))
    window["Description"].update(cPage["desc"])

    if page == pageAmt - 1:
        window["NextPage"].update("Finish")
    else:
        window["NextPage"].update("Next")


def doUI():
    global currentImageLoc

    page = 0
    window = sg.Window("LibreCall - First time use", layout, resizable=True)
    window.refresh()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return "Closed"

        elif event == "NextPage":
            if page < pageAmt - 1:
                page += 1
                updateContent(window, page)
            else:
                window.close()
                break

        elif event == "PreviousPage":
            if page > 0:
                page -= 1
                updateContent(window, page)
        
        elif event == "SkipIntro":
            window.close()
            break