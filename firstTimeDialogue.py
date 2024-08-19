import sys
sys.exit(8)
# will be made soon


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

pageAmt = len(pages)

def updateContent(window, page):
    cPage = pages[page]
    window["Title"].update(cPage["title"])
    window["Image"].update(sysInfo.getLocation(f"{sysInfo.fileLocation}/img/{cPage['image']}"))
    window["Description"].update(cPage["desc"])

    if page == pageAmt - 1:
        window["NextPage"].update("Finish")
    else:
        window["NextPage"].update("Next")
