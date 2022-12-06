from pygame import Surface
from data.scripts.UI.UIElements import createText
import data.scripts.globalVar as globalVar
globalVar.init()

class FloatingText:

    """High res text appearing in game win
    """

    def __init__(self, 
            camera_scale: float,
            text: str, 
            pos: tuple,
            font: str,
            colour: tuple,
            size: float,
            display: bool = True):
        
        self.pos = pos

        self.__text = text
        self.__font = font
        self.__colour = colour
        self.__size = size
        self.__display = False

        self.setDisplay(camera_scale, display)


    def setDisplay(self, camera_scale: tuple, value: bool):

        """Sets whether the text should display
        """

        if self.__display != value:
            self.__display = value
            if self.__display:
                self.setTextSurf(camera_scale)


    def isDisplay(self) -> bool:

        """Returns whether the text should be displayed

        Returns:
            bool: text should be displayed
        """        

        return self.__display


    def setText(self, camera_scale: float, text: str):

        """Sets the text
        """

        if self.__text != text:
            self.__text = text

            self.setTextSurf(camera_scale)

    def getText(self):

        """Returns the text
        """

        return self.__text

    def setTextSurf(self, camera_scale: float):

        """Sets the text surface, scaling with the game window
        """

        if self.isDisplay():
            self.__text_surf = createText(
                self.__text, 
                self.__font, 
                self.__colour, 
                round(self.__size * camera_scale))

            self.dimensions = (
                self.__text_surf.get_width(),
                self.__text_surf.get_height())

            self.center = (
                self.__text_surf.get_width() / 2, 
                self.__text_surf.get_height() / 2)


    def draw(self, surf: Surface, draw_from_pos: tuple, camera_scale: float):

        """Draws text on surface
        """

        if self.isDisplay():

            surf.blit(
                self.__text_surf, 
                (((draw_from_pos[0] + self.pos[0]) * camera_scale) - self.center[0], 
                ((draw_from_pos[1] + self.pos[1]) * camera_scale) - self.center[1]))