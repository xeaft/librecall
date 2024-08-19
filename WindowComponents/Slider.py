from .BaseSetting import BaseSetting, ctk, Base

class Slider(BaseSetting):
    def __init__(self, title, value, minValue, maxValue, _intOnly=True, _callback=lambda x:x, _app=Base.app, _row=-1, _col=-1):
        super().__init__(title, _callback, _app, _row, _col)
        
        self.value = value
        self.min = minValue
        self.max = maxValue
        self.intOnly = _intOnly

        def _callback(value):
            if self.intOnly:
                value = round(value)

            self.valueText.configure(text=str(value))
            self.callback(value)

        self._callback = _callback
        
        self.valueText = ctk.CTkLabel(master=self.app, text=str(value), text_color=self.fontColor)
        self.valueText.grid(row=self.row, pady=self.yPadding, padx=self.xPadding, column=self.col + 1, sticky="e")

        self.slider = ctk.CTkSlider(master=self.app, from_=self.min, to=self.max, command=self._callback, height=20, width=250)
        self.slider.grid(row=self.row, pady=self.yPadding, padx=self.xPadding, column=self.col + 2, sticky="e")

        if self.max - self.min == 0:
            self.slider.configure(state="disabled")
            self.valueText.configure(text=f"{self.min} (only value)")
        else:
            self.slider.set(value)

    def getValue(self):
        val = self.slider.get()
        if self.intOnly:
            val = round(val)
        return val