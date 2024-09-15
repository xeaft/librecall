from .BaseSetting import BaseSetting, ctk, Base
from .Notification import Notification

class Dropdown(BaseSetting):
    def __init__(self, title, options, _defaultOption=None, _callback=lambda x:x, _app=Base.app, _row=-1, _col=-1):
        super().__init__(title, _callback, _app, _row, _col)

        self.options = options

        if not _defaultOption or _defaultOption not in self.options:
            if len(options):
                _defaultOption = options[0]
            else:
                Notification("Error", "No screenshotting tool available")

        self.defaultOption = _defaultOption
        
        self.dropdown = ctk.CTkComboBox(master=self.app, values=self.options, command=self.callback, state="readonly", width=250, text_color=self.fontColor)
        self.dropdown.grid(row=self.row, pady=self.yPadding, padx=self.xPadding, column=self.col + 2, sticky="e")

        self.dropdown.set(self.defaultOption)
    
    def getOption(self):
        return self.dropdown.get()
