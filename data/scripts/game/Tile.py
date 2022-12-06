from data.scripts.globalVar import getImage
from data.scripts.basic import createMask

class Tile:

    """Stores data about tiles
    """    

    def __init__(self, map_layer: str, tile_name: str, tile_properties: dict):
        self.tile_name = tile_name
        self.map_layer = map_layer

        self.__setTileMask("collision" in tile_properties)

    def isCollision(self) -> bool:

        """Returns whether the tile has collsions

        Returns:
            bool: tile has collision
        """

        return self.mask != None

    def __setTileMask(self, collision: bool):

        """If tile has 'collision' property, creates mask of texture, otherwise
        sets to None
        """

        if collision:
            tile_img = getImage(self.tile_name)
            self.mask = createMask(tile_img)
        
        else:
            self.mask = None