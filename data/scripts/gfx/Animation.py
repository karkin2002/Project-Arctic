from pygame import Surface
from data.scripts.UI.saveLoadData import loadImgPath, getImg
import data.scripts.globalVar as globalVar

class Animation:

    """Handles images animations
    """

    __ANIMATION_IMG_NAME = "{name} ({current_frame})"

    def __init__(self, 
            name: str, 
            __num_frames: int, 
            animation_speed: float = 1.0,
            force_animation: bool = False):
        
        self.__name = name

        self.__num_frames = __num_frames

        self.current_frame = 1
        
        self.__animation_speed = animation_speed

        self.force_animation = force_animation

        self.playing = False


    def updateCurrentFrame(self):

        """Updates the animation frames
        """
        
        self.current_frame += (1 * self.__animation_speed) * globalVar.dt

        if int(self.current_frame) > self.__num_frames:
            self.playing = False
            self.current_frame = 1


    def getImgName(self) -> str:

        """Returns animation img name

        Returns:
            str: animation img name
        """

        return self.__ANIMATION_IMG_NAME.format(
            name = self.__name, 
            current_frame = int(self.current_frame))

    def getImg(self) -> Surface:

        """Returns animation img

        Returns:
            Surface: animation img surface
        """        
        
        return getImg(self.getImgName())
