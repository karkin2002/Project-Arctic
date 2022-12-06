from pygame import Surface as pySurface, SRCALPHA
from data.scripts.UI.printInfo import printInfo
from data.scripts.UI.saveLoadData import loadData, saveData
from data.scripts.game.TriggerManager import TriggerManager
from data.scripts.gfx.ParticleManager import ParticleManager
from data.scripts.entity.Entity import Entity
from math import ceil as roundUp

import data.scripts.ThreadingVar as threadVar
from data.scripts.game.ThreadingChunks import requestChunk
from data.scripts.gfx.DecalManager import DecalManager
threadVar.init()

import data.scripts.globalVar as globalVar
globalVar.init()

class Map:

    """Stores map data and methods for drawing & processing the map
    """

    MAP_FOLDER_PATH = "data/saves/maps/{map_name}"

    MAP_PATH = MAP_FOLDER_PATH + "/{map_name}_map.json"

    MAP_METADATA_PATH = MAP_FOLDER_PATH + "/{map_name}_metadata.json"

    MAP_OBJECTS_PATH = MAP_FOLDER_PATH + "/{map_name}_objects.json"

    DEFULT_OBJECTS_DICT = {"triggers": {}, "particles": {}, "entities": {}}

    __CHUNK_SIZE = 15

    __RENDER_DISTANCE_GLOBAL_VAR_NAME = "map"

    def __init__(self, 
            map_name: str, 
            map_layers: list, 
            animations: dict, 
            stats: dict):

        self.map_name = map_name

        map_save_path = self.MAP_PATH.format(map_name = self.map_name)
        
        self.triggers = TriggerManager(True)
        self.particles = ParticleManager()
        self.entities = {}

        self.loadMap(map_save_path, animations, stats)

        self.__map_chunks = {}
        for layer in map_layers:
            self.__map_chunks[layer] = {}

        self.__setMapDimensionsPx()
        self.__setMapChunks()
        self.__setExtraMapTiles()
        self.__setChunkSize()

        self.__createMapSurface(map_layers)

        self.draw_from_pos = (0, 0)


    def loadMap(self, path: str, animations: dict, stats: dict):

        """Loads the map data & metadata
        """        

        self.__map = loadData(path)

        map_metadata_path = self.MAP_METADATA_PATH.format(map_name = self.map_name)
        self.__metadata = loadData(map_metadata_path)
        
        self.map_width = self.__metadata["map_width"]
        self.map_height = self.__metadata["map_height"]
        self.TILE_SIZE = self.__metadata["tile_size"]


        map_object_path = self.MAP_OBJECTS_PATH.format(map_name = self.map_name)
        map_objects_dict = loadData(map_object_path)
        
        if "triggers" not in map_objects_dict:
            map_objects_dict["triggers"] = {}
        self.triggers.loadTriggerSaveData(map_objects_dict["triggers"])
        
        if "particles" not in map_objects_dict:
            map_objects_dict["particles"] = {}
        self.particles.loadParticleSaveData(map_objects_dict["particles"])

        if "entities" not in map_objects_dict:
            map_objects_dict["entities"] = {}
        self.__loadEntitySaveData(
            map_objects_dict["entities"], animations, stats)


    def __getEntitySaveData(self):
        entity_dict = {}

        for entity_name in self.entities:
            entity_dict[entity_name] = {
                "type": self.entities[entity_name].type,
                "pos": self.entities[entity_name].pos[:],
                "defult_animation": self.entities[entity_name].defult_animation
            }

        return entity_dict

    def __loadEntitySaveData(self, 
            entity_data: dict, 
            animations: dict, 
            stats: dict):
        
        for entity_name in entity_data:
            self.entities[entity_name] = Entity(
                entity_name,
                entity_data[entity_name]["type"],
                entity_data[entity_name]["pos"], 
                animations = animations[entity_data[entity_name]["type"]],
                defult_animation = entity_data[entity_name]["defult_animation"],
                stats = stats)


    def saveMap(self):

        """Saves the map dict as a json file
        """        

        map_save_path = self.MAP_PATH.format(map_name = self.map_name)
        saveData(map_save_path, self.__map, True)

        map_object_path = self.MAP_OBJECTS_PATH.format(map_name = self.map_name)
        saveData(
            map_object_path, 
            {"triggers": self.triggers.getTriggerSaveData(), 
            "particles": self.particles.getParticleSaveData(), 
            "entities": self.__getEntitySaveData()}, 
            True)

        printInfo("Info", f"Saved map '{self.map_name}'")
        

    def __setChunkSize(self):

        """Sets the chunk_size, chunk_size_px, resized_chunk_size_px, and the
        maps width and height in chunks.
        """        

        # Size of chunk in pixles
        self.__chunk_size_px = self.TILE_SIZE * self.__CHUNK_SIZE

        # Resized size of chunk in pixles
        self.__resized_chunk_size = self.__chunk_size_px


    def __setMapDimensionsPx(self):

        """Sets the maps width and height
        """        

        self.map_width_px = self.map_width * self.TILE_SIZE
        self.map_height_px = self.map_height * self.TILE_SIZE


    def __setMapChunks(self):

        """Sets the maps width and height in chunks
        """        

        self.__map_chunk_width = self.map_width / self.__CHUNK_SIZE
        self.__map_chunk_height = self.map_height / self.__CHUNK_SIZE


    def __setExtraMapTiles(self):

        """Sets the left over tiles
        """        

        self.__extra_map_tiles_width = self.map_width % self.__CHUNK_SIZE
        self.__extra_map_tiles_height = self.map_height % self.__CHUNK_SIZE


    def __setupMapChunk(self, layer: str, chunk_x: int, chunk_y: int):

        """Sets up a map_chunks dict entry for a single chunk
        """        
        self.__map_chunks[layer]["0,0"] = None
        self.__map_chunks[layer][f"{chunk_x},{chunk_y}"] = None

        if (chunk_x == int(self.__map_chunk_width) -1 and 
            self.__extra_map_tiles_width > 0):
            self.__map_chunks[layer][f"{chunk_x + 1},{chunk_y}"] = None
        
        if (chunk_y == int(self.__map_chunk_height) -1 and 
            self.__extra_map_tiles_height > 0):
            self.__map_chunks[layer][f"{chunk_x},{chunk_y + 1}"] = None

        if (chunk_x == int(self.__map_chunk_width) -1 and 
            chunk_y == int(self.__map_chunk_height) -1 and 
            self.__extra_map_tiles_width > 0 and
            self.__extra_map_tiles_height > 0):
            self.__map_chunks[layer][f"{chunk_x + 1},{chunk_y + 1}"] = None


    def __createMapSurface(self, map_layers: list):

        """Sets up the map_chunks dict with empty entries
        """        

        for chunk_y in range(int(self.__map_chunk_height)):
            for chunk_x in range(int(self.__map_chunk_width)):
                for layer in map_layers:
                    self.__setupMapChunk(layer, chunk_x, chunk_y)


    def __setVisableSingleChunk(self, camera_pos: tuple,
                                    index: int,
                                    game_win_center_pos: tuple,
                                    map_length_px: int,
                                    map_chunk_length: int) -> tuple:

        """Returns the visable chunks from one side of a dimensionto the other

        Returns:
            tuple: coordinates of visable chunks
        """        

        ## Start chunk coordiantes
        map_dif_start = ((camera_pos[index] - game_win_center_pos[index]) 
            - globalVar.getRenderDistance(self.__RENDER_DISTANCE_GLOBAL_VAR_NAME))
        
        visible_chunk_start = int(map_dif_start / self.__chunk_size_px)
        
        if visible_chunk_start < 0:
            visible_chunk_start = 0

        ## End chunk coordinates
        map_dif_end = (((map_length_px - camera_pos[index]) - game_win_center_pos[index]) 
            - globalVar.getRenderDistance(self.__RENDER_DISTANCE_GLOBAL_VAR_NAME))
        
        visable_chunk_end = roundUp((map_chunk_length) - (map_dif_end / self.__chunk_size_px))

        if visable_chunk_end > (map_chunk_length):
            visable_chunk_end = roundUp(map_chunk_length)
        
        return (visible_chunk_start, visable_chunk_end)


    def setVisableChunks(self, camera_pos: tuple, game_win_center_pos: tuple):
        
        """Sets the chunks that are viewable
        """        
    
        self.__visable_chunks_x = self.__setVisableSingleChunk(camera_pos, 0,
                                     game_win_center_pos,
                                     self.map_width_px,
                                     self.__map_chunk_width)

        self.__visable_chunks_y = self.__setVisableSingleChunk(camera_pos, 1,
                                     game_win_center_pos,
                                     self.map_height_px,
                                     self.__map_chunk_height)

        self.draw_from_pos = (round(game_win_center_pos[0] - camera_pos[0]),
                              round(game_win_center_pos[1] - camera_pos[1]))



    def __addTileToChunk(self, layer_name: str, 
                                map_queue_item: dict, 
                                x: int, y: int, 
                                tile_x: int, tile_y: int,
                                extra_x: bool = False, 
                                extra_y: bool = False) -> list:

        """Adds tile to chunk. Creates new chunk surface if it's the first tile
        on the chunk.

        Returns:
            list: chunk stage & surface [progression, surface]
        """

        if f"{x},{y}" in self.__map[layer_name]:
            texture = globalVar.getImage(self.__map[layer_name][f"{x},{y}"])
            x_co = tile_x * self.TILE_SIZE
            y_co = tile_y * self.TILE_SIZE

            ## Surface for the chunk
            if map_queue_item[1] == False:
                if extra_x and extra_y: 
                    map_queue_item[1] = pySurface((
                        self.__extra_map_tiles_width * self.TILE_SIZE, 
                        self.__extra_map_tiles_height * self.TILE_SIZE),
                        SRCALPHA)
                elif extra_x:
                    map_queue_item[1] = pySurface((
                        self.__extra_map_tiles_width * self.TILE_SIZE, 
                        self.__chunk_size_px),
                        SRCALPHA)
                elif extra_y:
                    map_queue_item[1] = pySurface((
                        self.__chunk_size_px, 
                        self.__extra_map_tiles_height * self.TILE_SIZE),
                        SRCALPHA)
                else:
                    map_queue_item[1] = pySurface((
                        self.__chunk_size_px, 
                        self.__chunk_size_px), 
                        SRCALPHA)

            map_queue_item[1].blit(texture, (x_co, y_co))
            
        return map_queue_item



    def createMapChunkSurface(self, layer_name: str, chunk_pos: tuple) -> dict:   

        """Creates a chunk & places tiles on it.

        Returns:
            dict: Dictonary of extra chunks (chunks on edge of map that don't
            fit the chunk size).
        """

        threadVar.map_chunk_queue[f"{layer_name},{chunk_pos[0]},{chunk_pos[1]}"] = [
            "Waiting", False]
        
        map_extra_chunk_queue = {}

        chunk_x, chunk_y = chunk_pos[0], chunk_pos[1]


        ## ------  EXTRA X  ------ ##
        if (chunk_x == int(self.__map_chunk_width) - 1
            and self.__extra_map_tiles_width > 0):
            
            map_extra_chunk_queue[f"{layer_name},{chunk_x + 1},{chunk_y}"] = [
                "Processing", False]

            for tile_y in range(self.__CHUNK_SIZE):
                for tile_x in range(self.__extra_map_tiles_width):
                    x = ((chunk_x + 1) * self.__CHUNK_SIZE) + tile_x
                    y = (chunk_y * self.__CHUNK_SIZE) + tile_y

                    map_extra_chunk_queue[f"{layer_name},{chunk_x + 1},{chunk_y}"] = self.__addTileToChunk(layer_name, 
                        map_extra_chunk_queue[f"{layer_name},{chunk_x + 1},{chunk_y}"], 
                        x, y, tile_x, tile_y, True)

            map_extra_chunk_queue[f"{layer_name},{chunk_x + 1},{chunk_y}"][0] = "Done"


        ## ------  EXTRA Y ------ ##
        if (chunk_y == int(self.__map_chunk_height) - 1
            and self.__extra_map_tiles_height > 0):

            map_extra_chunk_queue[f"{layer_name},{chunk_x},{chunk_y + 1}"] = [
                "Processing", False]

            for tile_y in range(self.__extra_map_tiles_height):
                for tile_x in range(self.__CHUNK_SIZE):
                    x = (chunk_x * self.__CHUNK_SIZE) + tile_x
                    y = ((chunk_y + 1) * self.__CHUNK_SIZE) + tile_y

                    map_extra_chunk_queue[f"{layer_name},{chunk_x},{chunk_y + 1}"] = self.__addTileToChunk(layer_name, 
                        map_extra_chunk_queue[f"{layer_name},{chunk_x},{chunk_y + 1}"], 
                        x, y, tile_x, tile_y, False, True)

            map_extra_chunk_queue[f"{layer_name},{chunk_x},{chunk_y + 1}"][0] = "Done"


        ## ------  NORMAL  ------ ##
        threadVar.map_chunk_queue[f"{layer_name},{chunk_x},{chunk_y}"] = [
                "Processing", False]

        for tile_y in range(self.__CHUNK_SIZE):
            for tile_x in range(self.__CHUNK_SIZE):
                x = (chunk_x * self.__CHUNK_SIZE) + tile_x
                y = (chunk_y * self.__CHUNK_SIZE) + tile_y

                threadVar.map_chunk_queue[f"{layer_name},{chunk_x},{chunk_y}"] = self.__addTileToChunk(layer_name, 
                    threadVar.map_chunk_queue[f"{layer_name},{chunk_x},{chunk_y}"], 
                    x, y, tile_x, tile_y)

        threadVar.map_chunk_queue[f"{layer_name},{chunk_x},{chunk_y}"][0] = "Done"

        ## ------  EXTRA X Y  ------ ##
        if (chunk_x == int(self.__map_chunk_width) - 1
            and self.__extra_map_tiles_width > 0
            and chunk_y == int(self.__map_chunk_height) - 1
            and self.__extra_map_tiles_height > 0):

            map_extra_chunk_queue[f"{layer_name},{chunk_x + 1},{chunk_y + 1}"] = [
                "Processing", False]

            for tile_y in range(self.__extra_map_tiles_height):
                for tile_x in range(self.__extra_map_tiles_width):
                    x = ((chunk_x + 1) * self.__CHUNK_SIZE) + tile_x
                    y = ((chunk_y + 1) * self.__CHUNK_SIZE) + tile_y

                    map_extra_chunk_queue[f"{layer_name},{chunk_x + 1},{chunk_y + 1}"] = self.__addTileToChunk(layer_name, 
                        map_extra_chunk_queue[f"{layer_name},{chunk_x + 1},{chunk_y + 1}"], 
                        x, y, tile_x, tile_y, True, True)
            
            map_extra_chunk_queue[f"{layer_name},{chunk_x + 1},{chunk_y + 1}"][0] = "Done"

        return map_extra_chunk_queue


    def isMouseInMap(self, map_pos: tuple) -> bool:

        """Returns whether mouse is in map

        Returns:
            bool: mouse is in map
        """

        return ((map_pos[0] >= 0 and map_pos[0] < self.map_height_px) and 
                (map_pos[1] >= 0 and map_pos[1] < self.map_width_px))

    def isTilePosInMap(self, tile_pos: tuple) -> bool:

        """Returns whether the tile pos is in the map

        Returns:
            bool: Tile pos in map
        """        

        return ((tile_pos[0] < self.map_width and tile_pos[0] >= 0) and 
                (tile_pos[1] < self.map_height and tile_pos[1] >= 0))

    
    def getTilePos(self, map_pos: tuple) -> tuple:

        """Returns tile coordiantes from the map's coordiante.

        Returns:
            tuple: tile coord
        """

        return (int(map_pos[0] / self.TILE_SIZE), int(map_pos[1] / self.TILE_SIZE))

    def getChunkPos(self, map_pos: tuple) -> tuple:

        """Returns chunk coordiantes from the map's coordiante.

        Returns:
            typle: chunk coord
        """
        tile_pos = self.getTilePos(map_pos)

        return (int(tile_pos[0] / self.__CHUNK_SIZE), int(tile_pos[1] / self.__CHUNK_SIZE))

    

    def __redrawChunkLayer(self, 
            layer_name: str,
            map_pos: tuple):
    
        """Redraws a chunk layer 
        """        

        chunk_pos = self.getChunkPos(map_pos)

        if self.__getChunk(layer_name, chunk_pos) != None:
            
            if self.__getChunk(layer_name, chunk_pos) != False:
                self.__map_chunks[layer_name][f"{chunk_pos[0]},{chunk_pos[1]}"] = pySurface((
                    self.__chunk_size_px, 
                    self.__chunk_size_px), 
                    SRCALPHA)

            for tile_y in range(self.__CHUNK_SIZE):
                for tile_x in range(self.__CHUNK_SIZE):
                    x = (chunk_pos[0] * self.__CHUNK_SIZE) + tile_x
                    y = (chunk_pos[1] * self.__CHUNK_SIZE) + tile_y

                    if f"{x},{y}" in self.__map[layer_name]:
                        texture = globalVar.getImage(self.__map[layer_name][f"{x},{y}"])
                        x_co = tile_x * self.TILE_SIZE
                        y_co = tile_y * self.TILE_SIZE

                        if self.__getChunk(layer_name, chunk_pos) == False:
                            self.__map_chunks[layer_name][f"{chunk_pos[0]},{chunk_pos[1]}"] = pySurface((
                                self.__chunk_size_px, 
                                self.__chunk_size_px), 
                                SRCALPHA)

                        self.__getChunk(layer_name, chunk_pos).blit(texture, (x_co, y_co))




    def placeTile(self, 
            layer_name: str, 
            tile_name: str, 
            map_pos: tuple):

        """Place tile on chunk layer & updates the chunk layer
        """

        tile_pos = self.getTilePos(map_pos)

        self.__map[layer_name][f"{tile_pos[0]},{tile_pos[1]}"] = tile_name

        self.__redrawChunkLayer(layer_name, map_pos)


    def removeTile(self,
            layer_name: str,
            map_pos: tuple):

        """Remove tile from a chunk layer & updates the chunk layer
        """
        
        tile_pos = self.getTilePos(map_pos)

        if f"{tile_pos[0]},{tile_pos[1]}" in self.__map[layer_name]:
            del self.__map[layer_name][f"{tile_pos[0]},{tile_pos[1]}"]
        
            self.__redrawChunkLayer(layer_name, map_pos)



    def getTile(self, layer_name: str, tile_pos: tuple) -> str:

        """Returns tile name from the tiles position

        Returns:
            str: tile name
        """
        
        if f"{tile_pos[0]},{tile_pos[1]}" in self.__map[layer_name]:
            return self.__map[layer_name][f"{tile_pos[0]},{tile_pos[1]}"]



    def __drawExtraDecal(self, decal_manager: DecalManager, decal_name: str, 
            decal_img: pySurface, layer_name: str, chunk_pos: tuple, 
            decal_pos: tuple, extra_x: int, extra_y: int):

        """Draws overlapping decal on next chunk
        """

        if extra_x != 0 or extra_y != 0:

            temp_chunk_pos = (chunk_pos[0] + extra_x, chunk_pos[1] + extra_y)

            temp_decal_pos = [decal_pos[0], decal_pos[1]]

            if extra_x > 0:
                temp_decal_pos[0] = decal_pos[0] - self.__chunk_size_px
            elif extra_x < 0:
                temp_decal_pos[0] = decal_pos[0] + self.__chunk_size_px

            if extra_y > 0:
                temp_decal_pos[1] = decal_pos[1] - self.__chunk_size_px
            elif extra_y < 0:
                temp_decal_pos[1] = decal_pos[1] + self.__chunk_size_px

            if self.__getChunk(layer_name, temp_chunk_pos) != None:      
                
                decal_manager.drawDecal(self.__getChunk(layer_name, temp_chunk_pos), 
                    decal_name, decal_img, temp_decal_pos)


    def drawRandDecal(self, 
            decal_manager: DecalManager, 
            decal_name: str, 
            layer_name: str, 
            map_pos: tuple):

        """Draws a random decal on map
        """

        chunk_pos = self.getChunkPos(map_pos)

        decal_img, decal_img_center, decal_img_name, rotation, alpha = decal_manager.getRandDecalSurf(decal_name)

        decal_pos = ((map_pos[0] % self.__chunk_size_px) - decal_img_center[0],
                    (map_pos[1] % self.__chunk_size_px) - decal_img_center[1])

        decal_manager.drawDecal(self.__getChunk(layer_name, chunk_pos), 
            decal_name, decal_img, decal_pos)

        extra_x = 0
        extra_y = 0

        ## Decal goes over a chunk
        if (decal_pos[0] + decal_img.get_width()) > self.__chunk_size_px:
            extra_x = 1

            self.__drawExtraDecal(decal_manager, decal_name, decal_img, layer_name,
            chunk_pos, decal_pos, extra_x, 0)
        
        elif (decal_pos[0]) < 0:
            extra_x = -1

            self.__drawExtraDecal(decal_manager, decal_name, decal_img, layer_name,
            chunk_pos, decal_pos, extra_x, 0)
        
        if (decal_pos[1] + decal_img.get_height()) > self.__chunk_size_px:
            extra_y = 1

            self.__drawExtraDecal(decal_manager, decal_name, decal_img, layer_name,
            chunk_pos, decal_pos, 0, extra_y)
            
        elif decal_pos[1] < 0:
            extra_y = -1
            
            self.__drawExtraDecal(decal_manager, decal_name, decal_img, layer_name,
                chunk_pos, decal_pos, 0, extra_y)

        if extra_x != 0 and extra_y != 0:
            self.__drawExtraDecal(decal_manager, decal_name, decal_img, layer_name,
                chunk_pos, decal_pos, extra_x, extra_y)




    def __addLoadedChunks(self):

        """Takes chunks off the global queue if they are done and places it in
        the map chuck dict
        """        

        for chunk in threadVar.map_chunk_queue:
            if threadVar.map_chunk_queue[chunk][0] == "Done":
                chunk_info = chunk.split(",")
                if f"{chunk_info[1]},{chunk_info[2]}" in self.__map_chunks[chunk_info[0]]:
                    if self.__map_chunks[chunk_info[0]][f"{chunk_info[1]},{chunk_info[2]}"] == None:
                        self.__map_chunks[chunk_info[0]][f"{chunk_info[1]},{chunk_info[2]}"] = threadVar.map_chunk_queue[chunk][1]
                
                threadVar.delete_chunk_queue[chunk] = None
                    

    def __isChunk(self, layer_name: str, chunk_pos: tuple) -> bool:
        
        """Returns whether the chunk exists in map_chunks.

        Returns:
            bool: chunk in map_chunks
        """
        
        return f"{chunk_pos[0]},{chunk_pos[1]}" in self.__map_chunks[layer_name]


    def __getChunk(self, layer_name, chunk_pos: tuple) -> pySurface:

        """Returns a chunk surface from map_chunks

        Returns:
            Surface: map chunk surface
        """

        if self.__isChunk(layer_name, chunk_pos):
            return self.__map_chunks[layer_name][f"{chunk_pos[0]},{chunk_pos[1]}"]
    
 
    def __drawMapChunk(self, surf: pySurface, layer_name: str, chunk_pos: tuple):
        
        """Draws a map chunk on a surface
        """        
        
        if (self.__getChunk(layer_name, chunk_pos) != None and 
                self.__getChunk(layer_name, chunk_pos) != False):
            
            surf.blit(self.__getChunk(layer_name, chunk_pos),
                    (self.draw_from_pos[0] + ((chunk_pos[0] * self.__chunk_size_px)), 
                    self.draw_from_pos[1]  + ((chunk_pos[1] * self.__chunk_size_px)) )   )
            
            # pygame.draw.rect(surf, (255,0,0), (
            #   self.draw_from_pos[0] + (chunk_pos[0] * self.__chunk_size_px), 
            #   self.draw_from_pos[1]  + (chunk_pos[1] * self.__chunk_size_px), 
            #   self.__chunk_size_px, self.__chunk_size_px), 1)


    def draw(self, surf: pySurface):

        """Draws the map on a sufrace
        """

        self.__addLoadedChunks()

        for chunk_y in range ( self.__visable_chunks_y[0], 
                                    self.__visable_chunks_y[1]):
            for chunk_x in range ( self.__visable_chunks_x[0],
                                        self.__visable_chunks_x[1]):
                for map_layer in self.__map_chunks:
                    requestChunk(self.__map_chunks, map_layer, chunk_x, chunk_y)

                    self.__drawMapChunk(surf, map_layer, (chunk_x, chunk_y))

        
