from pygame import Surface, draw, SRCALPHA, transform, font as pyfont, Rect
from data.scripts.basic import setTimer, isTimer, getTime, timeElapsed
import data.scripts.globalVar as globalVar

## Sets the alpha for a surface
def setSurfaceAlpha(surf: Surface, alpha: int) -> Surface:

    """Sets a alpha on a surface

    Returns:
        Surface: alpha surface
    """

    if alpha < 255:
        surf.set_colorkey((0,0,100))
        surf.set_alpha(alpha)
    
    return surf


## Returns a surface to display text
def createText(text: str, font: str, colour: tuple, size: int) -> Surface:

    """Creates a surface with text on it 

    Returns:
        Surface: surface with text
    """

    if font in pyfont.get_fonts():
        fontFormat = pyfont.SysFont(font, size)
    else:
        fontFormat = pyfont.Font(f"{font}", size)

    message = fontFormat.render(text, True, colour)

    return message


## Creates a surface
def createSurface(dimensions: tuple, colour: tuple, alpha: int) -> Surface:

    """Creates a surface

    Returns:
        Surface: new surface
    """

    surfaceWidth = round(dimensions[0]* globalVar.win_scale)
    surfaceHeight = round(dimensions[1] * globalVar.win_scale)
    
    if colour == None:
        newSurface = Surface((surfaceWidth, surfaceHeight), SRCALPHA)

        newSurface = setSurfaceAlpha(newSurface, alpha)
    
    else:
        newSurface = Surface((surfaceWidth, surfaceHeight))

        newSurface = setSurfaceAlpha(newSurface, alpha)
        
        draw.rect(newSurface, colour, (0,0, surfaceWidth, surfaceHeight))

    return newSurface



## Superclass for UI Elements
class UIElement:

    """Superclass for a single UI Element
    """

    def __init__(self,
            pos: tuple, 
            dimensions: tuple, 
            alpha: int = 255, 
            centered: bool = True, 
            display: bool = True):
        
        self.pos = list(pos)
        self.dimensions = list(dimensions)

        self.setWinPos()
        
        self.alpha = alpha

        self.centered = centered
        self.display = display

    ## Sets x and y pos for menu on window
    def setWinPos(self):

        """Sets pos of menu on the window.
        """

        self.xWinPos = round(self.pos[0] * globalVar.win_scale)
        self.yWinPos = round(self.pos[1] * globalVar.win_scale)
        self.xWinPosCenter = round((self.pos[0] - self.dimensions[0] / 2) * globalVar.win_scale)
        self.yWinPosCenter = round((self.pos[1] - self.dimensions[1] / 2) * globalVar.win_scale)

    ## Draw UI Element on surface
    def draw(self, surf: Surface):

        """Draws UI Element on surface
        """

        if self.display:
            if self.centered == False:
                surf.blit(self.surface, (self.xWinPos, self.yWinPos))
            
            else:
                surf.blit(self.surface, (self.xWinPosCenter, self.yWinPosCenter))
    
    ## Resize UI Element
    def resize(self):

        """Resizes UI Element
        """

        self.setWinPos()
        self.setSurface()





## Button
class Button(UIElement):

    """Button UI Element
    """

    def __init__(self, 
            pos: tuple, 
            alpha: int = 255, 
            press: bool = False, 
            pressAudio: str = None, 
            hoverAudio: str = None, 
            centered: bool = True, 
            display: bool = True):
        
        super().__init__(pos, (0, 0), alpha, centered, display)

        self.press = press
        self.hover = False
        self.pressCounter = 0

        self.update = False

        self.setSurface()
        self.setState(self.press, self.hover)

        ## Used in UI class to say whether pressAudio should play
        self.pressAudioPlay = False
        self.hoverAudioPlay = False

        self.pressAudio = pressAudio
        self.hoverAudio = hoverAudio

    ## Sets surface for a type of button state
    def setButtonSurface(self, originalSurf: Surface, dimensions: tuple) -> Surface:

        """Sets surface for a type of button state

        Returns:
            Surface: button surface
        """

        newSurf = transform.scale(originalSurf, 
            (round(dimensions[0] * globalVar.win_scale), 
            round(dimensions[1] * globalVar.win_scale)))

        return setSurfaceAlpha(newSurf, self.alpha)
        
    ## Sets the surface
    def setSurface(self):

        """Sets the surface
        """

        ## Creating button surface states
        self.pressSurface = self.setButtonSurface(self.originalPressSurface, 
            (self.pressSurfaceWidth, self.pressSurfaceHeight))

        self.unpressSurface = self.setButtonSurface(self.originalUnpressSurface, 
            (self.unpressSurfaceWidth, self.unpressSurfaceHeight))

        self.hoverSurface = self.setButtonSurface(self.originalHoverSurface, 
            (self.hoverSurfaceWidth, self.hoverSurfaceHeight))

        ## Rect used for collision, based on unpress surface
        if self.centered:
            self.buttonRect = Rect(round((self.pos[0] - self.unpressSurfaceWidth/2) * globalVar.win_scale), 
                round((self.pos[1] - self.unpressSurfaceHeight/2) * globalVar.win_scale), 
                round(self.unpressSurfaceWidth * globalVar.win_scale), 
                round(self.unpressSurfaceHeight * globalVar.win_scale))
        else:
            self.buttonRect = Rect(self.xWinPos, self.yWinPos, 
                round(self.unpressSurfaceWidth * globalVar.win_scale), 
                round(self.unpressSurfaceHeight * globalVar.win_scale))


    ## Sets surface, width, height
    def setSurfaceWidthHeight(self, surf: Surface, dimensions: tuple):
            self.surface = surf
            self.dimensions = dimensions
            self.setWinPos()

    ## Resize the the button
    def resize(self):

        """Resizes the button
        """

        self.setWinPos()
        self.setSurface()

        ## Redraws the button depending on state
        if self.press:
            self.setSurfaceWidthHeight(self.pressSurface, (self.pressSurfaceWidth, self.pressSurfaceHeight))
        elif self.hover:
            self.setSurfaceWidthHeight(self.hoverSurface, (self.hoverSurfaceWidth, self.hoverSurfaceHeight))
        else:
            self.setSurfaceWidthHeight(self.unpressSurface, (self.unpressSurfaceWidth, self.unpressSurfaceHeight))


    ## Sets the button state
    def setState(self, press: bool, hover: bool = False):

        """Sets the button state
        """

        self.pressAudioPlay = False
        self.hoverAudioPlay = False
        
        if self.press == False and press == True:
            self.setSurfaceWidthHeight(self.pressSurface, (self.pressSurfaceWidth, self.pressSurfaceHeight))
            self.update = True
            
            self.pressAudioPlay = True

        elif self.hover == False and hover == True: 
            self.setSurfaceWidthHeight(self.hoverSurface, (self.hoverSurfaceWidth, self.hoverSurfaceHeight))
            self.update = True
            
            if self.press == False: # Makes sure hover audio doesn't play after letting go of button
                self.hoverAudioPlay = True

        elif (self.press == True or self.hover == True) and press == False and hover == False:
            self.setSurfaceWidthHeight(self.unpressSurface, (self.unpressSurfaceWidth, self.unpressSurfaceHeight))
            self.update = True

        self.press = press
        self.hover = hover
    
    ## Check collision with mouse
    def isCollision(self, mousePos: tuple) -> bool:

        """Returns whether there is a collision with the mouse

        Returns:
            bool: collision with mouse
        """

        return self.buttonRect.collidepoint(mousePos)

    ## Check button press
    def isPress(self, mousePos: tuple, mouseClick: bool):

        """Returns whether the button has been pressed

        Returns:
            bool: button pressed
        """

        self.update = False

        if mouseClick:
            if self.isCollision(mousePos):
                self.setState(True)

        else:
            if self.isCollision(mousePos):
                self.setState(False, True)
            else:
                self.setState(False)

        return self.press


class ButtonText(Button):

    """Button using text surfaces
    """

    def __init__(self, 
        pos: tuple, 
        pressText: str, 
        unpressText: str, 
        hoverText: str = None, 
        pressSize: int = 1,
        unpressSize: int = 1, 
        hoverSize: int = 1, 
        pressColour: tuple = (0, 0, 0), 
        unpressColour: tuple = (0, 0, 0), 
        hoverColour: tuple = (0, 0, 0), 
        font: str = "verdana",
        alpha: int = 255, 
        press: bool = False, 
        pressAudio: str = None, 
        hoverAudio: str = None, 
        centered: bool = True, 
        display: bool = True):

                
        self.pressText = pressText
        self.pressSize = pressSize
        self.pressColour = pressColour

        self.unpressText = unpressText
        self.unpressSize = unpressSize
        self.unpressColour = unpressColour

        self.hoverText = hoverText
        self.hoverSize = hoverSize
        self.hoverColour = hoverColour

        self.font = font

        super().__init__(pos, alpha, 
                    press, 
                    pressAudio, hoverAudio, 
                    centered, display)

        self.setSurfaceWidthHeight(
            self.unpressSurface, 
            (self.unpressSurface.get_width(), self.unpressSurface.get_height()))

        self.resize()

    ## Sets the surface
    def setSurface(self):

        """Sets the surface
        """

        ## Creating button surface states
        self.pressSurface = createText(self.pressText, self.font, self.pressColour, 
                                        round(self.pressSize * globalVar.win_scale))

        self.unpressSurface = createText(self.unpressText, self.font, self.unpressColour, 
                                        round(self.unpressSize * globalVar.win_scale))

        self.hoverSurface = createText(self.hoverText, self.font, self.hoverColour, 
                                        round(self.hoverSize * globalVar.win_scale))


    ## Sets x and y pos for button on window
    def setWinPos(self):

        """Sets pos for button on window
        """

        self.xWinPos = round(self.pos[0] * globalVar.win_scale)
        self.yWinPos = round(self.pos[1] * globalVar.win_scale)
        self.xWinPosCenter = round(self.pos[0] * globalVar.win_scale) - self.dimensions[0]/2
        self.yWinPosCenter = round(self.pos[1] * globalVar.win_scale) - self.dimensions[1]/2


    ## Resize the the button
    def resize(self):

        """Resizes button
        """

        self.setSurface()

        ## Redraws the button depending on state
        if self.press:
            self.setSurfaceWidthHeight(
                self.pressSurface, 
                (self.pressSurface.get_width(), 
                self.pressSurface.get_height()))
        
        elif self.hover:
            self.setSurfaceWidthHeight(
                self.hoverSurface, 
                (self.hoverSurface.get_width(), 
                self.hoverSurface.get_height()))
        
        else:
            self.setSurfaceWidthHeight(
                self.unpressSurface, 
                (self.unpressSurface.get_width(), 
                self.unpressSurface.get_height()))

        ## Rect used for collision, based on unpress surface
        if self.centered:
            self.buttonRect = Rect(self.xWinPosCenter, self.yWinPosCenter, 
                self.unpressSurface.get_width(), self.unpressSurface.get_height())
        else:
            self.buttonRect = Rect(self.xWinPos, self.yWinPos, 
                self.unpressSurface.get_width(), self.unpressSurface.get_height())

        self.setWinPos()



    ## Sets the button state
    def setState(self, press: bool, hover: bool = False):

        """Sets the button state
        """

        self.pressAudioPlay = False
        self.hoverAudioPlay = False
        
        if self.press == False and press == True:
            self.setSurfaceWidthHeight(
                self.pressSurface, 
                (self.pressSurface.get_width(), 
                self.pressSurface.get_height()))
            self.update = True
            
            self.pressAudioPlay = True

        elif self.hover == False and hover == True: 
            self.setSurfaceWidthHeight(
                self.hoverSurface, 
                (self.hoverSurface.get_width(), 
                self.hoverSurface.get_height()))
            self.update = True
            
            if self.press == False: # Makes sure hover audio doesn't play after letting go of button
                self.hoverAudioPlay = True

        elif ((self.press == True or self.hover == True) 
                and press == False and hover == False):
            
            self.setSurfaceWidthHeight(
                self.unpressSurface, 
                (self.unpressSurface.get_width(), 
                self.unpressSurface.get_height()))
            self.update = True

        self.press = press
        self.hover = hover




## Image Button
class ButtonImage(Button):

    """Button using images
    """

    def __init__(self,
            pos: tuple, 
            pressImage: str, 
            unpressImage: str, 
            hoverImage: str = None, 
            pressScale: float = 1,
            unpressScale: float = 1, 
            hoverSacle: float = 1,
            alpha: int = 255, 
            press: bool = False, 
            pressAudio: str = None, 
            hoverAudio: str = None, 
            centered: bool = True, 
            display: bool = True):
        
        self.pressImage = pressImage
        self.pressScale = pressScale
        self.originalPressSurface, self.pressSurfaceWidth, self.pressSurfaceHeight = self.getSurfaceSetup(
            self.pressImage, self.pressScale)

        self.unpressImage = unpressImage
        self.unpressScale = unpressScale
        self.originalUnpressSurface, self.unpressSurfaceWidth, self.unpressSurfaceHeight = self.getSurfaceSetup(
            self.unpressImage, self.unpressScale)

        self.hoverImage = hoverImage
        self.hoverSacle = hoverSacle
        self.originalHoverSurface, self.hoverSurfaceWidth, self.hoverSurfaceHeight = self.getSurfaceSetup(
            self.hoverImage, self.hoverSacle)
        
        super().__init__(pos, alpha, press, pressAudio, hoverAudio, 
            centered, display)

        self.setSurfaceWidthHeight(self.pressSurface, (self.pressSurfaceWidth, self.pressSurfaceHeight))

    ## Gets the scaled surface & it's width & height
    def getSurfaceSetup(self, image: str, scale: float):

        """Returns scaled surface & it's dimensions

        Returns:
            Surface: scaled image surface
            tuple: images dimensions
        """

        originalImageSurface = self.getScaledImage(image, scale)
        imageSurfaceWidth = originalImageSurface.get_width()
        imageSurfaceHeight = originalImageSurface.get_height()
        
        return originalImageSurface, imageSurfaceWidth, imageSurfaceHeight


    ## Scales button image
    def getScaledImage(self, image: str, scale: float) -> Surface:

        """Returns scaled image

        Returns:
            Surface: scaled image
        """

        buttonSurf = globalVar.getImage(image)
        return transform.scale(buttonSurf, (
            round(buttonSurf.get_width()*scale), 
            round(buttonSurf.get_height()*scale)))


    ## Sets surface for a type of button state
    def setButtonSurface(self, originalSurf: Surface, diamensions: tuple) -> Surface:

        """Returns surface for a type of button state

        Returns:
            Surface: button surface
        """

        newSurf = transform.scale(originalSurf, 
            (round(diamensions[0]* globalVar.win_scale), round(diamensions[1] * globalVar.win_scale)))

        return setSurfaceAlpha(newSurf, self.alpha)





## Text
class Text(UIElement):

    """Text UI Element
    """

    def __init__(self, 
            pos: tuple, 
            text: str, 
            size: int,
            font: str = "verdana", 
            colour: tuple = (0,0,0), 
            alpha: int = 255, 
            centered: bool = True, 
            display: bool = True):
        
        super().__init__(pos, (0, 0), alpha, centered, display)

        self.text = text
        self.size = size
        self.font = font
        self.colour = colour
        self.setSurface()
        self.setWinPos()

    ## Sets the surface
    def setSurface(self):

        """Sets the surface
        """

        self.surface = createText(self.text, self.font, self.colour, round(self.size * globalVar.win_scale))

        self.surface = setSurfaceAlpha(self.surface, self.alpha)

        self.dimensions = (
            round(self.surface.get_width() / globalVar.win_scale), 
            round(self.surface.get_height() / globalVar.win_scale))

    ## Updates the text
    def updateText(self, text: str):

        """Updates the text
        """

        if self.text != text:
            self.text = text
            self.setSurface()
            self.setWinPos()




## Image
class Image(UIElement):

    """Image UI Element
    """

    def __init__(self, 
            pos: tuple, 
            image: str, 
            scale: int, 
            alpha: int = 255, 
            centered: bool = True, 
            display: bool = True):        
        
        self.image = image
        self.scale = scale

        ## Sets width and height based on image's dimensions and scale
        width = globalVar.getImage(self.image).get_width() * scale
        height = globalVar.getImage(self.image).get_height() * scale
        
        super().__init__(pos, (width, height), alpha, centered, display)

        self.setSurface()

    ## Sets the surface
    def setSurface(self):

        """Sets the surface
        """

        self.surface = createSurface(self.dimensions, None, self.alpha)

        self.surface.blit(transform.scale(globalVar.getImage(self.image), 
            (round(self.dimensions[0] * globalVar.win_scale), 
            round(self.dimensions[1] * globalVar.win_scale))), (0,0))

            


## Box
class Box(UIElement):

    """Box UI Element
    """

    def __init__(self, 
            pos: tuple, 
            dimensions: tuple, 
            colour: tuple = (0,0,0), 
            alpha: int = 255, 
            roundedCorner: float = 0, 
            centered: bool = True, 
            display: bool = True):
        
        super().__init__(pos, dimensions, alpha, centered, display)

        self.colour = colour
        self.roundedCorner = roundedCorner
        self.setSurface()

    ## Sets the surface
    def setSurface(self):

        """Sets surface
        """

        if self.roundedCorner > 0:
            self.surface = createSurface(self.dimensions, None, self.alpha)
        
        else:
            self.surface = createSurface(self.dimensions, (0,0,0), self.alpha)

        draw.rect(self.surface, self.colour, (0, 0, round(self.dimensions[0] * globalVar.win_scale),round(self.dimensions[1] * globalVar.win_scale)),
            border_radius = round(self.roundedCorner * globalVar.win_scale))

    




## Menu
class Menu(UIElement):

    """Menu UI Element
    """

    def __init__(self, 
            pos: tuple, 
            dimensions: tuple, 
            colour: tuple = (0,0,0),
            alpha: int = 255, 
            centered: bool = True, 
            display: bool = True):
        
        super().__init__(pos, dimensions, alpha, centered, display)

        self.colour = colour
        self.setSurface()

        self.menuElements = {}


    ## Sets the surface
    def setSurface(self):

        """Sets the surface
        """

        self.surface = createSurface(self.dimensions, self.colour, self.alpha)

    ## Add element to menuElements
    def addElement(self, elementName: str, element: UIElement):

        """Adds element to menu elements
        """

        self.menuElements[elementName] = element

    ## Resize elements & menu surface
    def resize(self):

        """Resizes menu surface & it's elements
        """

        for eachElement in self.menuElements:
            self.menuElements[eachElement].resize()

        self.setWinPos()
        self.setSurface()

        self.drawElements()

    ## Draws elements on Menu surface
    def drawElements(self):

        """Draws elements on menu surface
        """

        if self.colour != None:
            self.surface.fill(self.colour)
        
        for eachElement in self.menuElements:
            self.menuElements[eachElement].draw(self.surface)

    ## Checks whether it needs to update the surface
    def isPress(self, buttonName: str, mousePos: tuple, mouseClick: bool) -> bool:
        
        """Returns whether a button is pressed

        Returns:
            bool: button pressed
        """

        if self.menuElements[buttonName].display:
            ## Gets the mouse position in relation to the menu
            if self.centered:
                menuMousePos = [mousePos[0] - self.xWinPosCenter, mousePos[1] - self.yWinPosCenter]
            else:
                menuMousePos = [mousePos[0] - self.xWinPos, mousePos[1] - self.yWinPos]
        
            ## Checks the buttons state & if it should be updated
            press = self.menuElements[buttonName].isPress(menuMousePos, mouseClick)
            if self.menuElements[buttonName].update == True:
                self.drawElements()

            return press
        
        else:
            return False

    ## Returns a menu element
    def getMenuElement(self, elementName: str) -> UIElement:

        """Returns menu element

        Returns:
            UIElement: UI element
        """

        return self.menuElements[elementName]

    ## Updates text element's text
    def updateText(self, elementName: str, text: str):

        """Updates a text element
        """

        if self.getMenuElement(elementName).text != text:
            self.getMenuElement(elementName).updateText(text)
            self.drawElements()




    ## Adds a box to element dict
    def addBox(self, 
            elementName: str, 
            pos: tuple, 
            dimensions: tuple, 
            colour: tuple = (0,0,0), 
            alpha: int = 255, 
            roundedCorner: float = 0, 
            centered: bool = True, 
            display: bool = True):
        
        """Adds a box to the menu
        """

        self.addElement(elementName, Box(pos, dimensions, 
                                        colour, alpha, 
                                        roundedCorner, centered, 
                                        display))

    ## Adds a image to element dict
    def addImage(self, 
            elementName: str, 
            pos: tuple, 
            image: str, 
            scale: float, 
            alpha: int = 255, 
            centered: bool = True, 
            display: bool = True):

        """Adds an image to the menu
        """
        
        self.addElement(elementName, Image(pos, 
                                        image, scale, 
                                        alpha, 
                                        centered, 
                                        display))

    ## Adds a text to element dict
    def addText(self, 
            elementName: str, 
            pos: tuple, 
            text: str, 
            size: int,
            font: str = "verdana", 
            colour: tuple = (0,0,0), 
            alpha: int = 255, 
            centered: bool = True, 
            display: bool = True):

        """Adds text to the menu
        """
        
        self.addElement(elementName, Text(pos, 
                                        text, size, font, 
                                        colour, alpha, 
                                        centered, display))


    ## Adds Button Image to element dict
    def addButtonImage(self, 
            elementName: str, 
            pos: tuple, 
            pressImage: str, 
            unpressImage: str, 
            hoverImage: str = None, 
            pressScale: float = 1,
            unpressScale: float = 1, 
            hoverSacle: float = 1,
            alpha: int = 255, 
            press = False, 
            pressAudio: str = None, 
            hoverAudio: str = None, 
            centered = True, 
            display = True):

        """Adds a button image to the menu
        """
        
        self.addElement(elementName, ButtonImage(pos, 
                                            pressImage, unpressImage, 
                                            hoverImage, pressScale,
                                            unpressScale, hoverSacle,
                                            alpha,
                                            press, pressAudio, 
                                            hoverAudio, centered, 
                                            display))


    ## Adds Button Text to element dict
    def addButtonText(self, 
            elementName: str, 
            pos: tuple, 
            pressText: str, 
            unpressText: str, 
            hoverText: str = None, 
            pressSize: int = 1,
            unpressSize: int = 1, 
            hoverSize: int = 1, 
            pressColour: tuple = (0, 0, 0), 
            unpressColour: tuple = (0, 0, 0), 
            hoverColour: tuple = (0, 0, 0), 
            font: str = "verdana",
            alpha: int = 255, 
            press: bool = False, 
            pressAudio: str = None, 
            hoverAudio: str = None, 
            centered: bool = True, 
            display: bool = True):

        """Adds button text to the menu
        """
        
        self.addElement(elementName, ButtonText(pos, 
                                            pressText, unpressText, 
                                            hoverText, pressSize,
                                            unpressSize, hoverSize, 
                                            pressColour, 
                                            unpressColour, 
                                            hoverColour, font,
                                            alpha,
                                            press, pressAudio, 
                                            hoverAudio, centered, 
                                            display))





##  ------ FPS & Frametime ------  ##

class fpsCounter:

    """Frametime counter
    """

    def __init__(self):
        self.__setSecondTimer()
        self.frames = 0

        self.__setFrametimeTimer()
        self.frametime = 0

        self.__setFramesText()

    ## Creates text used to diplay fps and ft
    def __setFramesText(self):

        """Creates text used to display fps and ft
        """

        self.framesText = createText(f"{self.frames} fps  |  {self.frametime} ms","bahnschrift", 
                                    (255,255,255), 
                                    round(20*globalVar.win_scale))

    ## Sets new 1 sec time so count frames in 1 sec
    def __setSecondTimer(self):

        """Sets new 1 sec time so count frames in 1 sec
        """

        self.secondTimer = setTimer(1)

    ## Gets the current time
    def __setFrametimeTimer(self):

        """Gets the current time
        """

        self.frametimeTimer = getTime()

    ## Checks how much time has pased since last frame
    ## Converts it into ms, gets the current time again
    def __setFrametime(self):

        """Checks how much time has pased since last frame. Converts it into ms, 
        gets the current time again.
        """

        self.frametime = timeElapsed(self.frametimeTimer)
        self.frametime = round(self.frametime * 1000) # 1000 converts it from s to ms
        self.__setFrametimeTimer()

    ## Checks if second timer is up and updates
    ## the frame text and rests fram counts
    def __setFrames(self):

        """Checks if second timer is up and updates the frame text and rests 
        frame counts
        """

        self.frames += 1
        if isTimer(self.secondTimer):
            self.__setFramesText()
            self.__setSecondTimer()
            self.frames = 0

    def checkFrames(self):

        """Checks frames
        """

        self.__setFrametime()
        self.__setFrames()

    def draw(self, surf: Surface):

        """Draws fps counter on surface
        """

        surf.blit(self.framesText, (
            round(8*globalVar.win_scale), 
            round(3*globalVar.win_scale)))

