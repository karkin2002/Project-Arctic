from pickle import TRUE
import data.scripts.globalVar as globalVar 
from data.scripts.basic import exponential
from random import uniform
globalVar.init()

class Camera:

    """Class for camera used for game
    """

    def __init__(self,
            pos: tuple = (0, 0),
            scale: float = 4,
            velocity: float = 0.1, 
            exp_value: float = 2,
            shake_distance: float = 2,
            time_between_shakes: float = 2):

        self.camera_pos = list(pos)
        self.__last_camera_pos = list(pos)
        self.__camera_target_pos = list(pos)
        self.__velocity = velocity
        self.__exp_value = exp_value

        self.__screen_shake = False
        self.__shake_distance = shake_distance
        self.__time_between_shakes = time_between_shakes
        self.__screen_shake_timer = 0

        self.__original_scale = scale
        self.__scale = self.__original_scale


    def setCameraTargetPos(self, pos: list):

        """Sets the camera's target position
        """        

        self.__camera_target_pos = pos

        self.__setCameraPos()




    def moveCameraPos(self, x: int, y: int):

        """Moves the camera's position (adds or minus from camera's pos)
        """        

        self.camera_pos[0] += x * globalVar.dt
        self.camera_pos[1] += y * globalVar.dt


    def setScale(self):

        """Sets the scale based on the original scale value and 
        windows size diffence
        """        

        self.__scale = self.__original_scale * globalVar.win_scale


    def getScale(self) -> float:

        """Retunrs camera's scale

        Returns:
            float: Camera's scale
        """        

        return self.__scale


    def setOriginalScale(self, scale: int):

        """Sets original scale for camera (zoom value)
        """        

        if scale >= 1:
            self.__original_scale = scale
        
        else:
            self.__original_scale = 1

        
    def getOriginalScale(self) -> int:

        """Returns original scale

        Returns:
            int: original scale
        """   

        return self.__original_scale


    ## ------  Camera Movement  ------ ##

    def __screenShake(self):

        """Shakes the screen by moving the camera's position
        """        

        if self.__screen_shake:
            if self.__screen_shake_timer >= self.__time_between_shakes:
                for i in range(0,2):
                    self.camera_pos[i] += uniform(-self.__shake_distance,
                                                self.__shake_distance)
                self.__screen_shake_timer = 0

            self.__screen_shake_timer += 1 * globalVar.dt


    def __setCameraPos(self):

        """Sets the camera's position based on thr target camera position
        """        

        for i in range(0,2):
            self.__last_camera_pos[i] = self.camera_pos[i]

            if self.camera_pos[i] != None: 

                self.camera_pos[i] = exponential(self.camera_pos[i], 
                                                   int(self.__camera_target_pos[i]),
                                                   self.__velocity, 
                                                   self.__exp_value, 
                                                   globalVar.dt)



    def isCameraPosChange(self) -> bool:

        """Returns whether the cameras position has changed

        Returns:
            bool: has cameras position changed
        """

        return (round(self.__last_camera_pos[0]) != round(self.camera_pos[0]) or 
                round(self.__last_camera_pos[1]) != round(self.camera_pos[1]))


    def updateCameraPos(self):

        """Updates the camera's position
        """      
        
        self.__screenShake()
