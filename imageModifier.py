from PIL import Image
import io

def getAspectRatio(dimensions):
    width, height = dimensions
    return width / height

def adjustAspectRatio(dimensions, targetAspectRatio, limits):
    originalWidth, originalHeight = dimensions
    maxWidth, maxHeight = limits
    
    currentAspectRatio = originalWidth / originalHeight
    
    if currentAspectRatio < targetAspectRatio:
        newWidth = originalHeight * targetAspectRatio
        newWidth = min(newWidth, maxWidth)
        newHeight = newWidth / targetAspectRatio
    else:
        newHeight = originalWidth / targetAspectRatio
        newHeight = min(newHeight, maxHeight)
        newWidth = newHeight * targetAspectRatio
    
    return (int(newWidth), int(newHeight))

def resizeImagePost(imageBin, targetSize: tuple[int, int]):
    image_stream = io.BytesIO(imageBin)
    image = Image.open(image_stream)
    
    resizedImage = image.resize(targetSize)
    resizedImage_stream = io.BytesIO()
    resizedImage.save(resizedImage_stream, format='PNG')
    resizedImageBin = resizedImage_stream.getvalue()
    
    return resizedImageBin, targetSize


def resizeImage(imageBin, targetSize, screenSize, limit):
    aspectRatio = getAspectRatio(screenSize)
    targetSize = adjustAspectRatio(targetSize, aspectRatio, limit)
    return resizeImagePost(imageBin, targetSize)