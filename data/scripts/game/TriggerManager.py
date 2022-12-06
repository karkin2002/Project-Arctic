
from pygame import Surface
from data.scripts.game.Trigger import Trigger
from data.scripts.entity import Entity

class TriggerManager:

    """Manages all triggers
    """

    def __init__(self, display: bool = False):
        self.__triggers = {}

        self.__display = display

    def addTrigger(self, 
            name: str, 
            pos: tuple, 
            dimensions: tuple, 
            location: tuple = None,
            map_name: str = None,
            trigger: bool = True):

        """Adds a trigger to the triggers dict
        """
        
        self.__triggers[name] = Trigger(
            pos, dimensions, location, map_name, trigger)

    def checkTriggers(self, entity_obj: Entity) -> str:

        """Checks whether an entity has hit a trigger

        Returns:
            str: map name entity should be sent to
        """        
    
        for trigger_name in self.__triggers:
            if self.__triggers[trigger_name].isCollision(entity_obj):
                return self.__triggers[trigger_name].map_name

    def isTrigger(self, trigger_name: str, entity_name: str) -> bool:

        """Returns whether an entity has triggered a trigger

        Returns:
            bool: triggered
        """

        if trigger_name in self.__triggers:
            return self.__triggers[trigger_name].isTrigger(entity_name)
        else:
            return False

    
    def getTriggerSaveData(self):
        trigger_dict = {}

        for trigger_name in self.__triggers:
            trigger_dict[trigger_name] = {
                "pos": self.__triggers[trigger_name].pos,
                "dimensions": self.__triggers[trigger_name].dimensions,
                "location": self.__triggers[trigger_name].location,
                "map_name": self.__triggers[trigger_name].map_name,
                "trigger": self.__triggers[trigger_name].trigger}
        
        return trigger_dict


    def loadTriggerSaveData(self, trigger_data: dict):

        """Loads triggers from trigger save data
        """

        for trigger_name in trigger_data:
            self.addTrigger(
                trigger_name,
                trigger_data[trigger_name]["pos"],
                trigger_data[trigger_name]["dimensions"],
                trigger_data[trigger_name]["location"],
                trigger_data[trigger_name]["map_name"],
                trigger_data[trigger_name]["trigger"]
            )



    def draw(self, surf: Surface, draw_from_pos: tuple):

        """Draws all triggers
        """

        if self.__display:
            for trigger_name in self.__triggers:
                self.__triggers[trigger_name].draw(surf, draw_from_pos)