from pygame import Surface
from data.scripts.gfx.ImgParticle import ImgParticle
from data.scripts.basic import circleCoord
from random import uniform as randFloat, randint
import data.scripts.globalVar as globalVar
globalVar.init()

def randValue(value, float: bool = False):

    """Returns a random value if it's a tuple / list, otherwise returns 
    the value

    Returns:
        float | int  | Any: random value
    """

    if type(value) == tuple or type(value) == list:
        if float:
            return randFloat(value[0], value[1])
        else:
            return randint(value[0], value[1])
    else:
        return value

def getValue(value, float_value: bool = False, single_value: bool = False):

    """Returns a value for the particle

    Returns:
        Any: particle value
    """

    if value != None:
        if type(value) == list:
            if single_value:
                return randValue(value, float_value)
            else:
                return [randValue(value[0], float_value), randValue(value[1], float_value)]
        else:
            return value
    else:
        return None




class ParticleSpawner:

    """Spawns, draws & deletes particles.
    """

    def __init__(self, 
            spawner_pos: tuple,
            particle_type: str,
            max_particles: int,
            spawn: bool,
            timer: float,
            spawn_speed: float,
            spawn_amount: int,
            animation_name: str,
            num_frames: int,
            animation_speed: tuple,
            random_start_frame: bool,
            delete_animation: bool,
            pos: list, 
            target_pos: list, 
            relative_target: bool,
            target_vel: tuple, 
            exp_value: tuple,
            delete_target: bool, 
            velocity: list,
            change_vel: tuple,
            circular_spawn: bool,
            random_degree: bool,
            radius: float,
            circular_speed: float,
            angle: tuple,
            change_angle: tuple,
            inc_change_angle: tuple,
            alpha: tuple, 
            change_alpha: tuple,
            inc_change_alpha: tuple,
            delete_alpha: bool,
            stats: dict):

        self.particle_type = particle_type

        self.spawner_pos = spawner_pos
        self.__max_particles = max_particles
        self.spawn = spawn
        self.__spawn_speed = spawn_speed
        self.__spawn_amount = spawn_amount
        if self.__spawn_speed != None:
            self.__spawn_speed *= 60
        self.__spawn_timer = 0

        self.__animation_name = animation_name
        self.__num_frames = num_frames
        self.__animation_speed = animation_speed
        self.__random_start_frame = random_start_frame
        self.__delete_animation = delete_animation
        
        self.__pos = pos
        
        self.target_pos = target_pos
        self.__relative_target = relative_target
        self.__target_vel = target_vel
        self.__exp_value  = exp_value
        self.__delete_target = delete_target
        
        self.__velocity = velocity
        self.__change_vel = change_vel

        self.__circular_spawn = circular_spawn
        self.__random_degree = random_degree
        self.__radius = radius
        self.__circular_speed = getValue(circular_speed, True, True)
        self.__degree = 0

        self.__angle = angle
        self.__change_angle = change_angle
        self.__inc_change_angle = inc_change_angle
        
        self.__alpha  = alpha
        self.__change_alpha = change_alpha
        self.__inc_change_alpha = inc_change_alpha
        self.__delete_alpha = delete_alpha

        self.__stats = stats
        
        self.__particle_list = []
        self.__delete_list = []

        self.__delete_timer = timer
        if self.__delete_timer != None:
            self.__delete_timer *= 60
        self.__timer = 0
        self.delete = False


    def addParticle(self):

        """Adds a particle to the particle list.
        """

        if self.spawn:
            for _ in range(self.__spawn_amount):
                
                pos = getValue(self.__pos)
                if pos != None:
                    pos = [
                        self.spawner_pos[0] + pos[0], 
                        self.spawner_pos[1] + pos[1]]

                if self.__circular_spawn:

                    if self.__random_degree:
                        degree = randFloat(0, 360)
                    else:
                        degree = self.__degree
                    
                    target_pos = list(circleCoord(
                        getValue(self.__radius, True, True), 
                        degree))
                
                else:
                    target_pos = getValue(self.target_pos)
                
                
                if target_pos != None:
                    if self.__relative_target:
                        target_pos = [
                                    pos[0] + target_pos[0], 
                                    pos[1] + target_pos[1]]
                    
                    elif self.__circular_spawn and self.target_pos != None:
                                target_pos = [
                                    target_pos[0] + getValue(self.target_pos[0], False, True), 
                                    target_pos[1] + getValue(self.target_pos[1], False, True)]

                start_frame = 1
                
                if self.__random_start_frame:
                    start_frame = randint(start_frame, self.__num_frames)

                self.__particle_list.append(ImgParticle(
                    self.__animation_name,
                    self.__num_frames,
                    getValue(self.__animation_speed, True, True),
                    start_frame,
                    self.__delete_animation,
                    pos, 
                    target_pos, 
                    getValue(self.__target_vel, True), 
                    getValue(self.__exp_value, True, True), 
                    self.__delete_target,
                    getValue(self.__velocity, True),
                    getValue(self.__change_vel, True),
                    getValue(self.__angle, True, True),
                    getValue(self.__change_angle, True, True),
                    getValue(self.__inc_change_angle, True, True),
                    getValue(self.__alpha, True, True), 
                    getValue(self.__change_alpha, True, True),
                    getValue(self.__inc_change_alpha, True, True),
                    self.__delete_alpha
                ))


    def __setCircularMovement(self):

        """Sets a new particles target pos in a circular motion
        """

        if self.__circular_spawn and not self.__random_degree:

            self.__degree += self.__circular_speed * globalVar.dt
            
            if self.__degree > 360:
                self.__degree = self.__degree - 360
            elif self.__degree < 0:
                self.__degree = self.__degree + 360


    def __spawnTimer(self):

        """Checks when new particle should be spawned
        """

        if self.__spawn_speed != None:
            if self.__spawn_timer > self.__spawn_speed:
                
                self.addParticle()
                self.__spawn_timer = 0
            
            else:
                self.__spawn_timer += 1 * globalVar.dt
        else:
            self.addParticle()

    
    def __deleteTimer(self):

        """Deletes the particle spawner after a set time
        """

        if self.__delete_timer != None:

            self.__timer += 1 * globalVar.dt
    
            if self.__timer >= self.__delete_timer:
                self.delete = True



    def draw(self, 
            surf: Surface, 
            draw_from_pos: tuple, 
            game_win_width: int, 
            game_win_height: int,
            update: bool = True):

        """Draws all particles in particle list.
        """

        for particle in self.__particle_list:
            
            delete_particle = particle.draw(
                    surf,
                    draw_from_pos,
                    game_win_width,
                    game_win_height, 
                    update)
            
            if delete_particle:
                self.__delete_list.append(particle)

        if update:
            self.__setCircularMovement()
            self.__deleteTimer()

            for particle in self.__delete_list:
                self.__particle_list.remove(particle)

            self.__delete_list = []

            if self.__max_particles != None:
                if len(self.__particle_list) < self.__max_particles:
                    self.__spawnTimer()
            else:
                self.__spawnTimer()