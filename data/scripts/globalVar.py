from pygame import Surface, font
from data.scripts.UI.printInfo import printInfo

## Global Var
def init():
    global win_scale, image_dict, font_dict, mask_dict, win_width, win_height
    global dt, mouse_pos, run, RENDER_DISTANCE, audio

    ## Stores the value that items in
    ## the window should be scaled by.
    ## ----
    ## Value is set in UI.py
    win_scale = 1

    ## Stores all images
    ## ----
    ## Use this dict when using images
    ## to save memory
    ## ----
    ## Add new images using UI.addImage()
    image_dict = {}

    ## Font dict
    ## ----
    ## Stores all fonts
    font_dict = {}

    ## Stores masks of images in image dict
    ## ----
    ## Used for entities 
    mask_dict = {}

    ## window width & height
    ## ----
    ## The height and width of the UI window
    win_width = 1280
    win_height = 720

    ## Delta time
    ## ----
    ## dt multiplied with values to make
    ## them frame dependent
    ## ----
    ## Updated from within the UI class
    ## __setDeltaTime
    dt = 0

    ## Mouse Pos
    ## ----
    ## Stores the mouses position
    mouse_pos = (0, 0)

    ## Program Run
    ## ----
    ## Boolean value used to say if the
    ## program is still running
    run = True

    ## Render Distance
    ## ----
    ## Dictonary of values for render distances
    RENDER_DISTANCE = {"map": 64}

    ## audio
    ## ----
    ## stores and manages all audio
    audio = None 


def getRenderDistance(category_name) -> int:

    """Returns the render distance value of a category

    Returns:
        int: render distance value
    """

    return RENDER_DISTANCE[category_name]



## Checks whether image is in dict
def isImage(image_name: str) -> bool:

    """Returns whether image is in image dict

    Returns:
        bool: image in image dict
    """

    return image_name in image_dict


## Returns image
def getImage(image_name: str) -> Surface:

    """Returns image surface from an image name. If the image hasn't been loaded
    it will return an error image surface.

    Returns:
        Surface: image
    """

    if isImage(image_name):
        return image_dict[image_name]
    else:
        return image_dict["error"]


def isFont(font_name: str) -> bool:

    """Returns whether the font exists

    Returns:
        bool: font exists
    """
    
    return font_name in font_dict

def getFont(font_name: str):

    """Returns font

    Raises:
        Exception: font doesn't exist

    Returns:
        font: font
    """

    if isFont(font_name):
        return font_dict[font_name]
    
    elif font_name in font.get_fonts():
        return font_name

    else:
        printInfo("Error", f"'{font_name}' font doesn't exist")
        return font.get_fonts()[0]


## Checks whether mask is in dict
def isMask(image_name: str) -> bool:

    """Returns whether image mask exists

    Returns:
        bool: mask in image mask dict
    """

    if image_name in mask_dict:
        return True
    else:
        printInfo("Error", f"'{image_name}' mask doesn't exist")


def getMask(image_name: str):

    """Returns image mask

    Returns:
        Mask: image mask
    """

    if isMask(image_name):
        return mask_dict[image_name]