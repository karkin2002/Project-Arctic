from pygame import Surface
from data.scripts.gfx.FloatingText import FloatingText
from data.scripts.UI.printInfo import printInfo

class FloatingTextManager:
    def __init__(self):
        self.floating_text_dict = {}
    
    def addFloatingText(self, 
            camera_scale: float, 
            name: str, 
            text: str, 
            pos: tuple, 
            font: str, 
            colour: tuple, 
            size: int,
            display: bool = True):

        """Adds a floating text
        """
        
        self.floating_text_dict[name] = FloatingText(
            camera_scale, 
            text, 
            pos,
            font,
            colour,
            size,
            display)


    def removeFloatingText(self, name: str):

        """Removes a floating text
        """

        if self.isFloatingText(name):
            del self.floating_text_dict[name]


    def isFloatingText(self, name: str) -> bool:

        """Returns whether the floating text exists

        Returns:
            bool: text exists
        """        

        if name in self.floating_text_dict:
            return True
        else:
            printInfo("Error", f"'{name}' floating text doesn't exist")
            return False


    def getFloatingText(self, name: str) -> FloatingText:

        """Returns floating text

        Returns:
            FloatingText: floating text
        """

        if self.isFloatingText(name):
            return self.floating_text_dict[name]

    def setPos(self, name: str, pos: tuple):
        if self.isFloatingText(name):
            self.floating_text_dict[name].pos = pos

    def setText(self, camera_scale: float, name: str, text: str):

        """Sets floating texts, text
        """

        if self.isFloatingText(name):
            self.floating_text_dict[name].setText(camera_scale, text)

    def getText(self, name: str) -> str:

        """Returns floating texts, text

        Returns:
            str: text
        """
        
        if self.isFloatingText(name):
            return self.floating_text_dict[name].getText()

    
    def setFloatingTextDisplay(self, name: str, camera_scale: float, display: bool):

        if self.isFloatingText(name):
            self.getFloatingText(name).setDisplay(camera_scale, display)


    def resize(self, camera_scale: float):

        """Resizes the floating text
        """

        for floating_text_name in self.floating_text_dict:
            self.floating_text_dict[floating_text_name].setTextSurf(camera_scale)


    

    def draw(self, surf: Surface, draw_from_pos: tuple, camera_scale: float):

        """Draws the floating text on a surface
        """

        for floating_text_name in self.floating_text_dict:
            self.floating_text_dict[floating_text_name].draw(
                surf, 
                draw_from_pos, 
                camera_scale)