from .BaseSetting import BaseSetting, ctk, Base

class Checkbox(BaseSetting):
    def __init__(self, title, checked, checkOnText, checkOffText, callback=lambda x:x, _app=Base.app, _row=-1, _col=-1):
        super().__init__(title, callback, _app, _row, _col)
        self.checked = checked
        self.checkOnText = checkOnText
        self.checkOffText = checkOffText

        def callback():
            val = self.getToggled()
            text = "Enabled" if val else "Disabled"
            self.checkBox.configure(text=text)
            self.callback(val)

        self.checkBox = ctk.CTkSwitch(
                                        master=self.app, 
                                        text=self.checkOffText, 
                                        command=callback, 
                                        text_color=self.fontColor
                                    )

        if checked:
            self.checkBox.select()
            callback()

        self.checkBox.grid(row=self.row, pady=self.yPadding, column=self.col + 2, sticky="e")
    
    def getToggled(self) -> bool:
        return bool(self.checkBox.get())

    def setText(self, text):
        self.checkBox.configure(text=text)