from .BaseSetting import BaseSetting, ctk, Base

class FullWidthButton(BaseSetting):
    def __init__(self, title, _callback=lambda:0, _app=Base.app, _row=-1, _col=-1):
        super().__init__(None, _callback, _app, _row, _col)
        self.buttonText = title
        self.callback = _callback

        self.button = ctk.CTkButton(self.app, text=self.buttonText, fg_color="#565B5D", text_color=self.fontColor, hover_color="#343638", command=self.callback)
        self.button.grid(row=self.row, column=0, columnspan=3, sticky="ew", padx=self.xPadding, pady=self.yPadding)
