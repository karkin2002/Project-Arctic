from pygame import Surface
from data.scripts.UI.saveLoadData import makeDir, loadImgPath
from random import choice as randChoice, randint
from data.scripts.basic import rotSurf, alphaSurf

from data.scripts.globalVar import getImage

class Decal:

    """Decal that can be drawn onto surfaces.
    """

    __DECAL_TEXTURE_FOLDER_PATH = "data/images/textures/decal/{decal_name}"


    def __init__(self, decal_name: str, rotate: bool = False, alpha_range: tuple = None):
        self.__DECAL_NAME = decal_name

        self.__rotate = rotate
        self.__alpha_range = alpha_range

        self.__loadDecalImgs()    

    
    def __loadDecalImgs(self):

        """Loads the decal images from their folder based on decal name.
        """        
        
        decal_texture_folder_path = self.__DECAL_TEXTURE_FOLDER_PATH.format(
            decal_name= self.__DECAL_NAME)

        makeDir(decal_texture_folder_path)
        
        self.__decal_imgs = loadImgPath(f"{decal_texture_folder_path}/")




    ## ------  Drawing / Getting Decals  ------ ##

    def getDecal(self, decal_img_name: str, rotation: int, alpha: int):
        
        """Returns the decal img surface & it's center position

        Returns:
            Surface: decal img
            tuple: center of decal img
        """

        decal_img = getImage(decal_img_name)

        decal_img, decal_img_center = rotSurf(decal_img, rotation)

        decal_img = alphaSurf(decal_img, alpha)

        return decal_img, decal_img_center



    def getRandDecal(self):

        """Returns random decal.

        Returns:
            Surface: decal img
            tuple: decal img center
            str: decal img name
            int: rotation
            int: alpha
        """
        
        decal_name = randChoice(self.__decal_imgs)

        if self.__rotate:
            rotation = randint(0, 360)
        else:
            rotation = 0

        if self.__alpha_range != None:
            alpha = randint(self.__alpha_range[0], self.__alpha_range[1])
        else:
            alpha = 255

        decal_img, decal_img_center = self.getDecal(decal_name, rotation, alpha)

        return decal_img, decal_img_center, decal_name, rotation, alpha



    def drawRand(self, surf: Surface, pos: tuple):

        """Draws random decal image on a surface.

        Returns:
            str: decal img name
            int: rotation of the decal
            int: alpha of the decal
        """

        decal_img, decal_img_center, decal_name, rotation, alpha = self.getRandDecal()

        if surf != None:
            surf.blit(decal_img, (pos[0] - decal_img_center[0], pos[1] - decal_img_center[1]))

        return decal_name, rotation, alpha


    def draw(self, surf: Surface, decal_img_surf: Surface, pos: tuple):

        if surf != None:
            surf.blit(decal_img_surf, pos)
