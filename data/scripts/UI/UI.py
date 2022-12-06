from typing import Sequence
import pygame, time, data.scripts.globalVar as globalVar
from sys import exit as sysExit
from data.scripts.UI.printInfo import printInfo
from data.scripts.UI.saveLoadData import loadData, searchFiles, loadImg, loadImgPath, getFilename
from data.scripts.audio.audio import UIAudio
from data.scripts.UI.UIElements import Button, Menu, UIElement, fpsCounter
from ctypes import windll
globalVar.init()

## UI cass
class UI:

    __KEYBIND_PATH = "data/config/keybinds.json"

    __PYGAME_KEYBOARD_DICT = {
        pygame.K_BACKSPACE:         "backspace",
        pygame.K_TAB:               "tab",
        pygame.K_CLEAR:             "clear",
        pygame.K_RETURN:            "return",
        pygame.K_PAUSE:             "pause",
        pygame.K_ESCAPE:            "escape",
        pygame.K_SPACE:             "space",
        pygame.K_EXCLAIM:           "exclaim",
        pygame.K_QUOTEDBL:          "quotedbl",
        pygame.K_HASH:              "hash",
        pygame.K_DOLLAR:            "dollar",
        pygame.K_AMPERSAND:         "ampersand",
        pygame.K_QUOTE:             "quote",
        pygame.K_LEFTPAREN:         "left_parenthesis",
        pygame.K_RIGHTPAREN:        "right_parenthesis",
        pygame.K_ASTERISK:          "asterisk",
        pygame.K_PLUS:              "plus_sign",
        pygame.K_COMMA:             "comma",
        pygame.K_MINUS:             "minus_sign",
        pygame.K_PERIOD:            "period",
        pygame.K_SLASH:             "forward_slash",
        pygame.K_0:                 "0",
        pygame.K_1:                 "1",
        pygame.K_2:                 "2",
        pygame.K_3:                 "3",
        pygame.K_4:                 "4",
        pygame.K_5:                 "5",
        pygame.K_6:                 "6",
        pygame.K_7:                 "7",
        pygame.K_8:                 "8",
        pygame.K_9:                 "9",
        pygame.K_COLON:             "colon",
        pygame.K_SEMICOLON:         "semicolon",
        pygame.K_LESS:              "less_than_sign",
        pygame.K_EQUALS:            "equals_sign",
        pygame.K_GREATER:           "greater_than_sign",
        pygame.K_QUESTION:          "question_mark",
        pygame.K_AT:                "at",
        pygame.K_LEFTBRACKET:       "left_bracket",
        pygame.K_BACKSLASH:         "backslash",
        pygame.K_RIGHTBRACKET:     "right_bracket",
        pygame.K_CARET:             "caret",
        pygame.K_UNDERSCORE:        "underscore",
        pygame.K_BACKQUOTE:         "grave",
        pygame.K_a:                 "a",
        pygame.K_b:                 "b",
        pygame.K_c:                 "c",
        pygame.K_d:                 "d",
        pygame.K_e:                 "e",
        pygame.K_f:                 "f",
        pygame.K_g:                 "g",
        pygame.K_h:                 "h",
        pygame.K_i:                 "i",
        pygame.K_j:                 "j",
        pygame.K_k:                 "k",
        pygame.K_l:                 "l",
        pygame.K_m:                 "m",
        pygame.K_n:                 "n",
        pygame.K_o:                 "o",
        pygame.K_p:                 "p",
        pygame.K_q:                 "q",
        pygame.K_r:                 "r",
        pygame.K_s:                 "s",
        pygame.K_t:                 "t",
        pygame.K_u:                 "u",
        pygame.K_v:                 "v",
        pygame.K_w:                 "w",
        pygame.K_x:                 "x",
        pygame.K_y:                 "y",
        pygame.K_z:                 "z",
        pygame.K_DELETE:            "delete",
        pygame.K_KP0:               "keypad_0",
        pygame.K_KP1:               "keypad_1",
        pygame.K_KP2:               "keypad_2",
        pygame.K_KP3:               "keypad_3",
        pygame.K_KP4:               "keypad_4",
        pygame.K_KP5:               "keypad_5",
        pygame.K_KP6:               "keypad_6",
        pygame.K_KP7:               "keypad_7",
        pygame.K_KP8:               "keypad_8",
        pygame.K_KP9:               "keypad_9",
        pygame.K_KP_PERIOD:         "keypad_period",
        pygame.K_KP_DIVIDE:         "keypad_divide",
        pygame.K_KP_MULTIPLY:       "keypad_multiply",
        pygame.K_KP_MINUS:          "keypad_minus",
        pygame.K_KP_PLUS:           "keypad_plus",
        pygame.K_KP_ENTER:          "keypad_enter",
        pygame.K_KP_EQUALS:         "keypad_equals",
        pygame.K_UP:                "up_arrow",
        pygame.K_DOWN:              "down_arrow",
        pygame.K_RIGHT:             "right_arrow",
        pygame.K_LEFT:              "left_arrow",
        pygame.K_INSERT:            "insert",
        pygame.K_HOME:              "home",
        pygame.K_END:               "end",
        pygame.K_PAGEUP:            "page_up",
        pygame.K_PAGEDOWN:          "page_down",
        pygame.K_F1:                "F1",
        pygame.K_F2:                "F2",
        pygame.K_F3:                "F3",
        pygame.K_F4:                "F4",
        pygame.K_F5:                "F5",
        pygame.K_F6:                "F6",
        pygame.K_F7:                "F7",
        pygame.K_F8:                "F8",
        pygame.K_F9:                "F9",
        pygame.K_F10:               "F10",
        pygame.K_F11:               "F11",
        pygame.K_F12:               "F12",
        pygame.K_F13:               "F13",
        pygame.K_F14:               "F14",
        pygame.K_F15:               "F15",
        pygame.K_NUMLOCK:           "numlock",
        pygame.K_CAPSLOCK:          "capslock",
        pygame.K_SCROLLOCK:         "scrollock",
        pygame.K_RSHIFT:            "right_shift",
        pygame.K_LSHIFT:            "left_shift",
        pygame.K_RCTRL:             "right_control",
        pygame.K_LCTRL:             "left_control",
        pygame.K_RALT:              "right_alt",
        pygame.K_LALT:              "left_alt",
        pygame.K_RMETA:             "right_meta",
        pygame.K_LMETA:             "left_meta",
        pygame.K_LSUPER:            "left_Windows",
        pygame.K_RSUPER:            "right_Windows",
        pygame.K_MODE:              "mode_shift",
        pygame.K_HELP:              "help",
        pygame.K_PRINT:             "print_screen",
        pygame.K_SYSREQ:            "sysrq",
        pygame.K_BREAK:             "break",
        pygame.K_MENU:              "menu",
        pygame.K_POWER:             "power",
        pygame.K_EURO:              "Euro",
        pygame.K_AC_BACK:           "Android_back_button"
    }

    __PYGAME_KEYBOARD_DICT = {v: k for k, v in __PYGAME_KEYBOARD_DICT.items()}

    def __init__(self, 
            win_width: int = 1280, 
            caption: str = "Caption", 
            icon: str = None, 
            volume: float = 50, 
            background_colour: tuple = None, 
            fullscreen: bool = False, 
            resizable: bool = True, 
            frametime: int = None, 
            visible_cursor: bool = True,
            show_fps: bool = False, 
            windows_scaling: bool = False,
            button_audio_cat: str = "UI"):
        
        pygame.init()

        ## Prevents window from scaling with windows scaling
        if not windows_scaling and not fullscreen:
            windll.user32.SetProcessDPIAware() ## DON'T TURN THIS ON WITH FULLSCREEN

        self.setVisibleMouse(visible_cursor)

        self.fullscreen = fullscreen
        self.resizable = resizable

        globalVar.win_width = None
        self.setWinWidth(win_width)

        self.setWin()

        self.setCaption(caption)

        globalVar.image_dict = {} # Stores all the loaded images for the UI

        self.setIcon(icon)

        ## Clock and framerate
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        globalVar.dt = time.time() - self.last_time
        self.frametime = frametime
        self.framerate = 60 # Framerate for all movements / animations
        self.fps_counter = fpsCounter()
        self.show_fps = show_fps

        ## Display
        self.background_colour = background_colour
        self.menu_dict = {}
        pygame.font.init()

        ## Input's
        self.loadKeybinds()
        self.keybind_inputs = []
        self.last_keyboard_inputs = []
        self.setMousePos()
        self.mouse_press = [0,0,0]  # 0 == No, 1 == Press, 2 == Hold
        self.resized = False


        ## Audio
        globalVar.audio = UIAudio(volume, 32)
        self.setButtonAudioCat(button_audio_cat)

        ## Menu
        self.menu_dict = {}



    ##  ------ Window ------  ##

    ## Sets the window up
    def setWin(self):

        """Set up the window
        """

        if self.fullscreen:
            self.win = pygame.display.set_mode((globalVar.win_width, globalVar.win_height), pygame.FULLSCREEN)
        
        elif self.resizable:
            self.win = pygame.display.set_mode((globalVar.win_width, globalVar.win_height), pygame.RESIZABLE)

        else:
            self.win = pygame.display.set_mode((globalVar.win_width, globalVar.win_height))

    ## Sets fullscreen
    def setFullscreen(self, fullcreen: bool):

        """Sets windows fullscreen
        """

        if type(fullcreen) == bool:
            self.fullscreen == fullcreen
        else:
            printInfo("Error", f"setFullscreen - Value is not a bool [{fullcreen}]")
        
        self.setWin()

    ## Sets resizable
    def setResizeable(self, resizeable: bool):

        """Sets windows resizeable
        """

        if type(resizeable) == bool:
            self.resizable == resizeable
        else:
            printInfo("Error", f"setResizeable - Value is not a bool [{resizeable}]")
        
        self.setWin()

    ## Sets the caption on the window
    def setCaption(self, caption: str):

        """Sets the caption on the window
        """

        pygame.display.set_caption(caption)

    def setVisibleMouse(self, visible: bool):

        """Sets whether the mouse is visible
        """

        pygame.mouse.set_visible(visible)

    def getVisibleMouse(self) -> bool:

        """Returns whether the mouse is visible

        Returns:
            bool: mouse visible
        """

        return pygame.mouse.get_visible()


    ## Sets the height based on the width to keep the winow in a 16:9 ratio
    def setWinHeight(self):

        """Sets the height based on the width (keeps in 16:9 ratio)
        """

        globalVar.win_height = round((globalVar.win_width/16)*9)

    ## Sets the width difference between the window and a length of 1920
    def setWinScale(self):

        """Sets width different between window & 1920px
        """

        globalVar.win_scale = globalVar.win_width / 1920

    ## Sets the window's width
    def setWinWidth(self, width: int):

        """Sets the win width
        """

        if type(width) == int:
            globalVar.win_width = width
            self.setWinScale()
            self.setWinHeight()
            self.setWin()
        else:
            printInfo("Error", f"setWinWidth - width is not an int [{width}]")

    ## Resizes the window and menus
    def resize(self):

        """Resizes the window & menus
        """

        self.setWinWidth(self.win.get_width())
        self.resizeAllMenu()

    ## Draw background colour
    def drawBackground(self):

        """Draw background colour
        """

        if self.background_colour != None:
            self.win.fill(self.background_colour)

    ## Updates the window
    def updateDisplay(self):

        """Updates the window
        """    

        pygame.display.update()

    ## Draws all elements of UI in one neat package 
    def draw(self, update_display: bool = True):

        """Draws all elements & menus in one neat package
        """

        self.drawBackground()
        self.drawAllMenu()
        self.drawFPS()
        if update_display:
            self.updateDisplay()


    def updateDraw(self):

        """Draws and updates the window
        """

        self.updateClock()
        self.setInputs()
        self.checkWindowState()
        self.draw()


    ##  ------ Images ------  ##

    ## Loads image to image Dict, returns whether the image has been added
    def loadImage(self, image_path: str, image_name: str = None) -> str:

        """Loads image to image dict

        Returns:
            str: loaded image 
        """

        return loadImg(image_path, image_name)

    ## Loads all images from a source path
    def loadImagePath(self, path: str) -> list:

        """Loads all images in a directory

        Returns:
            list: list of images loaded
        """

        return loadImgPath(path)

    ## Returns image
    def getImage(self, image_name: str) -> pygame.Surface:

        """Returns an image surface from a name

        Returns:
            Surface: image surface
        """

        return globalVar.getImage(image_name)

    ## Sets Icon image
    def setIcon(self, image_path: str):

        """Sets icon image
        """

        if image_path != None:
            if self.loadImage(image_path, "windowIcon"):
                pygame.display.set_icon(self.getImage("windowIcon"))




    ##  ------ Clock ------  ##

    ## Updates delta time, updating game bassed on time elapsed
    def __setDeltaTime(self):

        """Updates delta time
        """
        
        globalVar.dt = time.time() - self.last_time # Checks how much time passed dt = delta time
        globalVar.dt *= self.framerate # e.g. One second passing == 60 frames
        self.last_time = time.time()

    ## Sets how many frames the game updates per second
    def __setClockTick(self):

        """Sets how many frames the game updates per second
        """

        if self.frametime != None:
            self.clock.tick(self.frametime)

    ## Update time and FPS
    def updateClock(self):

        """Update time & FPS
        """

        self.__setClockTick()

        self.__setDeltaTime()

    def drawFPS(self):

        """Draws FPS counter
        """

        if self.show_fps:
            self.fps_counter.checkFrames()
            self.fps_counter.draw(self.win)


    ##  ------ Inputs ------  ##

    ## Gets the cursor position
    def setMousePos(self):

        """Gets the cursor position
        """

        globalVar.mouse_pos = pygame.mouse.get_pos()

    ## Get the mouse button's inputs
    def getMousePress(self, button_pos: int = 0) -> bool:

        """Returns whether the mouse button has been pressed. (0 = left click,
        1 = middle click, 2 = right click )

        Returns:
            bool: button press
        """

        if button_pos >= 0 and button_pos <= 2:
            return pygame.mouse.get_pressed()[button_pos]
            
        else:
            printInfo("Error", f"getMousePress - Position should be an int from 0-2")
            return False

    ## Sets the mouse_press values
    def setMousePress(self):

        """Sets the mouse press
        """

        for pos in range(3):
            if self.getMousePress(pos):
                if self.mouse_press[pos] == 0:
                    self.mouse_press[pos] = 1
                elif self.mouse_press[pos] == 1:
                    self.mouse_press[pos] = 2
            else:
                self.mouse_press[pos] = 0

    ## Returns whether the button is being pressed
    def isPressMouse(self, button_pos: int) -> bool:

        """Returns whether a mouse button has been pressed

        Returns:
            bool: mouse button pressed
        """

        return self.mouse_press[button_pos] == 1
    
    ## Return whether the button is being held
    def isHoldMouse(self, button_pos: int):

        """Returns whether a mouse button is being held

        Returns:
            bool: mouse button held
        """

        return self.mouse_press[button_pos] == 1 or self.mouse_press[button_pos] == 2
                

    ## Loads keybinds
    def loadKeybinds(self):

        """Loads keybinds
        """

        self.keybinds = loadData(self.__KEYBIND_PATH)

    def __isKeyPress(self, keyboard_event: Sequence[bool], key: str) -> bool:
        
        """Returns whether key has been pressed

        Returns:
            bool: pressed
        """        

        if key in self.__PYGAME_KEYBOARD_DICT:
            return keyboard_event[self.__PYGAME_KEYBOARD_DICT[key]]
        else:
            printInfo("Error", f"{key} isn't a valid keyboard input")


    ## Recives keyboard Input
    def setKeyboardInputs(self):

        """Recives keyboard inputs
        """

        self.last_keyboard_inputs = self.keybind_inputs
        self.keybind_inputs = []
        
        # keyboard_event = keyboard.get_hotkey_name()
        keyboard_event = pygame.key.get_pressed()

        for keybind_name in self.keybinds:
            if self.__isKeyPress(keyboard_event, self.keybinds[keybind_name]):
                self.keybind_inputs.append(keybind_name)

        # print(self.keybind_inputs)        

    def setInputs(self):

        """Sets inputs
        """

        self.setMousePress()
        self.setMousePos()
        self.setKeyboardInputs()

    def __isKeybind(self, keybind_name) -> bool:

        """Returns whether a keybind is in keybinds dict

        Returns:
            bool: keybind in keybinds dict
        """

        if keybind_name in self.keybinds:
            return True
        
        else:
            printInfo("Info", f"isHold - Keybind doesn't exist [{keybind_name}]")
            return False

    ## Check if a key has been pressed
    def isPressKey(self, keybind_name: str) -> bool:

        """Checks if a key has been pressed (str / list)

        Returns:
            bool: key pressed
        """

        if type(keybind_name) == list:
            press = True
            
            for keybind in keybind_name:
                if self.__isKeybind(keybind):
                    if not keybind in self.keybind_inputs and keybind not in self.last_keyboard_inputs:
                        press = False
                        break
                else:
                    return False
            
            return press

        else:
            if self.__isKeybind(keybind_name):
                return keybind_name in self.keybind_inputs and keybind_name not in self.last_keyboard_inputs

        return False


    ## Check if key is being held
    def isHoldKey(self, keybind_name: str) -> bool:

        """Checks if a key is being held (str / list)

        Returns:
            bool: key held
        """

        if type(keybind_name) == list:
            press = True
            
            for keybind in keybind_name:
                if self.__isKeybind(keybind):
                    if not keybind in self.keybind_inputs:
                        press = False
                        break
                else:
                    return False
            
            return press

        else:
            if self.__isKeybind(keybind_name):
                return keybind_name in self.keybind_inputs

        return False
            

    ## Check Window state deals with resizing and 
    ## exit window button
    def checkWindowState(self):

        """Checks window state, deal with resizing & exit window button
        """

        self.resized = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globalVar.run = False

            elif event.type == pygame.VIDEORESIZE:
                self.resize()
                self.resized = True
    



    ##  ------ Menus ------  ##

    ## Adds menu to menu dict
    def addMenu(self, 
            menu_name: str, 
            pos: tuple, 
            dimensions: tuple,
            colour: tuple = (0,0,0), 
            alpha: int = 255,
            centered: bool = True, 
            display: bool = True):

        """Adds menu element to UI
        """    
        
        self.menu_dict[menu_name] = Menu(pos, dimensions, 
                                    colour, alpha,
                                    centered, display)
        
        printInfo("INFO", f"New menu added [{menu_name}]")

    ## Returns menu from menu dict according to its indexed name
    def getMenu(self, menu_name: str) -> Menu:

        """Returns menu from UI

        Returns:
            Menu: menu
        """

        return self.menu_dict[menu_name]

    ## Returns element of a menu
    def getMenuElement(self, menu_name: str, element_name: str) -> UIElement:

        """Returns UI element from a menu

        Returns:
            UIElement: menu UI element
        """

        return self.getMenu(menu_name).getMenuElement(element_name)

    ## Sets menu's display value
    def setDisplayMenu(self, menu_name: str, display: bool):

        """Sets menu's display value (whether it is visible)
        """

        self.getMenu(menu_name).display = display
    
    def getDisplayMenu(self, menu_name: str) -> bool:
        
        """Returns whether the menu is being displayed

        Returns:
            bool: menu displayed
        """
        
        return self.getMenu(menu_name).display

    ## Sets element in menu's display value
    def setDisplayElement(self, menu_name: str, element_name: str, display: bool):

        """Sets UI elements display value (whether it is visible)
        """
        
        self.getMenuElement(menu_name, element_name).display = display

        self.drawMenu(menu_name)

    
    def getDisplayElement(self, menu_name: str, element_name: str) -> bool:
        
        """Returns whether the element is being displayed

        Returns:
            bool: element displayed
        """
        
        return self.getMenuElement(menu_name, element_name).display


    ## Makes menu redraw all their elements
    def drawMenuElements(self, menu_name: str):

        """Making menu redraw all their elements
        """

        self.getMenu(menu_name).drawElements()

    ## Draws a menu on window surface
    def drawMenu(self, menu_name: str):

        """Draws menu on window surface
        """

        self.getMenu(menu_name).draw(self.win)

    ## Draws all menus on window surface
    def drawAllMenu(self):

        """Draws all menu's on window surface
        """

        for menu_name in self.menu_dict:
            self.drawMenu(menu_name)

    def resizeMenu(self, menu_name: str):

        """Resizes menu
        """

        self.getMenu(menu_name).resize()

    ## Resizes all menus on window surface
    def resizeAllMenu(self):

        """Resizes all menus
        """

        for menu_name in self.menu_dict:
            self.resizeMenu(menu_name)

    ## Updates text for a menu text element
    def updateText(self, menu_name: str, element_name: str, text: str):

        """Updates text for a menu text element 
        """

        self.getMenu(menu_name).updateText(element_name, text)

    ## Adds new font
    def addFont(self, font_path: str, font_name: str = None):

        """Adds a new font
        """
        
        globalVar.font_dict[font_name] = font_path

        printInfo("Info", f"Added new font '{font_name}'")

    def addFontDir(self, path):
        for font_path in searchFiles(path, "ttf"):
            
            self.addFont(font_path, getFilename(font_path))

    ## Returns font path from fonts name
    def getFont(self, font_name: str):

        """Returns font

        Returns:
            font: font
        """

        return globalVar.getFont(font_name)






    ##  ------ Buttons ------  ##

    ## Sets the audio cat for buttons to use &
    ## creates one if there isn't one
    def setButtonAudioCat(self, cat_name: str):

        """Sets audio category for UI elements
        """

        self.button_audio_cat = cat_name
        self.addCat(self.button_audio_cat)

    ## Returns the name of the button audio cat
    def getButtonAudioCat(self) -> str:

        """Returns name of UI element audio's category

        Returns:
            str: audio category
        """

        return self.button_audio_cat

    def getButton(self, menu_name: str, button_name: str) -> Button:

        """Returns button from a menu

        Returns:
            Button: button
        """

        return self.getMenu(menu_name).getMenuElement(button_name)

    ## Plays the buttons audio
    def playButtonAudio(self, menu_name: str, button_name: str):

        """Plays button audio
        """

        button = self.getButton(menu_name, button_name)
        
        if button.pressAudio != None:
            if button.pressAudioPlay:
                self.play(self.button_audio_cat, button.pressAudio)
        
        if button.hoverAudio != None:
            if button.hoverAudioPlay:
                self.play(self.button_audio_cat, button.hoverAudio)
        

    ## Updates a button being pressed
    def isPressButton(self, menu_name: str, button_name: str, mouse_button: int) -> bool:

        """Returns whether the button has been pressed

        Returns:
            bool: button pressed
        """

        press = self.getMenu(menu_name).isPress(button_name, globalVar.mouse_pos, self.isPressMouse(mouse_button))
        self.playButtonAudio(menu_name, button_name)
        return press
    
    ## Updates a button being held
    def isHoldButton(self, menu_name: str, button_name: str, mouse_button: int) -> bool:

        """Returns whether the button is being held

        Returns:
            bool: button held
        """

        press = self.getMenu(menu_name).isPress(button_name, globalVar.mouse_pos, self.isHoldMouse(mouse_button))
        self.playButtonAudio(menu_name, button_name)
        return press

    ## Adds a box to element dict
    def addBox(self, 
            menu_name: str, 
            element_name: str, 
            pos: tuple, 
            dimension: tuple, 
            colour: tuple = (0,0,0), 
            alpha: int = 255, 
            rounded_corners: float = 0, 
            centered: bool = True, 
            display: bool = True):

        """Adds a box element to the UI
        """

        self.getMenu(menu_name).addBox(element_name, 
                                        pos, dimension, 
                                        colour, alpha, 
                                        rounded_corners, centered, 
                                        display)

        self.drawMenuElements(menu_name)

        printInfo("INFO", f"New box element added [{menu_name}] [{element_name}]")

    ## Adds a image to element dict
    def addImage(self, 
            menu_name: str, 
            element_name: str, 
            pos: tuple, 
            image: str, 
            scale: float, 
            alpha: int = 255, 
            centered: bool = True, 
            display: bool = True):

        """Adds an image element to the UI
        """
        
        self.getMenu(menu_name).addImage(element_name, 
                                        pos, 
                                        image, scale, 
                                        alpha, 
                                        centered, 
                                        display)
        
        self.drawMenuElements(menu_name)

        printInfo("INFO", f"New image element added [{menu_name}] [{element_name}]")

    ## Adds a text to element dict
    def addText(self, 
            menu_name: str, 
            element_name: str, 
            pos: tuple, 
            text: str, 
            size: int,
            font: str = "verdana", 
            colour: tuple = (0,0,0), 
            alpha: int = 255, 
            centered: bool = True, 
            display: bool = True):

        """Adds an text element to the UI
        """
        
        self.getMenu(menu_name).addText(element_name,
                                        pos, 
                                        text, size, self.getFont(font), 
                                        colour, alpha, 
                                        centered, display)
        
        self.drawMenuElements(menu_name)

        printInfo("INFO", f"New text element added [{menu_name}] [{element_name}]")

    ## Adds Button Image to element dict
    def addButtonImage(self, 
            menu_name: str, 
            element_name: str, 
            pos: tuple, 
            press_image: str, 
            unpess_image: str, 
            hover_image: str = None, 
            press_scale: float = 1,
            unpress_scale: float = 1, 
            hover_scale: float = 1,
            alpha: int = 255, 
            press: bool = False, 
            press_audio: str = None, 
            hover_audio: str = None, 
            centered: bool = True, 
            display: bool = True):

        """Adds an image button element to the UI
        """
        
        self.getMenu(menu_name).addButtonImage(element_name,
                                        pos, 
                                        press_image, unpess_image, 
                                        hover_image, press_scale,
                                        unpress_scale, hover_scale,
                                        alpha,
                                        press, press_audio, 
                                        hover_audio, centered, 
                                        display)

        self.drawMenuElements(menu_name)

        printInfo("INFO", f"New button element added [{menu_name}] [{element_name}]")


    ## Adds Button Text to element dict
    def addButtonText(self, 
            menu_name: str, 
            element_name: str, 
            pos: tuple, 
            press_text: str, 
            unpress_text: str, 
            hover_text: str = None, 
            press_size: int = 1,
            unpress_size: int = 1, 
            hover_size: int = 1, 
            press_colour: tuple = (0, 0, 0), 
            unpress_colour: tuple = (0, 0, 0), 
            hover_colour: tuple = (0, 0, 0),
            font: str = "verdana",
            alpha: int = 255, 
            press: bool = False, 
            press_audio: str = None, 
            hover_audio: str = None, 
            centered: bool = True, 
            display: bool = True):

        """Adds an text button element to the UI
        """
        
        self.getMenu(menu_name).addButtonText(element_name, pos, 
                    press_text, unpress_text, 
                    hover_text, press_size,
                    unpress_size, hover_size, 
                    press_colour, 
                    unpress_colour, 
                    hover_colour, self.getFont(font), 
                    alpha,
                    press, press_audio, 
                    hover_audio, centered, 
                    display)

        self.drawMenuElements(menu_name)

        printInfo("INFO", f"New button element added [{menu_name}] [{element_name}]")




    ##  ------ Audio ------  ##

    ## Adds new audio category
    def addCat(self, cat_name: str, volume: float = 50):

        """Adds a new audio category
        """

        globalVar.audio.addCat(cat_name, volume)

    ## Adds a new audio to a category
    def addAudio(self, cat_name: str, path: str, audio_name: str = None, volume: float = 50):

        """Adds new audio to a category
        """

        globalVar.audio.addAudio(cat_name, path, audio_name, volume)

    ## Adds all audio from a source path
    def addAudioPath(self, cat_name: str, path, volume: float = 50):

        """Adds all audio from a directory
        """

        for audio_name in searchFiles(path, "wav"):
            self.addAudio(cat_name, audio_name, volume = volume)

    ## Sets volume of an audio category
    def setCatVolume(self, cat_name: str, volume: float):

        """Sets volume of an audiop category
        """

        globalVar.audio.setCatVolume(cat_name, volume)
    
    ## Sets volume of an audio
    def setAudioVolume(self, cat_name: str, audio_name: str, volume: float):

        """Sets volume of an audio
        """

        globalVar.audio.setAudioVolume(cat_name, audio_name, volume)
    
    ## Plays an audio
    def play(self, cat_name: str, audio_name: str, loops: int = 0):

        """Plays an audio
        """

        globalVar.audio.play(cat_name, audio_name, loops)

    ## Pauses an Audio
    def pause(self, cat_name: str, audio_name: str):

        """Pauses an audio
        """

        globalVar.audio.pause(cat_name, audio_name)
    
    ## Unpauses an audio
    def unpause(self, cat_name: str, audio_name: str):

        """Unpauses an audio
        """

        globalVar.audio.unpause(cat_name, audio_name)

    ## Queues an audio after another audio
    def queue(self, cat_name: str, audio_name: str, audioQueue: str):

        """Queues an audio after another audio
        """

        globalVar.audio.queue(cat_name, audio_name, audioQueue)