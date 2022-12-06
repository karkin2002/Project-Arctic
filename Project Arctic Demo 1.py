from data.scripts.UI.UI import UI
from data.scripts.game.Game import Game
import data.scripts.globalVar as globalVar
from data.scripts.basic import setTimer, isTimer
from random import randint
globalVar.init()

def movePlayer():
    """Movement of player
    """    
    game_obj.moveEntity()
    if window.isHoldKey("move_up"):
        game_obj.moveEntity(up = True) # If name is None it auto sets to the players entity
    if window.isHoldKey("move_down"):
        game_obj.moveEntity(down = True)
    if window.isHoldKey("move_left"):
        game_obj.moveEntity(left = True)
    if window.isHoldKey("move_right"):
        game_obj.moveEntity(right = True)


def updateCamera():
    """Updates the camera's position and zoom
    """    
    game_obj.setCameraFollowEntitiy()
    if window.isHoldKey("zoom_in"):
        if game_obj.getCamera().getOriginalScale() < 5:
            game_obj.zoom(0.01)
    if window.isHoldKey("zoom_out"):
        if game_obj.getCamera().getOriginalScale() > 3:
            game_obj.zoom(-0.01)

def setupTileMenu():
    """ Creates the menu's, button's and text UI
    """  
    window.addMenu("admin_menu", (1470, 540), (800, 980), (255, 255, 199), alpha = 255, centered = True, display=False)
    window.addText("admin_menu", "admin_menu_title", (400, 80), "Build Menu", 70, font = "example_font", colour =  (255, 135, 61))

    window.addButtonText(
        "admin_menu", 
        "tile_button", 
        (400, 400), 
        "Tiles", 
        "Tiles", 
        "Tiles", 
        65, 60 , 68, 
        (20, 20, 20),
        (20, 20, 20),
        (50, 50, 50),
        font = "example_font",
        press_audio="bwap",
        hover_audio="do")

    window.addButtonText(
        "admin_menu", 
        "entity_button",
        (400, 550), 
        "Entities", 
        "Entities", 
        "Entities", 
        65, 60 , 68, 
        (20, 20, 20),
        (20, 20, 20),
        (50, 50, 50),
        font = "example_font",
        press_audio="bwap",
        hover_audio="do")

    window.addButtonText(
        "admin_menu", 
        "decal_button", 
        (400, 700), 
        "Decals", 
        "Decals", 
        "Decals", 
        65, 60 , 68, 
        (20, 20, 20),
        (20, 20, 20),
        (50, 50, 50),
        font = "example_font",
        press_audio="bwap",
        hover_audio="do")

    window.addMenu("tile_menu", (1470, 540), (800, 980), (255, 255, 199), alpha = 255, centered = True, display=False)
    window.addText("tile_menu", "tile_menu_title", (400, 80), "Build Menu", 70, font = "example_font", colour =  (255, 135, 61))

    window.addMenu("entity_menu", (1470, 540), (800, 980), (255, 255, 199), alpha = 255, centered = True, display=False)
    window.addText("entity_menu", "entity_menu_title", (400, 80), "Entity Menu", 70, font = "example_font", colour =  (255, 135, 61))

    start_pos = (115, 200)
    start_pos_temp = list(start_pos)
    for tile_name in game_obj.tiles:
        window.addButtonImage(
            "tile_menu", 
            f"{tile_name}_button", 
            start_pos_temp, 
            tile_name, 
            tile_name, 
            tile_name, 
            3.5, 
            4, 
            4.5, 
            press_audio="bwap",
            hover_audio="do")
        start_pos_temp[0] += 80
        
        if start_pos_temp[0] > 750:
            start_pos_temp[1] += 80
            start_pos_temp[0] = start_pos[0]

    start_pos_temp = list(start_pos)
    for entity_name in game_obj.entity_animation_properties:
        window.addButtonImage(
            "entity_menu", 
            f"{entity_name}_button", 
            start_pos_temp, 
            entity_name, 
            entity_name, 
            entity_name, 
            3.5, 
            4, 
            4.5, 
            press_audio="bwap",
            hover_audio="do")
        start_pos_temp[0] += 80
        
        if start_pos_temp[0] > 750:
            start_pos_temp[1] += 80
            start_pos_temp[0] = start_pos[0]


def moveNPC(npcTimer, pickup, mouse_dif):
    """ Handels NPC movement
    """  
    
    if isTimer(npcTimer):
        game_obj.setEntityPath((randint(0, 20), randint(0, 20)), "npc1")
        npcTimer = setTimer(randint(2, 6))

    if window.isHoldMouse(0):
        mouse_pos = game_obj.getMapMousePos()
        if game_obj.isEntityCollidepoint(mouse_pos, "npc1") or pickup:

            entity_pos = game_obj.getEntity("npc1").getMapPos()
            
            if pickup == False:
                mouse_dif = (mouse_pos[0] - entity_pos[0], mouse_pos[1] -  entity_pos[1])

                game_obj.setFloatingTextDisplay("Scream", True) 
                pickup = True
            
            game_obj.setAnimation("down", "npc1")
            game_obj.setFloatingTextPos("Scream", (entity_pos[0], entity_pos[1] - 30))
            game_obj.getEntity("npc1").setMapPos((mouse_pos[0] - mouse_dif[0], mouse_pos[1] - mouse_dif[1]))
    
    else:
        game_obj.setFloatingTextDisplay("Scream", False)
        game_obj.setAnimation("idle", "npc1")
        pickup = False

    return npcTimer, pickup, mouse_dif

def menuInput(open_menu, item_selected, tool, entity_num):
    """ Handels menu inputs
    """  
    if not window.getDisplayMenu("tile_menu"):
        if window.isHoldMouse(0):
            if tool == "build":
                game_obj.placeTile(item_selected)

        if window.isPressMouse(0):
            if tool == "decal":
                game_obj.drawDecal("test_decal_1", game_obj.getMapMousePos())
                entity_num += 1

            if tool == "entity":
                game_obj.addEntity(f"new_entity{entity_num}", item_selected, game_obj.getMapMousePos(), "idle")
                entity_num += 1


    if window.isPressKey("open_menu"):
        window.setDisplayMenu(open_menu, not window.getDisplayMenu(open_menu))
        window.play("UI", "wha")

    if window.getDisplayMenu("admin_menu"):
        if window.isPressButton("admin_menu", "tile_button", 0):
            open_menu = "tile_menu"
            window.setDisplayMenu("admin_menu", False)
            window.setDisplayMenu("tile_menu", True)
        
        elif window.isPressButton("admin_menu", "entity_button", 0):
            open_menu = "entity_menu"
            window.setDisplayMenu("admin_menu", False)
            window.setDisplayMenu("entity_menu", True)
        
        elif window.isPressButton("admin_menu", "decal_button", 0):
            tool = "decal"
        
        elif window.isPressKey("esc"):
            window.setDisplayMenu("admin_menu", False)
        

    elif window.getDisplayMenu("tile_menu"):
        if window.isPressKey("esc"):
            open_menu = "admin_menu"
            window.setDisplayMenu("tile_menu", False)
            window.setDisplayMenu("admin_menu", True)

        for tile_name in game_obj.tiles:
            if window.isPressButton("tile_menu", f"{tile_name}_button", 0):
                tool = "build"
                item_selected = tile_name


    elif window.getDisplayMenu("entity_menu"):
        if window.isPressKey("esc"):
            open_menu = "admin_menu"
            window.setDisplayMenu("entity_menu", False)
            window.setDisplayMenu("admin_menu", True)
        
        for entity_name in game_obj.entity_animation_properties:
            if window.isPressButton("entity_menu", f"{entity_name}_button", 0):
                tool = "entity"
                item_selected = entity_name

    return open_menu, item_selected, tool, entity_num

def particleTriggers():
    """ Handels particle triggers & particles
    """  

    if game_obj.map_name == "map1":
        game_obj.isTrigger("door1", "player1")
        
        if game_obj.isTrigger("particle_trigger1", "player1"):
            game_obj.setParticleSpawnerSpawn("particle_1", True)
            game_obj.setParticleSpawnerPos("particle_1", game_obj.getEntity().getMapPos())
        else:
            game_obj.setParticleSpawnerSpawn("particle_1", False)
        
        
        if game_obj.isTrigger("particle_trigger2", "player1"):
            game_obj.setParticleSpawnerSpawn("particle_2", True)
            game_obj.setParticleSpawnerPos("particle_2", game_obj.getEntity().getMapPos())
            game_obj.setParticleSpawnerTargetPos("particle_2", game_obj.getEntity().getMapPos())
        else:
            game_obj.setParticleSpawnerSpawn("particle_2", False)


        if game_obj.isTrigger("particle_trigger3", "player1"):
            game_obj.setParticleSpawnerSpawn("particle_3_1", True)
            game_obj.setParticleSpawnerSpawn("particle_3_2", True)
            game_obj.setParticleSpawnerPos("particle_3_1", game_obj.getEntity().getMapPos())
            game_obj.setParticleSpawnerPos("particle_3_2", game_obj.getEntity().getMapPos())
            window.unpause("env", "rain")
            window.unpause("env", "thunder")
        else:
            game_obj.setParticleSpawnerSpawn("particle_3_1", False)
            game_obj.setParticleSpawnerSpawn("particle_3_2", False)
            window.pause("env", "rain")
            window.pause("env", "thunder")

        
        if game_obj.isTrigger("particle_trigger4", "player1"):
            game_obj.setParticleSpawnerSpawn("particle_4", True)
            game_obj.setParticleSpawnerPos("particle_4", game_obj.getEntity().getMapPos())
        else:
            game_obj.setParticleSpawnerSpawn("particle_4", False)

    else:
        game_obj.voices.play()
        game_obj.setFloatingTextText("Player Health", game_obj.voices.getVoice("narrator").played_sentence)

        if game_obj.isTrigger("door2", "player1"):
            player_health = game_obj.getEntity().getStat("health")
            game_obj.setFloatingTextText("Player Health", f"Health: {player_health}")




def checkHealthPickups():
    """ Handels picking up hearts
    """  

    player_pos = game_obj.getEntity().getMapPos()
    game_obj.setFloatingTextPos("Player Health", (player_pos[0], player_pos[1] - 30))

    if game_obj.getEntity().getItemAmount("heart") > 0:
        game_obj.getEntity().setStat("health", game_obj.getEntity().getStat("health") + (10 * game_obj.getEntity().getItemAmount("heart")))
        game_obj.getEntity().removeItem("heart", game_obj.getEntity().getItemAmount("heart"))
        player_health = game_obj.getEntity().getStat("health")
        game_obj.setFloatingTextText("Player Health", f"Health: {player_health}")





## Creating UI
window = UI(
    1270, 
    "Project Arctic Demo 1",
    fullscreen = False,
    show_fps = True, 
    windows_scaling = True, 
    volume = 50,
    visible_cursor = True,
    icon = "data/images/icon.png")

window.addFontDir("data/images/UI/fonts/") ## Loading fonts

window.addAudioPath("UI", "data/audio/UI/", 20) ## Loading UI audio
window.addCat("env") ## Creating new audio category
window.addAudioPath("env", "data/audio/background/") ## Loading environemtal audio

## Starting environmental audio
window.play("env", "rain", 99)
window.play("env", "thunder", 99)
window.pause("env", "rain")
window.pause("env", "thunder")

## Setting up a game object
game_obj = Game("player1", (0, 0, 0), None, True, False, False)


## Creating new maps if files aren't already there
game_obj.newMap("map1", (20, 20), ["black"])
game_obj.newMap("map2", (200, 200), ["grass1", "grass2", "grass3", "grass4"])
game_obj.setMapName("map1") # Setting the current map


## Creating player, NPC & item entities
game_obj.addEntity(
    "player1", 
    "player", (
    game_obj.getMap().map_width_px /2, game_obj.getMap().map_height_px /2), 
    "idle")
game_obj.addEntity("npc1", "log", (50, 50), "idle")
for i in range(5):
    game_obj.addEntity(f"coin{i}", "coin", (232, 88 + (i * 16)), "idle")
for i in range(5):
    game_obj.addEntity(f"heart{i}", "heart", (300, 88 + (i * 16)), "idle")

game_obj.setZoom(3) # Settings the camera's zoom
game_obj.setCameraPos(game_obj.getEntity().getMapPos()) ## Settings camera's starting position

npcTimer = setTimer(5) # Setting timer used for NPC movement




## Creating triggers and particles
game_obj.addTrigger("particle_trigger1", (16, 256), (48, 48), None)
game_obj.addParticleSpawner("particle_1", (0, 0), "circle3")
game_obj.addTrigger("particle_trigger2", (96, 256), (48, 48), None)
game_obj.addParticleSpawner("particle_2", (0, 0), "circle")
game_obj.addTrigger("particle_trigger3", (176, 256), (48, 48), None)
game_obj.addParticleSpawner("particle_3_1", (0, 0), "rain")
game_obj.addParticleSpawner("particle_3_2", (0, 0), "rain_hit")
game_obj.addTrigger("particle_trigger4", (256, 256), (48, 48), None)
game_obj.addParticleSpawner("particle_4", (0, 0), "smoke")
map_2_center = (game_obj.getMap("map2").map_width_px / 2, game_obj.getMap("map2").map_height_px / 2)
game_obj.getMap("map2").placeTile("object", "door", (map_2_center[0], map_2_center[1] + 16))
game_obj.addTrigger("door1", (16, 176), (16, 16), (map_2_center[0], map_2_center[1]), "map2")
game_obj.addTrigger("door2", (map_2_center[0], map_2_center[1] + 16), (16, 16), (game_obj.getMap("map1").map_width_px / 2, game_obj.getMap("map1").map_height_px / 2), "map1", map_name="map2")

## Creating floating text
game_obj.addFloatingText("Level Text", "Demo Map 1", (160, -40), "example_font", (255, 255, 255), 30)
game_obj.addFloatingText("Player Health", "Health: 100", (0, 0), "example_font", (255, 255, 255), 6)
game_obj.addFloatingText("Scream", "Ahhh!", (0, 0), "example_font", (200, 100, 100), 10, False)

## Settings up narrator
game_obj.addVoice("narrator", "male1")
game_obj.voices.getVoice("narrator").addSentence("   ")
game_obj.voices.getVoice("narrator").addSentence("Hello World.")
game_obj.voices.getVoice("narrator").addSentence("Where am I?")
game_obj.voices.getVoice("narrator").addSentence("This place looks endless")
game_obj.voices.getVoice("narrator").addSentence("maybe I should go back.")
game_obj.voices.getVoice("narrator").addSentence(" ")

setupTileMenu()

pickup = False
mouse_dif = (0, 0)
item_selected = None
tool = None
open_menu = "admin_menu"
entity_num = 0

## Main Loop
while globalVar.run:

    movePlayer()
    updateCamera()
    open_menu, item_selected, tool, entity_num = menuInput(open_menu, item_selected, tool, entity_num)
    npcTimer, pickup, mouse_dif = moveNPC(npcTimer, pickup, mouse_dif)
    particleTriggers()
    checkHealthPickups()

    ## Drawing & Update
    window.updateDraw()
    game_obj.updateDraw(window)
