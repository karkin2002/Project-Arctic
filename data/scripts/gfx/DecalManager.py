from pygame import Surface
from data.scripts.UI.printInfo import printInfo
from data.scripts.gfx.Decal import Decal
from data.scripts.UI.saveLoadData import loadData, saveData

class DecalManager:

    """Manages and loads all decals.
    """

    __DECAL_PROPTERTIES_PATH = "data/config/decal_properties.json"

    __DECAL_PROPERTIES_ROTATE = "rotate"

    __DECAL_PROPERTIES_ALPHA_RANGE = "alpha_range"
    
    def __init__(self):
        self.__decal_dict = {}

        self.__decal_properties_dict = loadData(self.__DECAL_PROPTERTIES_PATH)

        self.__loadDecals()


    def addDecal(self, 
            decal_name: str, 
            rotate: int = 0, 
            alpha_range: tuple = None):

        """Adds new decal object to decal dict.
        """

        self.__decal_dict[decal_name] = Decal(decal_name, rotate, alpha_range)

    
    def __loadDecals(self):

        """Loads decals from decal properties.
        """

        save_decal = False

        for decal_name in self.__decal_properties_dict:
            
            decal_properties = self.__decal_properties_dict[decal_name]

            ## Checks if "rotate" & "alpha_range" are in decal_properties
            ## and adds it if it isn't
            if self.__DECAL_PROPERTIES_ROTATE not in decal_properties:
                decal_properties[self.__DECAL_PROPERTIES_ROTATE] = False
                save_decal = True
            
            if self.__DECAL_PROPERTIES_ALPHA_RANGE not in decal_properties:
                decal_properties[self.__DECAL_PROPERTIES_ALPHA_RANGE] = None
                save_decal = True
            
            self.addDecal(
                    decal_name,
                    decal_properties[self.__DECAL_PROPERTIES_ROTATE],
                    decal_properties[self.__DECAL_PROPERTIES_ALPHA_RANGE])

        if save_decal:
            saveData(
                self.__DECAL_PROPTERTIES_PATH, 
                self.__decal_properties_dict, 
                True)


    def __isDecal(self, decal_name: str) -> bool:

        """Returns whether decal is in decal dict

        Returns:
            bool: whether decal is in decal dict
        """

        return decal_name in self.__decal_dict


    def __getDecal(self, decal_name: str) -> Decal:
        
        """Returns a decal object from decal dict

        Raises:
            Exception: decal isn't in decal dict

        Returns:
            Decal: decal from decal dict
        """
        
        if self.__isDecal(decal_name):
            return self.__decal_dict[decal_name]
        else:
            printInfo("ERROR", f"'{decal_name}' decal does not exist")
            raise Exception(f"'{decal_name}' decal does not exist")





    def getDecalSurf(self, decal_name, decal_img_name: str, rotation: int, alpha: int):
        
        """Returns the decal img surface & it's center position

        Returns:
            Surface: decal img
            tuple: center of decal img
        """

        return self.__getDecal(decal_name).getDecalSurf(
            decal_img_name, rotation, alpha)


    def getRandDecalSurf(self, decal_name):

        """Returns random decal.

        Returns:
            Surface: decal img
            tuple: decal img center
            str: decal img name
            int: rotation
            int: alpha
        """

        return self.__getDecal(decal_name).getRandDecal()


    def drawRandDecal(self, surf: Surface, decal_name: str, pos: tuple):

        """Draws random decal on surface.

        Returns:
            str: decal img name
            int: rotation of decal
            int: alpha of decal
        """

        return self.__getDecal(decal_name).drawRand(surf, pos)


    def drawDecal(self, surf: Surface, decal_name: str, 
            decal_img_surf: Surface, pos: tuple):
        
        """Draws a decal on surface.
        """

        self.__getDecal(decal_name).draw(surf, decal_img_surf, pos)
            

