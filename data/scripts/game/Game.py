from data.scripts.UI.printInfo import printInfo
from data.scripts.UI.saveLoadData import loadData, loadImg, loadImgPath, saveData, makeDir
from data.scripts.game.Map import Map
from data.scripts.game.Camera import Camera
from data.scripts.UI.UI import UI
from data.scripts.gfx.DecalManager import DecalManager
from pygame import Surface as pySurface, transform as pyTransform, Vector2
from data.scripts.entity.Entity import Entity
from data.scripts.game.ThreadingChunks import checkChunkQueue
from data.scripts.game.Tile import Tile
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from data.scripts.gfx.FloatingTextManager import FloatingTextManager
from data.scripts.audio.VoiceManager import VoiceManager
import pygame, concurrent.futures, random

import data.scripts.ThreadingVar as threadVar
threadVar.init()

import data.scripts.globalVar as globalVar
globalVar.init()

class Game:

    """Class for all game elements
    """    


    __ERROR_IMG_PATH = "data/images/textures/error.png"

    __SELECTOR_IMG_PATH = "data/images/textures/selector.png"

    __DEFULT_CAMERA_NAME = "defult_camera"


    __ANIMATION_PROPERTY_PATH = "data/config/entity_animation_properties.json"

    __ENTITY_STATS_PATH = "data/config/entity_stats.json"


    __MAP_TEXTURE_PATH = "data/images/textures/map/{map_layer}/"

    __TILE_PROPERTY_PATH = "data/config/tile_properties.json"

    __MAP_LAYERS = ["ground", "surface", "object", "sky"]

    __DELETE_TILE_NAME = "remove_{layer_name}"


    CHUNK_QUEUE_TIME = 0.08


    __VOICE_AUDIO_CAT_NAME = "voice"


    def __init__(self, 
            player_entity_name: str = None, 
            background_colour: tuple = None, 
            pixel_cursor: tuple = None,
            map_boarder: bool = False, 
            draw_triggers: bool = False,
            save_map_on_exit: bool = False):

        self.background_colour = background_colour
        self.pixel_cursor = pixel_cursor
        self.map_boarder = map_boarder
        self.__draw_triggers = draw_triggers

        loadImg(self.__SELECTOR_IMG_PATH)

        loadImg(self.__ERROR_IMG_PATH)

        self.loadMapTextures()

        self.__map_textures = {}
        for map_layer in self.__MAP_LAYERS:
            self.__map_textures[map_layer] = []

        self.__maps = {}
        self.__collision_matrices = {}
        self.map_name = None
        self.__save_map_on_exit = save_map_on_exit

        self.player_entitiy_name = player_entity_name
        self.entity_animation_properties = loadData(self.__ANIMATION_PROPERTY_PATH)
        self.__entity_stats = loadData(self.__ENTITY_STATS_PATH)
        self.__delete_entity = []

        self.__cameras = {}
        self.__camera_name = self.__DEFULT_CAMERA_NAME
        self.addCamera(self.__camera_name, (0, 0))
        
        self.__decals = DecalManager()
        self.__floating_text = FloatingTextManager()

        globalVar.audio.addCat(self.__VOICE_AUDIO_CAT_NAME)
        self.voices = VoiceManager()
        
        self.resizeGameWin()

        self.startThread()

    def resizeGameWin(self):

        """Resizes the game window by setting the scale, game window
        dimensions, game window's scale and creates the game window
        """        

        ## Sets the scale value for the camera
        self.getCamera(self.__camera_name).setScale()


        ## Sets the game windows dimensions based on the scale value
        self.__game_win_width = round(globalVar.win_width 
                / self.__getCameraScale(self.__camera_name))
        self.__game_win_height = round(globalVar.win_height
                / self.__getCameraScale(self.__camera_name))

        ## Center of the game window
        self.__game_win_center_pos = (self.__game_win_width / 2, 
                                      self.__game_win_height / 2)

        ## The game window surface
        self.__game_win = pySurface((self.__game_win_width, 
                                     self.__game_win_height))

        self.__floating_text.resize(self.__getCameraScale(self.__camera_name))

    def scaleGameWin(self) -> pySurface:

        """Scales the game window to the size of the UI window

        Returns:
            Surface: Scaled game win surface
        """

        return pyTransform.scale(self.__game_win, (globalVar.win_width, 
                                                   globalVar.win_height))


    ## ------  Textures  ------ ##

    def loadMapTextures(self):

        """Loads map textures, adds them to tile properties if they're not 
        in tile properties
        """        

        tile_properties = loadData(self.__TILE_PROPERTY_PATH)
        self.tiles = {}

        for map_layer in self.__MAP_LAYERS:

            texture_path = self.__MAP_TEXTURE_PATH.format(map_layer = map_layer)
            texture_list = loadImgPath(texture_path)

            for texture_name in texture_list:

                ## adds texture to tile properties if it isn't there
                if texture_name not in tile_properties[map_layer]:
                    tile_properties[map_layer][texture_name] = {}

                self.tiles[texture_name] = Tile(
                        map_layer,
                        texture_name, 
                        tile_properties[map_layer][texture_name])

        saveData(self.__TILE_PROPERTY_PATH, tile_properties, True)

    def getTile(self, tile_name: str) -> Tile:
        
        """Returns Tile object from tiles dict

        Raises:
            Exception: Tile objects doesn't exist

        Returns:
            Tile: tile
        """

        if tile_name in self.tiles:
            return self.tiles[tile_name]
        
        else:
            raise Exception(f"'{tile_name}' Tile object doesn't exist")



    ## ------  Input  ------ ##

    def getGameMousePos(self) -> tuple:

        """Returns the mouse's position on the game window.

        Returns:
            tuple: mouse's position
        """

        return ((globalVar.mouse_pos[0] / self.__getCameraScale(self.__camera_name)), 
                (globalVar.mouse_pos[1] / self.__getCameraScale(self.__camera_name)))

    def getMapMousePos(self) -> tuple:

        """Returns mouse's position on the map

        Returns:
            tuple: mouse's position
        """

        game_mouse_pos = self.getGameMousePos()

        current_map = self.getMap()

        return (int(game_mouse_pos[0] - current_map.draw_from_pos[0]),   
                int(game_mouse_pos[1] - current_map.draw_from_pos[1]))

    def getTileMousePos(self) -> tuple:

        """Returns tile the mouse is on

        Returns:
            tuple: tile position
        """

        current_map = self.getMap()
        
        return current_map.getTilePos(self.getMapMousePos())

    def getChunkMousePos(self) -> tuple:

        """Returns chunk the mouse is on

        Returns:
            tuple: chunk position
        """

        current_map = self.getMap()

        return current_map.getChunkPos(self.getMapMousePos())


    ## ------  Threading  ------ ##

    def startThread(self):

        """Starts thread for loading chunks
        """

        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.executor.submit(checkChunkQueue, self)


    ## ------  Map  ------ ##

    def setMapName(self, map_name: str = None):

        """Sets the visible map (map_name = None, will set map to whatever
        map the player entity is on)
        """        

        if map_name == None and self.player_entitiy_name != None:
            if self.isEntitiy(self.player_entitiy_name, map_name):
                self.map_name = self.getEntityMap(self.player_entitiy_name).map_name

        elif map_name in self.__maps:
            self.map_name = map_name
        
        else:
            printInfo("info", f"{map_name} doesn't exist")

        self.updateCamera(True)

    def addMap(self, map_name: str):

        """Adds a new map to the maps dict
        """        

        self.__maps[map_name] = Map(
            map_name, 
            self.__MAP_LAYERS, 
            self.entity_animation_properties,
            self.__entity_stats)

        self.__load_collision_matrix(map_name)


    def getMap(self, map_name: str = None) -> Map:
        
        """Returns a map from maps dict, set map_name to None if you want
        current map

        Raises:
            Exception: map doesn't exist

        Returns:
            Map: map
        """
        if map_name == None:
            map_name = self.map_name
        
        if map_name in self.__maps:
            return self.__maps[map_name]
        else:
            raise Exception("Need to set map name --> setMapName(map_name)")


    def newMap(self, 
            map_name: str, 
            dimensions: tuple, 
            base_textures: list = [],
            tile_size: int = 16):

        """Creates new map files & adds map to game
        """

        map_folder_path = Map.MAP_FOLDER_PATH.format(map_name = map_name)
        map_path = Map.MAP_PATH.format(map_name = map_name)
        map_metadata_path = Map.MAP_METADATA_PATH.format(map_name = map_name)
        map_objects_path = Map.MAP_OBJECTS_PATH.format(map_name = map_name)

        makeDir(map_folder_path)
        
        map_dict = {}
        for layer in self.__MAP_LAYERS:
            map_dict[layer] = {}
        
        for layer in self.__MAP_LAYERS:
            if layer == self.__MAP_LAYERS[0]:
                for y in range(dimensions[1]):
                    for x in range(dimensions[0]):

                        if len(base_textures) > 0: 
                            map_dict[layer][f"{x},{y}"] = random.choice(
                                base_textures)


        saveData(map_path, map_dict)

        saveData(map_metadata_path, {
            "map_width": dimensions[0], 
            "map_height": dimensions[1], 
            "tile_size": tile_size})

        saveData(map_objects_path, Map.DEFULT_OBJECTS_DICT)

        self.addMap(map_name)

        if self.map_name == None:
            self.setMapName(map_name)


    def __isMap(self) -> bool:

        """Returns if map name isn't null

        Returns:
            bool: map name isn't null
        """

        return self.map_name != None

    def __drawMap(self):

        """Draws map onto the game window
        """
        
        if self.__isMap():
            current_map = self.getMap()

            current_map.draw(self.__game_win)

            if self.map_boarder:
                pygame.draw.rect(
                    self.__game_win, 
                    (255, 0, 0), 
                    (current_map.draw_from_pos[0],
                    current_map.draw_from_pos[1],
                    current_map.map_width_px,
                    current_map.map_height_px),
                    1)

            # if self.isMouseInMap():
            #     self.__game_win.blit(
            #         globalVar.getImage("selector"), 
            #         (current_map.draw_from_pos[0] + (self.getTileMousePos()[0] * current_map.TILE_SIZE), 
            #         current_map.draw_from_pos[1] + (self.getTileMousePos()[1] * current_map.TILE_SIZE)))


    def isMouseInMap(self) -> bool:

        """Returns whether mouse is in map

        Returns:
            bool: mouse in map
        """

        return self.getMap().isMouseInMap(self.getMapMousePos())


    def __isMapPosVisable(self, 
            current_map: Map,
            map_pos: tuple, 
            width_render_dist: int = 1, 
            height_render_dist: int = 1) -> bool:

        """Returns whether a map position is visible on the game window.

        Returns:
            bool: map position visible
        """
        
        return ((current_map.draw_from_pos[0] + map_pos[0]) < (self.__game_win_width + width_render_dist) and
                (current_map.draw_from_pos[0] + map_pos[0]) > -abs(width_render_dist) and
                (current_map.draw_from_pos[1] + map_pos[1]) < (self.__game_win_height + height_render_dist) and 
                (current_map.draw_from_pos[1] + map_pos[1]) > -abs(height_render_dist))


    def placeTile(self, tile_name: str):

        """Checks & places tile on surface
        """        

        if tile_name != None:
            if self.isMouseInMap():

                if tile_name in self.tiles:
                    
                    current_map = self.getMap()

                    if current_map.getTile(
                            self.tiles[tile_name].map_layer, 
                            self.getTileMousePos()) != tile_name:
                        
                        current_map.placeTile(
                            self.tiles[tile_name].map_layer, 
                            tile_name, 
                            self.getMapMousePos()
                        )

                else:
                    if self.isMouseInMap():
                        for layer_name in self.__MAP_LAYERS:
                            if tile_name == self.__DELETE_TILE_NAME.format(
                                    layer_name=layer_name):
                            
                                current_map = self.getMap()

                                current_map.removeTile(layer_name, self.getMapMousePos())

                                break

    
    def saveGame(self):

        """Saves states of all maps
        """

        for map_name in self.__maps:
            self.__maps[map_name].saveMap()

    def __saveOnExit(self):

        """Saves the game when the program ends
        """

        if not globalVar.run and self.__save_map_on_exit:
            self.saveGame()



    ##  ------ Pathfinding ------  ##

    def __load_collision_matrix(self, map_name: str):

        """Adds a matrix to collision_matrices, states which tiles have 
        collisions on it
        """

        current_map = self.getMap(map_name)

        collision_matrix = []

        for tile_y in range(current_map.map_height):

            collision_matrix.append([])
            for tile_x in range(current_map.map_width):
                collision_value = 1

                for layer_name in self.__MAP_LAYERS:
                    
                    tile_name = current_map.getTile(layer_name, (tile_x, tile_y))

                    if tile_name != None:

                        tile = self.getTile(tile_name)
                            
                        if tile.isCollision():
                            collision_value = 0
                            break
                
                collision_matrix[tile_y].append(collision_value)
        
        self.__collision_matrices[map_name] = collision_matrix

    
    def __isCollisionOnTile(self, tile_pos: tuple, map_name: str = None) -> bool:

        """Returns whether there is a collision on the tile

        Returns:
            bool: collision on tile
        """
        current_map = self.getMap(map_name)

        for layer_name in self.__MAP_LAYERS:
                
                tile_name = current_map.getTile(layer_name, tile_pos)

                if tile_name != None:

                    tile = self.getTile(tile_name)
                        
                    if tile.isCollision():
                        return True
        
        return False


    def pathfind(self, map_name: str, start_pos: tuple, end_pos: tuple) -> list:

        """Returns list of tile positions, pathfinding from start to end

        Returns:
            list: path for entity to take
        """

        if start_pos != end_pos:
            current_map = self.getMap()

            if (current_map.isTilePosInMap(start_pos) and 
                current_map.isTilePosInMap(end_pos)):
                
                if (self.__isCollisionOnTile(start_pos, map_name) or 
                    self.__isCollisionOnTile(end_pos, map_name)):
                    return []

                grid = Grid(matrix=self.__collision_matrices[map_name])
                start = grid.node(int(start_pos[0]), int(start_pos[1]))
                end = grid.node(int(end_pos[0]), int(end_pos[1]))
                
                finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
                path, runs = finder.find_path(start, end, grid)
                
                return path

        return []


    ## ------  Decals  ------ ##
    def drawDecal(self, decal_name, map_pos):

        """Draws a decal on the map
        """

        self.getMap().drawRandDecal(
            self.__decals, decal_name, 
            self.__MAP_LAYERS[0], map_pos)


    ## ------  Particles  ------ ##
    def addParticleSpawner(self, 
            name: str, 
            pos: tuple, 
            particle_name: str, 
            map_name: str = None):

        """Adds a particle spawner to a map
        """
        
        self.getMap(map_name).particles.addParticleSpawner(name, pos, particle_name)
    
    def setParticleSpawnerPos(self, 
            name: str, 
            pos: tuple, 
            map_name: str = None):

        """Sets a particle spawners position
        """
        
        self.getMap(map_name).particles.setParticleSpawnerPos(name, pos)

    def setParticleSpawnerTargetPos(self,
            name: str, 
            pos: tuple, 
            map_name: str = None):

        """Sets a particle spawners position
        """
        
        self.getMap(map_name).particles.setParticleSpawnerTargetPos(name, pos)


    def setParticleSpawnerSpawn(self,
            name: str,
            spawn: bool,
            map_name: str = None):

        """Sets whether a particle spawn should spawn particles"""    

        self.getMap(map_name).particles.setParticleSpawnerSpawn(name, spawn)

    def getParticleSpawnerSpawn(self,
            name: str,
            map_name: str = None) -> bool:

        """Returns the particle spawners spawn value"""    

        return self.getMap(map_name).particles.getParticleSpawnerSpawn(name)

    def __drawParticles(self):

        """Draws particles
        """        
        
        if self.__isMap():
            self.getMap().particles.drawParticles(
                self.__game_win, 
                self.getMap().draw_from_pos, 
                self.__game_win_width, 
                self.__game_win_height)


        


    ## ------  Floating Text  ------ ##
    def addFloatingText(self, 
            name: str, 
            text: str, 
            pos: tuple, 
            font: str, 
            colour: tuple, 
            size: int,
            display: bool = True):
        
        """Adds floating text
        """

        self.__floating_text.addFloatingText( 
            self.__getCameraScale(self.__camera_name),
            name, text, pos, globalVar.getFont(font), colour, size, display)

    def removeFloatingText(self, name: str):

        """Removes floating text
        """

        self.__floating_text.removeFloatingText(name)

    def setFloatingTextPos(self, name: str, pos: tuple):

        """Sets a floating texts position
        """

        self.__floating_text.setPos(name, pos)

    def setFloatingTextText(self, name: str, text: str):

        """Sets a floating texts, text
        """

        self.__floating_text.setText(self.__getCameraScale(self.__camera_name), name, text)

    def setFloatingTextDisplay(self, name, display: bool):

        """Sets whether the floating text will be displayed
        """

        self.__floating_text.setFloatingTextDisplay(
            name, self.__getCameraScale(self.__camera_name), display)

    
    def __drawFloatingText(self, surf):

        """Draws the floating text on screen
        """        

        floating_text_dict = self.__floating_text.floating_text_dict
        
        for floating_text_name in floating_text_dict:

            if floating_text_dict[floating_text_name].isDisplay():

                floating_text = floating_text_dict[floating_text_name]
            
                if self.__isMapPosVisable(
                        self.getMap(),
                        floating_text.pos,
                        floating_text.center[0],
                        floating_text.center[1]):

                    current_map = self.getMap()
                    
                    floating_text.draw(
                        surf, 
                        current_map.draw_from_pos, 
                        self.__getCameraScale(self.__camera_name))

    ## ------  Voices  ------ ##
    def addVoice(self, 
            voice_name: str, 
            voice_title: str,
            letter_speed: float = 0.05,
            pause_speed: int = 1,
            break_speed: int = 2):

        self.voices.addVoice(
            self.__VOICE_AUDIO_CAT_NAME, 
            voice_name, 
            voice_title, 
            letter_speed,
            pause_speed,
            break_speed)

    
    ## ------  Triggers  ------ ##
    def addTrigger(self,
            name: str,
            pos: tuple,
            dimensions: tuple,
            location: tuple,
            new_map_name: str = None,
            trigger: bool = True,
            map_name: str = None):

        """Adds trigger
        """

        self.getMap(map_name).triggers.addTrigger(
            name, pos, dimensions, location, new_map_name, trigger)

    def __checkTrigger(self, entity_name: str = None):

        """Checks whether entity collides with trigger
        """

        entity_obj = self.getEntity(entity_name)


        map_name = self.getMap().triggers.checkTriggers(entity_obj)

        if map_name != None:
            self.__setEntityMap(entity_obj, map_name)

            if entity_name == None or entity_name == self.player_entitiy_name:
                self.setMapName(map_name)
                self.setCameraPos(self.getEntity(entity_name).getMapPos())

    def isTrigger(self, trigger_name: str, entity_name: str) -> bool:

        """Returns whether an entity has triggered a trigger

        Returns:
            bool: triggered
        """

        return self.getMap().triggers.isTrigger(trigger_name, entity_name)

    
    def __drawTriggers(self):

        """Draws triggers
        """

        if self.__draw_triggers:
            if self.__isMap():
                self.getMap().triggers.draw(
                    self.__game_win, 
                    self.getMap().draw_from_pos)




    ## ------  Entity  ------ ##
    def addEntity(self, entity_name: str, type: str, pos: tuple, defult_animation: str = None, map_name: str = None):

        """Adds entity to entities dict
        """    
        
        if type in self.entity_animation_properties:
            self.getMap(map_name).entities[entity_name] = Entity(
                entity_name,
                type, 
                pos, 
                animations = self.entity_animation_properties[type],
                defult_animation = defult_animation,
                stats = self.__entity_stats)
       
        else:
            self.getMap(map_name).entities[entity_name] = Entity(entity_name, type, pos)
            self.entity_animation_properties[type] = {}
            saveData(self.__ANIMATION_PROPERTY_PATH, self.entity_animation_properties, True)

    def removeEntity(self, entity_name):

        """Removes Entity
        """

        self.__delete_entity.append(entity_name)
        
    
    def getEntity(self, entity_name: str = None) -> Entity:

        """Retruns entity by name

        Returns:
            Entity: entity
        """

        if entity_name == None:
            entity_name = self.player_entitiy_name

        for map_name in self.__maps:
            if entity_name in self.getMap(map_name).entities:
                return self.getMap(map_name).entities[entity_name]

        printInfo("Error", f"{entity_name} entitiy doesn't exist")

    def isEntitiy(self, entity_name: str = None, map_name: str = None):

        if entity_name == None:
            entity_name = self.player_entitiy_name

        if map_name == None:
            for map_name in self.__maps:
                if entity_name in self.getMap(map_name).entities:
                    return True
            return False
        
        else:
            if entity_name in self.getMap(map_name).entities:
                return True
            return False
            

    def getEntityMap(self, entity_name: str = None):
    
        if entity_name == None:
            entity_name = self.player_entitiy_name
        
        for map_name in self.__maps:
            current_map = self.getMap(map_name)
            if entity_name in current_map.entities:
                return current_map

        printInfo("Error", f"{entity_name} entitiy doesn't exist")
            

    def __setEntityMap(self, 
            entity_obj: Entity, 
            map_name: str):

        """Sets what map an entity is in
        """
        
        if entity_obj != None:
            del self.getEntityMap(entity_obj.name).entities[entity_obj.name]

            self.getMap(map_name).entities[entity_obj.name] = entity_obj


    def __createMaskList(self, current_map: Map, entity_obj: Entity) -> list:

        """Returns a list of masks that may collide with an entity object

        Returns:
            list: 2D array [[mask, (x, y)], [mask, (x, y)]]
        """

        tile_pos =  current_map.getTilePos(entity_obj.getMapPos())

        mask_collision_list = []

        for tile_y in range(
                tile_pos[1] - entity_obj.COLLISION_RANGE, 
                (tile_pos[1] + entity_obj.COLLISION_RANGE) + 1):
            for tile_x in range(
                    tile_pos[0] - entity_obj.COLLISION_RANGE, 
                    (tile_pos[0] + entity_obj.COLLISION_RANGE) + 1):
                
                for map_layer in self.__MAP_LAYERS:
                    
                    tile_name = current_map.getTile(map_layer, (tile_x, tile_y))

                    if tile_name != None:
                        
                        tile = self.getTile(tile_name)
                        
                        if tile.isCollision():
                            mask_collision_list.append(
                                [tile.mask, 
                                (current_map.TILE_SIZE * tile_x, 
                                current_map.TILE_SIZE * tile_y)])

        return mask_collision_list
    

    def moveEntity(self, 
            name: str = None,
            up: bool = False, 
            down: bool = False, 
            left: bool = False,
            right: bool = False,
            target_pos: Vector2 = None):

        """Moves an entity also handeling collision
        """

        entity_obj = self.getEntity(name)

        if up or down or left or right or target_pos:

            mask_collision_list = self.__createMaskList(
                self.getMap(), entity_obj)
            
            if target_pos == None:
                entity_obj.move(mask_collision_list, up, down, left, right)
            else:
                entity_obj.moveTowards(target_pos, mask_collision_list)

            self.__checkTrigger(name)

            self.__entity_pickup_items(name)
        
        else:
            entity_obj.move([], up, down, left, right)

    
    def setEntityPath(self, end_pos: tuple, entity_name: str = None):

        """Sets the entities path, using A* pathfinding algorithm
        """

        current_map = self.getMap()
        entity_tile_pos = self.getEntity(entity_name).getTilePos(current_map.TILE_SIZE)


        if len(self.getEntity(entity_name).path) > 0:
            if end_pos != self.getEntity(entity_name).path[len(self.getEntity(entity_name).path) - 1]:
                self.getEntity(entity_name).path = self.pathfind(
                    self.map_name, 
                    entity_tile_pos,
                    end_pos)
        else:
            self.getEntity(entity_name).path = self.pathfind(
                self.map_name, 
                entity_tile_pos,
                end_pos)


    def __pathfindEntity(self, entity_name):

        entity_obj = self.getEntity(entity_name)

        if len(entity_obj.path) > 0:

            mask_collision_list = self.__createMaskList(self.getMap(), entity_obj)

            entity_obj.pathfind(
                self.getMap().TILE_SIZE, 
                mask_collision_list)

    def __entity_pickup_items(self, entity_name):

        """Processes entities picking up items
        """        

        entities_dict = self.getMap().entities

        if entity_name == None:
            entity_name = self.player_entitiy_name
        
        if entities_dict[entity_name].getStat("item") == False:                         ## MUST BE A FASTER WAY OF DOING THIS!!!
            for item_name in entities_dict:
                if entities_dict[item_name].getStat("item"):
                    if self.isEntityCollide(entity_name, item_name, True):
                        self.removeEntity(item_name)
                        entities_dict[entity_name].addItem(entities_dict[item_name].type)


    def __remove_entities(self):
        for entity_name in self.__delete_entity:
            for map_name in self.__maps:
                if entity_name in self.getMap(map_name).entities:
                    del self.getMap(map_name).entities[entity_name]
                    

    
    def updateEntities(self):

        """Updates the entity. Pathfinding, picking up items"""

        if self.__isMap():
            entities_dict = self.getMap().entities

            for entity_name in entities_dict:
                self.__pathfindEntity(entity_name)

            self.__remove_entities()

            



    def drawEntities(self):

        """Draws all entities
        """

        if self.__isMap():
            current_map = self.getMap()

            visible_entity_list = []

            for entity_name in self.getMap().entities:
                entity_obj = self.getEntity(entity_name)
                map_pos = entity_obj.getMapPos()
                if self.__isMapPosVisable(current_map, map_pos, abs(entity_obj.draw_from_pos[0]), abs(entity_obj.draw_from_pos[1])):
                    visible_entity_list.append([entity_name, map_pos[1]])

            visible_entity_list = sorted(visible_entity_list, key=lambda x:x[1])
        
            for entity in visible_entity_list:
                self.getEntity(entity[0]).draw(self.__game_win, current_map.draw_from_pos)


    def setAnimation(self, animation_name: str, entity_name: str = None):

        """Sets the entities current animation
        """

        self.getEntity(entity_name).setCurrentAnimation(animation_name)


    def isEntityCollidepoint(self, map_pos: tuple, entity_name: str = None):

        """Returns whether entity collides with a point

        Returns:
            bool: entity collides with point
        """

        return self.getEntity(entity_name).isCollidepoint(map_pos)

    def isEntityCollide(self, entity_name_1: str, entity_name_2: str, collision_mask: bool = False):
        
        return self.getEntity(entity_name_1).isCollideEntity(self.getEntity(entity_name_2), collision_mask)

    def isEntityMouseCollision(self, entity_name: str = None) -> bool:

        """Returns whether entity collides with mouse

        Returns:
            bool: entity collides with mouse
        """

        return self.isEntityCollidepoint(self.getMapMousePos(), entity_name)


    ## ------  Camera  ------ ##

    def addCamera(self, camera_name: str, pos: tuple = (0, 0)):

        """Adds a new camera to the cameras dict
        """        

        self.__cameras[camera_name] = Camera(pos)

    def getCamera(self, camera_name: str = None) -> Camera:

        """Returns a camera stored in cameras dict from a camera name, 
        camera name == None will get current camera

        Returns:
            Camera: camera from cameras dict
        """        

        if camera_name == None:
            camera_name = self.__camera_name

        return self.__cameras[camera_name]


    def __getCameraScale(self, camera_name: str) -> float:

        """Returns a camera's scale value

        Returns:
            Camera: camera's scale
        """        
        
        return self.__cameras[camera_name].getScale()

    def updateCamera(self, force_update: bool = False):
        
        """Updates the camera's position and gets the visible chunks
        """        

        if self.__isMap():
            camera = self.getCamera()
            camera.updateCameraPos()

            if force_update or camera.isCameraPosChange():
                self.getMap().setVisableChunks(
                    camera.camera_pos,
                    self.__game_win_center_pos)


    def zoom(self, zoom_value: int, camera_name: str = None):

        """Changes the zoom of the camera. 
        zoom_value is added to original scale.
        """        

        zoom_value *= globalVar.dt

        while True:
            camera = self.getCamera(camera_name)

            camera.setOriginalScale(camera.getOriginalScale() + zoom_value)

            self.resizeGameWin()

            self.updateCamera(True)

            ## Allows for smooth zooming, stops jumping between pixles
            if ((self.__game_win_center_pos[0] - int(self.__game_win_center_pos[0]) < 0.5) and 
                (self.__game_win_center_pos[1] - int(self.__game_win_center_pos[1]) < 0.5)):
                break

            ## Adds zoom value until finds scale value that fits  ## PROABLEY NOT VERY EFFICIENT
            if zoom_value > 0:
                zoom_value += 0.001
            else:
                zoom_value -= 0.001


    def setZoom(self, zoom_value: int, camera_name: str = None):

        """Sets a camera's zoom
        """
        
        camera = self.getCamera(camera_name)

        if zoom_value != camera.getOriginalScale():

            camera.setOriginalScale(zoom_value)

            self.resizeGameWin()

            self.updateCamera(True)

            

    def moveCameraPos(self, x: int = 0, y: int = 0, camera_name: str = None):

        """Moves the camera's position
        """

        self.getCamera(camera_name).moveCameraPos(x, y)

    def setCameraTargetPos(self, pos: tuple, camera_name: str = None):

        """Sets camera's target position
        """

        self.getCamera(camera_name).setCameraTargetPos(pos)

    def setCameraFollowEntitiy(self, entity_name: str = None, camera_name: str = None):

        """Sets a camera to follow an entity
        """

        self.getCamera(camera_name).setCameraTargetPos(self.getEntity(entity_name).getMapPos())


    def setCameraPos(self, pos: tuple, camera_name: str = None):
        
        """Sets the camera's position
        """

        self.getCamera(camera_name).camera_pos = list(pos)

        self.updateCamera(True)


    def __draw_pixel_cursor(self):

        if self.pixel_cursor != None:
            pygame.draw.rect(
                self.__game_win, self.pixel_cursor, 
                (self.getGameMousePos()[0], self.getGameMousePos()[1], 1, 1))


    def draw(self, window: UI):

        """Draws game window on UI window
        """

        if window.resized == True:
            self.resizeGameWin()


        if self.background_colour != None:
            self.__game_win.fill(self.background_colour)
        
        self.__drawMap()

        self.drawEntities()

        self.__drawParticles()

        self.__drawTriggers()

        self.__draw_pixel_cursor()

        # surf = pySurface((self.__game_win_width, self.__game_win_height), pygame.SRCALPHA)
        # surf.set_colorkey((0,0,0))
        # surf.set_alpha(150)
        # pygame.draw.rect(surf, (1, 0, 0), (0, 0, self.__game_win_width, self.__game_win_height))


        # self.__game_win.blit(surf, (0, 0))

        ## Drawing game win on window
        # window.win.blit(self.__game_win, (0,0))
        window.win.blit(self.scaleGameWin(), (0, 0)) ## SCALING GAME_WIN HALVES FRAME RATE

        self.__drawFloatingText(window.win)


    def updateDraw(self, window: UI):

        """Updates and draws the Game
        """

        self.__saveOnExit()
        self.updateEntities()
        self.updateCamera()
        self.draw(window)