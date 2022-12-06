from data.scripts.basic import exponential, circleCoord

import data.scripts.globalVar as globalVar
globalVar.init()

class Particle:

    """A parent particle class
    """

    __MAX_TARGET_POS_DIF = 1

    def __init__(self, 
            pos: list, 
            target_pos: tuple, 
            target_vel: float, 
            exp_value: float, 
            delete_target: bool,
            velocity: tuple,
            change_vel: tuple,
            angle: float,               ## Angle
            change_angle: float,        ## How much the angle is changing by
            inc_change_angle: float,    ## How much the change angle value is increasing by
            alpha: float,               ## Alpha
            change_alpha: float,        ## How much the alpha is changed by
            inc_change_alpha: float,    ## How much the change alpha value is increased by
            delete_alpha: bool):        ## Whether the particle is deleted after alpha hits 0

        self._pos = pos

        self.__target_pos = target_pos
        self.__target_vel = target_vel
        self.__exp_value = exp_value
        self.__delete_target = delete_target

        self.__velocity = velocity
        self.__change_vel = change_vel

        self._angle = angle
        self._last_angle = None
        self.__change_angle = change_angle
        self.__inc_change_angle = inc_change_angle

        self._alpha = alpha
        self._last_alpha = None
        self.__change_alpha = change_alpha
        self.__inc_change_alpha = inc_change_alpha
        self.__delete_alpha = delete_alpha

        self._delete = False


    def _setTarget(self):

        """Moves the particle based on target pos.
        """        

        if self.__target_pos != None:

            for i in range (2):
                if self._pos[i] != self.__target_pos[i]:
                    self._pos[i] = exponential(
                        self._pos[i], 
                        self.__target_pos[i], 
                        self.__target_vel, 
                        self.__exp_value, 
                        globalVar.dt)

                    if abs(self._pos[i] - self.__target_pos[i]) < self.__MAX_TARGET_POS_DIF:
                        self._pos[i] = self.__target_pos[i]


            if self.__delete_target and self._pos == self.__target_pos:
                self._delete = True
                

    def _setVelocity(self):
        
        """Moves the particle based on velocity.
        """  

        if self.__velocity != None:
            self._pos[0] += self.__velocity[0] * globalVar.dt
            self._pos[1] += self.__velocity[1] * globalVar.dt
    

    def _addVelocity(self):

        """Adds change_vel to volcity
        """    

        if self.__velocity != None and self.__change_vel != None:
            self.__velocity[0] += self.__change_vel[0] * globalVar.dt
            self.__velocity[1] += self.__change_vel[1] * globalVar.dt

    
    def _addAlpha(self):

        """Adds change_alpha value to alpha value
        """

        self._last_alpha = round(self._alpha)

        if self.__change_alpha != None and self.__change_alpha != 0:
            self._alpha += self.__change_alpha * globalVar.dt

            if self._alpha < 0:
                self._alpha = 0
                
                if self.__delete_alpha:
                    self._delete = True
            
            elif self._alpha > 255:
                self._alpha = 255

        self.__addChangeAlpha()

    
    def __addChangeAlpha(self):
        
        """Adds inc_change_alpha value to alpha value
        """

        if self.__inc_change_alpha != None and self.__inc_change_alpha != 0:
            self.__change_alpha += self.__inc_change_alpha * globalVar.dt


    def _addAngle(self):

        """Adds change_angle value to angle value
        """

        self._last_angle = round(self._angle)

        if self.__change_angle != None and self.__change_angle != 0:
            self._angle += self.__change_angle * globalVar.dt

        self.__addChangeAngle()

    
    def __addChangeAngle(self):
        
        """Adds inc_change_angle value to angle value
        """

        if self.__inc_change_angle != None and self.__inc_change_angle != 0:
            self.__change_angle += self.__inc_change_angle * globalVar.dt