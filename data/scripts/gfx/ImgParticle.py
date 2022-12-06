from pygame import Surface
from data.scripts.entity.Entity import Entity
from data.scripts.gfx.Particle import Particle
from data.scripts.gfx.Animation import Animation
from data.scripts.basic import alphaSurf, rotSurf
from data.scripts.basic import createMask, isMaskCollision, isMaskCollidepoint

import data.scripts.globalVar as globalVar
globalVar.init()

class ImgParticle(Particle):
    
    """Particle using image / animation using images
    """

    def __init__(self, 
            animation_name: str,
            num_frames: int,
            animation_speed: float,
            start_frame: int,
            delete_animation: bool,
            pos: list, 
            target_pos: tuple, 
            target_vel: float, 
            exp_value: float, 
            delete_target: bool,
            velocity: tuple,
            change_vel: tuple,
            angle: float,
            change_angle: float,
            inc_change_angle: float,
            alpha: float, 
            change_alpha: float,
            inc_change_alpha: float,
            delete_alpha: bool):

        super().__init__(pos, 
            target_pos, 
            target_vel, 
            exp_value,
            delete_target, 
            velocity, 
            change_vel, 
            angle,
            change_angle,
            inc_change_angle,
            alpha, 
            change_alpha,
            inc_change_alpha,
            delete_alpha)

        self.__animation = Animation(
            animation_name, 
            num_frames, 
            animation_speed)
        self.__animation.current_frame = start_frame
        self.__animation.playing = True

        self.__delete_animation = delete_animation

        self.__last_animaton_name = None
        self.__current_animation_name = self.__animation.getImgName()
        self.__setCurrentAnimation()

    def __setCurrentAnimation(self, visible: bool = True, force: bool = False):

        """Sets the current animation surface
        """

        if (
            visible and (
            self._last_alpha != round(self._alpha) or
            self._last_angle != round(self._angle) or
            force == True)
        ):

            self.__current_animation, self.__center = rotSurf(
                self.__animation.getImg(), self._angle)

            self.__current_animaton = alphaSurf(
                self.__current_animation, self._alpha)

    def __updateAnimation(self, visible: bool = True):

        """Updates the animation
        """

        self.__last_animaton_name = self.__current_animation_name
        self.__current_animation_name = self.__animation.getImgName()
        
        if self.__last_animaton_name != self.__current_animation_name:
            self.__setCurrentAnimation(visible, True)
        
        else:
            self.__setCurrentAnimation(visible)


        if self.__delete_animation and self.__animation.playing == False:
            self._delete = True

        self.__animation.updateCurrentFrame()

    def __isVisible(self, 
            draw_from_pos: tuple, 
            game_win_width: int, 
            game_win_height: int):

        return ((draw_from_pos[0] + self._pos[0]) < (game_win_width + self.__center[0]) and
                (draw_from_pos[0] + self._pos[0]) > -abs(self.__center[0]) and
                (draw_from_pos[1] + self._pos[1]) < (game_win_height + self.__center[1]) and 
                (draw_from_pos[1] + self._pos[1]) > -abs(self.__center[0]))


    def __isCollide(self, entity_obj: Entity, particle_pos: tuple):
        if isMaskCollision(
                entity_obj.getCurrentAnimationMask(), entity_obj.pos,
                globalVar.getMask(self.__current_animation_name), particle_pos):
            
            print(True)

        

    def __update(self, visible: bool) -> bool:

        """Updates the particle, returns whether the particle should be deleted

        Returns:
            bool: particle should be deleted
        """

        self._setTarget()
        self._setVelocity()
        self._addVelocity()
        self._addAngle()
        self._addAlpha()
        self.__updateAnimation(True)

        return self._delete


    def draw(self, 
            surf: Surface, 
            draw_from_pos: tuple,
            game_win_width: int, 
            game_win_height: int,
            update: bool = True) -> bool:

        """Draws particle on surface & updates particle if update is True,
        returns whether the particle should be deleted

        Returns:
            bool: particle should be deleted
        """

        visible = self.__isVisible(draw_from_pos, game_win_width, game_win_height)

        if visible:
            if self._alpha > 0:
                surf.blit(
                    self.__current_animaton, 
                    (round(draw_from_pos[0] + (self._pos[0] - self.__center[0])), 
                    round(draw_from_pos[1] + (self._pos[1] - self.__center[0]))))

        if update:
            return self.__update(visible)

        return False
        