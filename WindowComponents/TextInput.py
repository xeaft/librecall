from .BaseSetting import BaseSetting, Base, ctk
import re

class TextInput(BaseSetting):
    def __init__(self, title, value, _callback=lambda x:x, _regex="", _app=Base.app, _row=-1, _col=-1):
        super().__init__(title, _callback, _app, _row, _col=_col)

        self.textbox = ctk.CTkTextbox(self.app, wrap="none", height=10, width=250, text_color=self.fontColor)
        self.textbox.insert("0.0", value)
        self.callback = _callback

        def preventNewline(ev):
            return "break"

        def filterTexbox(event, autofix=True, first=False):
            if not _regex:
                return self.callback(self.get())

            thing = self.get().replace("\n", "")
            matches = re.findall(_regex, thing)
            newText = ''.join(matches)
            if newText == thing:
                self.textbox.configure(text_color=self.fontColor)
            else:
                if not autofix:
                    self.textbox.configure(text_color="#ff0000")
                else:
                    self.clear()
                    self.textbox.insert("0.0", newText)

            self.callback(self.get().replace("\n", ""))
        
        # fix a newline bug
        val = self.get()
        newLineIndex = val.find("\n")
        if newLineIndex:
            self.clear()
            self.textbox.insert("0.0", val[:newLineIndex])

        filterTexbox(None, False, True)

        self.textbox.bind("<KeyRelease>", filterTexbox)
        self.textbox.bind("<Return>", preventNewline)

        self.textbox.grid(row=self.row, column=self.col + 2, padx=self.xPadding, pady=self.yPadding, sticky="e")

    def get(self) -> str:
        return self.textbox.get("0.0", "end")

    def clear(self):
        self.textbox.delete("0.0", "end")