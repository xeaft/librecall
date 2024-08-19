import customtkinter as ctk

class Base:
    app: ctk.CTk = None
    timeline: ctk.CTkToplevel = None
    ctk = ctk
    fontColor: tuple[str, str] = "#333333", "#cccccc"
    screenSize = 0,0
    timelineHeight = 0
    timelineWidth = 0
    timelineCurrentImage = 0

    @staticmethod
    def getElementSize(widget):
        return widget.winfo_width(), widget.winfo_height()