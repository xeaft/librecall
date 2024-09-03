from .WindowComponentBase import ctk, Base


class Notification:
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.toplevel = ctk.CTkToplevel()
        self.toplevel.geometry("300x150")
        self.toplevel.resizable(False, False)

        titleLabel = ctk.CTkTextbox(self.toplevel, font=(
            None, 18), text_color=Base.fontColor)
        textLabel = ctk.CTkTextbox(self.toplevel, font=(
            None, 14), text_color=Base.fontColor)

        titleLabel.insert("0.0", title)
        textLabel.insert("0.0", text)

        titleLabel.configure(wrap="word", state="disabled",
                             width=290, height=40, fg_color="transparent")
        textLabel.configure(wrap="word", state="disabled",
                            width=290, height=70, fg_color="transparent")

        titleLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        textLabel.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.toplevel.focus()
