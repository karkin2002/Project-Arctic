from pygame import Rect, Surface, draw, mask
from data.scripts.entity.Entity import Entity
from data.scripts.basic import createMask, isMaskCollision

class Trigger:

    """Trigger can trigger events when an entity passes ontop of it
    """
    
    def __init__(self,  
            pos: tuple, 
            dimensions: tuple,
            location: tuple = None,
            map_name: str = None,
            trigger: bool = True):
        
        self.pos = pos
        self.dimensions = dimensions
        self.__createMask()

        self.trigger = trigger
        self.triggered = []

        self.location = location
        self.map_name = map_name


    def __createMask(self):
        
        """Creates a mask for the teleporter collisions
        """
        
        temp_surf = Surface(self.dimensions)
        
        draw.rect(
            temp_surf,
            (255, 0, 0),
            (0, 0, self.dimensions[0], self.dimensions[1]))

        self.__mask = createMask(temp_surf)

    
    def isTrigger(self, entity_name: str) -> bool:

        """Returns whether an entity has triggered

        Returns:
            bool: entity triggered
        """

        return entity_name in self.triggered

    def __addTrigger(self, entity_name: str):

        """Adds entity name to triggered list
        """

        if entity_name not in self.triggered:
            self.triggered.append(entity_name)

    def __removeTrigger(self, entity_name: str):

        """Removes entity name from triggered
        """

        if entity_name in self.triggered:
            self.triggered.remove(entity_name)
        


    def isCollision(self, entity_obj: Entity) -> bool:

        """Returns whether the teleporter collides with a mask

        Returns:
            bool: collides with mask
        """
        
        if self.trigger:
            if isMaskCollision(
                    self.__mask, 
                    self.pos, 
                    entity_obj.mask, 
                    entity_obj.pos):
                
                self.__addTrigger(entity_obj.name)
                
                self.__teleport(entity_obj)
                return True

        self.__removeTrigger(entity_obj.name)
        return False


    def __teleport(self, entity_obj: Entity):

        """Teleports entity to location
        """

        if self.location != None:
            entity_obj.setMapPos(self.location)
        

    def draw(self, surf: Surface, draw_from_pos: tuple):

        """Draws the teleporter
        """

        draw.rect(
            surf, 
            (255, 0, 0), 
            (self.pos[0] + draw_from_pos[0], 
            self.pos[1] + draw_from_pos[1], 
            self.dimensions[0], 
            self.dimensions[1]), 
            1)
        