from .BaseSetting import BaseSetting, ctk, Base

class Button(BaseSetting):
    def __init__(self, title, _callback=lambda:0, _app=Base.app, _row=-1, _col=-1, _stick="ew"):
        super().__init__(None, _callback, _app, _row, _col)
        self.buttonText = title
        self.callback = _callback

        self.button = ctk.CTkButton(self.app, text=self.buttonText, fg_color="#565B5D", text_color=self.fontColor, hover_color="#343638", command=self.callback)
        self.button.grid(row=self.row, column=self.col, sticky=_stick, padx=self.xPadding, pady=self.yPadding)

    def setText(self, text):
        self.buttonText = text
        self.button.configure(text=text)
