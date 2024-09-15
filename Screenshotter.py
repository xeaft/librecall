import os
import random
import screenshotters
import sys
import traceback
from PIL import ImageGrab
from SystemInfo import SystemInfo
from ConfigManager import ConfigManager


class Screenshotter:
    _insts = []

    def __new__(cls):
        if Screenshotter._insts:
            return Screenshotter._insts[0]

        screenshotter = super().__new__(cls)
        Screenshotter._insts.append(screenshotter)

        screenshotter.sysInfo = SystemInfo()
        screenshotter.configManager = ConfigManager()
        screenshotter.tool = screenshotter.configManager.get("SCREENSHOT_TOOL")

        return screenshotter

    def handleWaylandScreenshot(self):
        try:
            return self.getCustomToolScreenshot()
        except Exception as e:
            if not self.sysInfo.info:
                print(
                    "Falied to take a screenshot. This might be an issue with your compositor/screenshotting tool")
            else:
                print("Failed to take a screenshot")
                print(f"Screenshotting tool: {self.tool}")
                print(f"Exception: {e}, {type(e)}")
                with open(f"{self.sysInfo.dataDir}/.wayland_fail.log", "w") as f:
                    f.write(traceback.format_exc())

    def getCustomToolScreenshot(self):
        return screenshotters.tools[self.tool]()

    def getPILScreenshotBin(self):
        screenshot = ImageGrab.grab()
        rawPath = f"{self.sysInfo.tmpPath}/{self.sysInfo.getTimeMS()}_image{random.randint(0, 100)}.png"
        path = self.sysInfo.getLocation(rawPath)
        screenshot.save(path)

        imgBin = None

        try:
            with open(path, "rb") as img:
                imgBin = img.read()
        finally:
            os.remove(path)

        return imgBin

    def getScreenshotBinary(self):
        screenshotBin = None
        if self.sysInfo.isWayland:
            screenshotBin = self.handleWaylandScreenshot()
        else:
            if self.configManager.get("SCREENSHOT_TOOL").lower() == "default":
                screenshotBin = self.getPILScreenshotBin()
            else:
                screenshotBin = self.getCustomToolScreenshot()

        if not screenshotBin:
            if self.sysInfo.info:
                print("Failed to take a screenshot")
            return None

        with open(self.sysInfo.infoFile, "w") as file:
            file.write(str(self.sysInfo.getTimeMS()))

        return screenshotBin

    def getScreenshot(self) -> bytes:
        if self.tool == "N/A" or (not screenshotters.availableTools and self.sysInfo.isWayland):
            print("""
\t\tWayland doesnt support PIL's default ImageGrab.grab() method, and you do
\t\tnot have any screenshotting tools compatible with librecall. Please refer
\t\tto the README or use the "--wayland-tools" flag and download a tool that
\t\tworks on your compositor.
            """)
            sys.exit(5)

        return self.getScreenshotBinary()
