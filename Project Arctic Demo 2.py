from data.scripts.UI.UI import UI
from data.scripts.game.Game import Game
import data.scripts.globalVar as globalVar
globalVar.init()

## Settting up window
window = UI(
    1270, 
    "Project Arctic Demo 2",
    fullscreen = False,
    show_fps = True, 
    windows_scaling = True, 
    volume = 50,
    visible_cursor = False)

game_obj = Game("player1", (0, 0, 0), (255, 255, 255), False, False, False) # Settings up game

game_obj.newMap("map1", (100, 100), ["black"]) # Creating new map

game_obj.addEntity("player1", "log", (0, 0), "idle") # Creating player entity


## Main Loop
while globalVar.run:

    ## Player Movement
    game_obj.moveEntity()
    if window.isHoldKey("move_up"):
        game_obj.moveEntity(up = True)
    if window.isHoldKey("move_down"):
        game_obj.moveEntity(down = True)
    if window.isHoldKey("move_right"):
        game_obj.moveEntity(right = True)
    if window.isHoldKey("move_left"):
        game_obj.moveEntity(left = True)

    game_obj.setCameraFollowEntitiy() # Move Camera

    ## Drawing & Update
    window.updateDraw()
    game_obj.updateDraw(window)