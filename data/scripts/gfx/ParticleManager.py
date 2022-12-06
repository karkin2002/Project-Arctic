from pygame import Surface
from data.scripts.UI.printInfo import printInfo
from data.scripts.gfx.ParticleSpawner import ParticleSpawner
from data.scripts.UI.saveLoadData import loadData, loadImgPath, makeDir, saveData
from data.scripts.basic import createMask

import data.scripts.globalVar as globalVar
globalVar.init()

class ParticleManager:

    """Manages all particle spawners
    """

    __PARTICLE_PROPERTIES_PATH = "data/config/particle_properties.json"

    __PARTICLE_IMAGE_FOLDER_PATH = "data/images/textures/particle/{animation_name}/"

    __DEFULT_PARTICLE_PROPERTY = {
        "max_particles": None,
        "spawn": True,
        "timer": None,
        "spawn_speed": None,
        "spawn_amount": 1,
        "animation_name": "particle_animation",
        "num_frames": 0,
        "animation_speed": 0.1,
        "random_start_frame": False,
        "delete_animation": False,
        "pos": [0, 0], 
        "target_pos": None, 
        "relative_target": True,
        "target_vel": 0.1, 
        "exp_value": 10, 
        "delete_target": False,
        "velocity": None,
        "change_vel": None,
        "circular_spawn": False, 
        "random_degree": False,
        "radius": 30,
        "circular_speed": 0.1,
        "angle": 0,
        "change_angle": None,
        "inc_change_angle": None,
        "alpha": 255, 
        "change_alpha": None,
        "inc_change_alpha": None,
        "delete_alpha": False,
        "stats": {}
    }

    __loaded_animations = []


    def __init__(self):
        self.__loadParticleProperties()

        self.__particle_spawners = {}

    def __loadParticleProperties(self):

        """Loads the particle properties
        """

        self.__particle_properties = loadData(self.__PARTICLE_PROPERTIES_PATH)

        for particle_name in self.__particle_properties:

            animation_name = self.__getParticleProperty(particle_name, "animation_name")

            if animation_name not in self.__loaded_animations:

                particle_image_folder = self.__PARTICLE_IMAGE_FOLDER_PATH.format(
                    animation_name = animation_name)

                makeDir(particle_image_folder)

                particle_animation = loadImgPath(particle_image_folder)

                for image_name in particle_animation:
                    globalVar.mask_dict[image_name] = createMask(
                        globalVar.getImage(image_name))

                self.__loaded_animations.append(animation_name)


    def addParticleSpawnerProperties(self, 
            particle_name: str,
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

        
        self.__particle_spawners[particle_name] = ParticleSpawner(
            spawner_pos,
            particle_type,
            max_particles,
            spawn,
            timer,
            spawn_speed,
            spawn_amount,
            animation_name,
            num_frames,
            animation_speed,
            random_start_frame,
            delete_animation,
            pos, 
            target_pos, 
            relative_target,
            target_vel, 
            exp_value, 
            delete_target,
            velocity,
            change_vel,
            circular_spawn,
            random_degree,
            radius,
            circular_speed,
            angle,
            change_angle,
            inc_change_angle,
            alpha, 
            change_alpha,
            inc_change_alpha,
            delete_alpha,
            stats
        )

    def __isParticle(self, particle_name: str) -> bool:
        if particle_name in self.__particle_properties:
            return True
        else:
            printInfo("Error", f"'{particle_name}' particle doesn't exist")
            return False

    def __isParticleProperty(self, particle_name: str, property_name: str) -> bool:
        if property_name in self.__particle_properties[particle_name]:
            return True
        else:
            printInfo("Error", f"'[{particle_name}][{property_name}]' particle property doesn't exist")
            return False

    def __getParticleProperty(self, particle_name: str, property_name: str):
        if not self.__isParticleProperty(particle_name, property_name):
            self.__particle_properties[particle_name][property_name] = self.__DEFULT_PARTICLE_PROPERTY[property_name]
            saveData(self.__PARTICLE_PROPERTIES_PATH, self.__particle_properties, True)
            
        return self.__particle_properties[particle_name][property_name]



    
    def addParticleSpawner(self, name: str, pos: tuple, particle_type: str):
        if self.__isParticle(particle_type):

            self.addParticleSpawnerProperties(
                name,
                list(pos),
                particle_type,
                self.__getParticleProperty(particle_type, "max_particles"),
                self.__getParticleProperty(particle_type, "spawn"),
                self.__getParticleProperty(particle_type, "timer"),
                self.__getParticleProperty(particle_type, "spawn_speed"),
                self.__getParticleProperty(particle_type, "spawn_amount"),
                self.__getParticleProperty(particle_type, "animation_name"),
                self.__getParticleProperty(particle_type, "num_frames"),
                self.__getParticleProperty(particle_type, "animation_speed"),
                self.__getParticleProperty(particle_type, "random_start_frame"),
                self.__getParticleProperty(particle_type, "delete_animation"),
                self.__getParticleProperty(particle_type, "pos"),
                self.__getParticleProperty(particle_type, "target_pos"),
                self.__getParticleProperty(particle_type, "relative_target"),
                self.__getParticleProperty(particle_type, "target_vel"),
                self.__getParticleProperty(particle_type, "exp_value"),
                self.__getParticleProperty(particle_type, "delete_target"),
                self.__getParticleProperty(particle_type, "velocity"),
                self.__getParticleProperty(particle_type, "change_vel"),
                self.__getParticleProperty(particle_type, "circular_spawn"),
                self.__getParticleProperty(particle_type, "random_degree"),
                self.__getParticleProperty(particle_type, "radius"),
                self.__getParticleProperty(particle_type, "circular_speed"),
                self.__getParticleProperty(particle_type, "angle"),
                self.__getParticleProperty(particle_type, "change_angle"),
                self.__getParticleProperty(particle_type, "inc_change_angle"),
                self.__getParticleProperty(particle_type, "alpha"),
                self.__getParticleProperty(particle_type, "change_alpha"),
                self.__getParticleProperty(particle_type, "inc_change_alpha"),
                self.__getParticleProperty(particle_type, "delete_alpha"),
                self.__getParticleProperty(particle_type, "stats")
            )

    def __isParticleSpawner(self, particle_spawner_name):
        if particle_spawner_name in self.__particle_spawners:
            return True
        else:
            printInfo("Error", f"'{particle_spawner_name}' particle spawner doesn't exist")
            return False

    def setParticleSpawnerPos(self, name: str, pos: tuple):
        if self.__isParticleSpawner(name):
            self.__particle_spawners[name].spawner_pos = list(pos)
    
    def setParticleSpawnerTargetPos(self, name: str, pos: tuple):
        if self.__isParticleSpawner(name):
            self.__particle_spawners[name].target_pos = pos

    def setParticleSpawnerSpawn(self, name: str, spawn: bool):
        if self.__isParticleSpawner(name):
            self.__particle_spawners[name].spawn = spawn

    def getParticleSpawnerSpawn(self, name: str) -> bool:
        if self.__isParticleSpawner(name):
            return self.__particle_spawners[name].spawn


    def getParticleSaveData(self) -> dict:

        """Returns a dict of all particle spawners save data

        Returns:
            dict: particle save data
        """

        particle_dict = {}

        for particle_spawner_name in self.__particle_spawners:
            particle_dict[particle_spawner_name] = {
                "pos": self.__particle_spawners[particle_spawner_name].spawner_pos,
                "target_pos": self.__particle_spawners[particle_spawner_name].target_pos,
                "particle_type": self.__particle_spawners[particle_spawner_name].particle_type
            }

        return particle_dict

    def loadParticleSaveData(self, particle_data: dict):

        """Loads all particles from particle save data dict
        """

        for particle_name in particle_data:
            self.addParticleSpawner(
                particle_name, 
                particle_data[particle_name]["pos"],
                particle_data[particle_name]["particle_type"])

            self.__particle_spawners[particle_name].target_pos = particle_data[particle_name]["target_pos"]


    def drawParticles(self, 
            surf: Surface, 
            draw_from_pos: tuple, 
            game_win_width: int, 
            game_win_height: int,
            update: bool = True):

        delete_list = []

        for particle_spawner in self.__particle_spawners:
            self.__particle_spawners[particle_spawner].draw(
                surf, draw_from_pos, game_win_width, game_win_height, update)

            if update and self.__particle_spawners[particle_spawner].delete:
                delete_list.append(particle_spawner)

        for particle_spawner in delete_list:
            del self.__particle_spawners[particle_spawner]
