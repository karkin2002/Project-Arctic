from pygame import Surface, mask, Vector2
from data.scripts.UI.printInfo import printInfo

from data.scripts.basic import createMask, isMaskCollision, isMaskCollidepoint
from data.scripts.UI.saveLoadData import makeDir, loadImgPath
from data.scripts.gfx.Animation import Animation

import data.scripts.globalVar as globalVar
globalVar.init()

class Entity:

    """Entity superclass used for entities that can be drawn on game map
    """

    __ENTITY_TEXTURE_FOLDER_PATH = "data/images/textures/entity/{entity_name}/"
    __COLLISION_MAP_FILENAME = "{entity_name}_collision_map"
    __VELOCITY_STAT_NAME = "velocity"
    __loaded_animations = []
    
    def __init__(self, 
            name: str,
            type: str, 
            pos: tuple, 
            collision_range: int = 2, 
            animations: dict = {},
            defult_animation = None,
            stats: dict = {}):

        self.name = name
        
        self.type = type
        
        self.__animations = {}

        ##  ------ Texture ------  ##
        if self.type not in self.__loaded_animations:
            loadImgPath(self.__ENTITY_TEXTURE_FOLDER_PATH.format(
                entity_name = self.type))

            for animation_name in animations:
                animation_path = self.__ENTITY_TEXTURE_FOLDER_PATH.format(
                    entity_name = self.type) + f"{animation_name}/"
                
                makeDir(animation_path)
                
                loadImgPath(animation_path, True)

                self.__addAnimation(
                    animation_name, 
                    animations[animation_name][0],
                    animations[animation_name][1],
                    animations[animation_name][2])
            
            self.__loaded_animations.append(self.type)

            globalVar.mask_dict[self.type] = createMask(globalVar.getImage(self.type))
        
        else:
            for animation_name in animations:
                self.__addAnimation(
                    animation_name, 
                    animations[animation_name][0],
                    animations[animation_name][1],
                    animations[animation_name][2])

        self.defult_animation = defult_animation
        self.current_animation = self.defult_animation

        entity_texture = globalVar.getImage(self.type)
        self.width = entity_texture.get_width()
        self.height = entity_texture.get_height()
        

        ##  ------ Movement stuff ------ ##
        self.draw_from_pos = (
                -(entity_texture.get_width() / 2), 
                -entity_texture.get_height())

        self.pos = Vector2(
                pos[0] + self.draw_from_pos[0], 
                pos[1] + self.draw_from_pos[1])

        self.path = []


        ##  ------ Collision stuff ------  ##
        collision_map_texture_name = self.__COLLISION_MAP_FILENAME.format(entity_name = self.type)
        if globalVar.isImage(collision_map_texture_name):
            self.mask = createMask(globalVar.getImage(collision_map_texture_name))
        
        else:
            self.mask = createMask(entity_texture)

        self.mask_dimensions = self.mask.get_size()

        

        self.COLLISION_RANGE = collision_range


        ##  ------ Stats / Inventory -------  ##

        self.__loadStats(stats)

        self.__inventory = {}


    def isItem(self, item_name: str) -> bool:

        """Returns whether item in inventory

        Returns:
            bool: item in inventory
        """

        return item_name in self.__inventory


    def addItem(self, item_name: str):

        """Adds item to inventory"""

        if self.isItem(item_name):
            self.__inventory[item_name] += 1

        else:
            self.__inventory[item_name] = 1


    def getItemAmount(self, item_name: str) -> int:

        """Returns amount of item in inventory

        Returns:
            int: amount of item
        """


        if self.isItem(item_name):
            return self.__inventory[item_name]
        else:
            return 0

    
    def removeItem(self, item_name: str, amount: int = 1) -> bool:

        """Removes item from inventory

        Returns:
            bool: item removed
        """

        if self.isItem(item_name):
            
            if self.getItemAmount(item_name) > 0:
                if amount >= self.getItemAmount(item_name):
                    del self.__inventory[item_name]
                
                else:
                    self.__inventory[item_name] -= amount

                return True
        
        return False




    def __loadStats(self, stats_dict: dict):
        self.__stats = {}

        for stat_name in stats_dict:

            if self.type in stats_dict[stat_name]:
                self.__stats[stat_name] = stats_dict[stat_name][self.type]
            else:
                self.__stats[stat_name] = stats_dict[stat_name]["all"]

        
        if self.__VELOCITY_STAT_NAME in self.__stats:
            self.__velocity = self.__stats[self.__VELOCITY_STAT_NAME]
        else:
            self.__velocity = 1.5

    def isStat(self, stat_name: str) -> bool:

        """Returns weather a stat exists

        Returns:
            _type_: _description_
        """

        if stat_name in self.__stats:
            return True
        
        else:
            printInfo("Error", f"'{stat_name}' doesn't exist for {self.type}")
            return False


    def setStat(self, stat_name: str, value):

        """Sets an entity stat
        """

        if self.isStat(stat_name):
            self.__stats[stat_name] = value
    
    def  getStat(self, stat_name: str):

        """Returns the stat from its stat name

        Returns:
            Any: entity stat
        """

        if self.isStat(stat_name):
            return self.__stats[stat_name]



    def __addAnimation(self, 
            animation_name: str, 
            num_frames: int, 
            animation_speed: float, 
            force_animation: bool):

        """Adds an animation obj to animations dict
        """

        self.__animations[animation_name] = Animation(
            f"{self.type}_{animation_name}", 
            num_frames, 
            animation_speed,
            force_animation)

    def __getAnimation(self, animation_name: str) -> Animation:

        """Returns an animation obj from animations

        Returns:
            Animation: Animation
        """

        return self.__animations[animation_name]
        
    def __getCurrentAnimation(self) -> Animation:

        """Returns animation obj of current animation

        Returns:
            Animation: current animation obj
        """

        return self.__getAnimation(self.current_animation)

    def setCurrentAnimation(self, animation_name: str):
        
        """Sets the current animation
        """

        if animation_name in self.__animations:
            if self.__getCurrentAnimation().force_animation:
                if not self.__getCurrentAnimation().playing:
                    self.current_animation = animation_name
                    self.__getCurrentAnimation().playing = True
            else:
                self.current_animation = animation_name
                self.__getCurrentAnimation().playing = True


        
        else:
            printInfo("Error", f"'{animation_name}' animation doesn't exist for {self.type}")

    def getCurrentAnimationMask(self) -> mask:

        """Returns current animation mask

        Returns:
            mask: current animation
        """

        if self.current_animation != None:
            return globalVar.getMask(self.__getCurrentAnimation().getImgName())
        
        else:
            return globalVar.getMask(self.type)


    def isCollidepoint(self, map_pos: tuple) -> bool:
        
        """Returns whether the entities current animation mask collides with a point

        Returns:
            bool: entity collide with point
        """

        return isMaskCollidepoint(
            self.getCurrentAnimationMask(), 
            self.pos, 
            map_pos)


    def isCollideMask(self, mask_obj: mask, pos: tuple, collision_mask: bool = False) -> bool:

        """Returns whether entity mask collsides with another mask

        Returns:
            bool: collidies with mask
        """

        if collision_mask:
            return isMaskCollision(
                self.mask, self.pos, 
                mask_obj, pos)

        else:
            return isMaskCollision(
                self.getCurrentAnimationMask(), self.pos, 
                mask_obj, pos)


    def isCollideEntity(self, entity_obj, collision_mask: bool = False) -> bool:
        
        """Returns whether entity obj has collided with this entity

        Returns:
            bool: collision
        """
        
        if collision_mask:
            return self.isCollideMask(
                entity_obj.mask, 
                entity_obj.pos,
                collision_mask)
        
        else:
            return self.isCollideMask(
                entity_obj.getCurrentAnimationMask(), 
                entity_obj.pos,
                collision_mask)




    ## collision_mask_list = [[mask, (x, y)], [mask, (x, y)]]
    def __isTileCollision(self, mask_collision_list: list, new_pos: tuple) -> bool:

        """Returns whether a new position will lead to a collision

        Returns:
            bool: is there a collision
        """

        collision = False

        for collision_mask in mask_collision_list:
            if isMaskCollision(
                    self.mask, new_pos, 
                    collision_mask[0], collision_mask[1]):

                collision = True
                break

        return collision


    def moveTowards(self, target_pos: Vector2, mask_collision_list: list = [], stopping_distance = 1):
        if abs(self.getMapPos()[1] - target_pos[1]) > stopping_distance or abs(self.getMapPos()[0] - target_pos[0]) > stopping_distance:
            self.move(
                mask_collision_list,
                up = abs(self.getMapPos()[1] - target_pos[1]) > stopping_distance and self.getMapPos()[1] > target_pos[1],
                down = abs(self.getMapPos()[1] - target_pos[1]) > stopping_distance and self.getMapPos()[1] < target_pos[1],
                left = abs(self.getMapPos()[0] - target_pos[0]) > stopping_distance and self.getMapPos()[0] > target_pos[0],
                right = abs(self.getMapPos()[0] - target_pos[0]) > stopping_distance and self.getMapPos()[0] < target_pos[0],
            )
        else:
            self.setCurrentAnimation(self.defult_animation)



    def move(self, 
            mask_collision_list: list = [],
            up: bool = False, 
            down: bool = False, 
            left: bool = False,
            right: bool = False):

        """Moves entity
        """

        if up or down or right or left:
            target_pos = Vector2(self.pos[:])

            if up:
                if not self.__isTileCollision(
                        mask_collision_list, 
                        (self.pos[0], 
                        self.pos[1] - self.__velocity * globalVar.dt)):
                
                    target_pos[1] -= self.__velocity * globalVar.dt

                self.setCurrentAnimation("up")
            
            elif down:
                if not self.__isTileCollision(
                        mask_collision_list, 
                        (self.pos[0], 
                        self.pos[1] + self.__velocity * globalVar.dt)):
                    
                    target_pos[1] += self.__velocity * globalVar.dt

                self.setCurrentAnimation("down")
            
            
            if left:
                if not self.__isTileCollision(
                        mask_collision_list, 
                        (self.pos[0] - self.__velocity * globalVar.dt, 
                        self.pos[1])):

                    target_pos[0] -= self.__velocity * globalVar.dt

                self.setCurrentAnimation("left")
            
            elif right:
                if not self.__isTileCollision(
                        mask_collision_list, 
                        (self.pos[0] + self.__velocity * globalVar.dt, 
                        self.pos[1])):

                    target_pos[0] += self.__velocity * globalVar.dt

                self.setCurrentAnimation("right")

            self.pos = self.pos.move_towards(target_pos, self.__velocity * globalVar.dt)
        else:
            self.setCurrentAnimation(self.defult_animation)



    def pathfind(self, tile_size: int, mask_collision_list: list = []):
        
        if len(self.path) > 0:
            
            target_pos = (
                (self.path[0][0] * tile_size) + tile_size / 2, 
                (self.path[0][1] * tile_size) + tile_size / 2)

            map_pos = self.getMapPos()

            if int(map_pos[1]) > target_pos[1]:
                self.move(mask_collision_list, up = True)

            elif int(map_pos[1]) < target_pos[1]:
                self.move(mask_collision_list, down = True)
            
            if int(map_pos[0]) > target_pos[0]:
                self.move(mask_collision_list, left = True)

            elif int(map_pos[0]) < target_pos[0]:
                self.move(mask_collision_list, right = True)

            if self.getTilePos(tile_size) == self.path[0]:
                self.path.remove(self.path[0])

                if len(self.path) == 0:
                    self.move()
                

            



        


    def getMapPos(self) -> tuple:

        """Returns the entities position on the map

        Returns:
            tuple: map position
        """

        return (self.pos[0] + abs(self.draw_from_pos[0]), 
                self.pos[1] + abs(self.draw_from_pos[1]))

    def setMapPos(self, pos: tuple):

        """Sets the entities position on the map
        """

        self.pos = Vector2(
            pos[0] + self.draw_from_pos[0], 
            pos[1] + self.draw_from_pos[1])

    
    def getTilePos(self, tile_size: int) -> tuple:

        """Returns the entities position in terms of tiles

        Returns:
            tuple: tile position
        """

        return (int(self.getMapPos()[0] / tile_size), 
                int(self.getMapPos()[1] / tile_size))


    def draw(self, surf: Surface, draw_from_pos: tuple):

        """Draws Entity
        """

        if self.current_animation == None:
            surf.blit(
                globalVar.getImage(self.type), 
                (draw_from_pos[0] + self.pos[0], 
                draw_from_pos[1] + self.pos[1]))
        else:
            
            surf.blit(
                self.__getCurrentAnimation().getImg(), 
                (draw_from_pos[0] + self.pos[0], 
                draw_from_pos[1] + self.pos[1]))
            
            self.__getCurrentAnimation().updateCurrentFrame()