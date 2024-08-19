from .WindowComponentBase import Base

ctk = Base.ctk
class BaseSetting:
    elements: list["BaseSetting"] = {}

    def __init__(self, title="Setting Title", _callback=lambda:0, app=Base.app, _row=-1, _col=-1):
        strApp = str(app)
        if not strApp in BaseSetting.elements:
            BaseSetting.elements[strApp] = []

        if _row == -1:
            _row = len(BaseSetting.elements[strApp])
        if _col == -1:
            _col = 0

        self.app = app
        self.title = title
        self.row = _row
        self.col = _col
        self.callback = _callback
        self.xPadding = 10
        self.yPadding = 5
        self.fontColor = Base.fontColor

        if self.title is not None:
            self.title = ctk.CTkLabel(master=self.app, text=self.title, font=(None, 14), text_color=self.fontColor)
            self.title.grid(row=self.row, column=self.col, pady=self.yPadding, padx=self.xPadding, sticky="w")

        BaseSetting.elements[strApp].append(self)

    @classmethod
    def getElements(cls):
        return BaseSetting.elements