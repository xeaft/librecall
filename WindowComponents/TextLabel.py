from .BaseSetting import BaseSetting, ctk, Base

class TextLabel(BaseSetting):
    def __init__(self, text, _app=Base.app, _row=-1, _col=0, align="left", _rowspan=1, _maxcol=3):
        stick = "w"
        if align == "right":
            _col = _maxcol
            stick = "e"
        elif align == "center":
            stick = "ew"

        columnspan = 4
        super().__init__(None, lambda:0, _app, _row, _col)

        if align == "center":
            self.xPadding = 0
            self.yPadding = 0

        self.text = text
        self.label = ctk.CTkLabel(master=self.app, text=self.text, text_color=self.fontColor, font=(None, 16), height=0, justify="left")
        self.label.grid(row=self.row, pady=self.yPadding, padx=self.xPadding, column=self.col, sticky=stick, columnspan=columnspan, rowspan=_rowspan)

    def setText(self, newText):
        self.text = newText
        self.label.configure(text=newText)