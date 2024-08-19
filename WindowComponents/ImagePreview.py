import imageModifier
import io
from .BaseSetting import BaseSetting, ctk
from .WindowComponentBase import Base
from PIL import Image, ImageTk

class ImagePreview(BaseSetting):
    def __init__(self, image=None, size=(0,0), onImageRender=lambda:0, app=Base.app, _row=-1, _col=-1):
        super().__init__(None, onImageRender, app, _row, _col)

        self.image = image
        self.size = size
        app.grid_rowconfigure(self.row, weight=1)
        app.grid_columnconfigure(self.col, weight=1)
        frame = ctk.CTkFrame(app)
        frame.grid(row=self.row, column=self.col, sticky="nsew", columnspan=5)

        self.label = ctk.CTkLabel(frame, text="")
        self.label.grid(row=0, column=0, sticky="nsew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
    
    def renderImageFromBin(self, bin):
        targetSize = Base.getElementSize(self.label)
        if targetSize[0] < 100 or targetSize[1] < 100:
            return
            
        imageBin, imageSize = imageModifier.resizeImage(bin, targetSize, Base.screenSize, targetSize)
        pilImage = Image.open(io.BytesIO(imageBin))
        image = ctk.CTkImage(dark_image=pilImage, light_image=pilImage, size=imageSize)

        self.image = image
        self.label.configure(image=self.image)

        self.callback()