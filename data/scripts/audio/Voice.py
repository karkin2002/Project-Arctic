from data.scripts.UI.saveLoadData import loadData, makeDir
from data.scripts.UI.printInfo import printInfo
import data.scripts.globalVar as globalVar
globalVar.init()

class Voice:

    """Plays each letter for each letter in a sentence
    """


    __VOICE_SOUNDS = [
        'a', 'b', 'c', 'd', 'e', 'f', 
        'g', 'h', 'i', 'j', 'k', 'l', 
        'm', 'n', 'o', 'p', 'q', 'r', 
        's', 't', 'u', 'v', 'w', 'x', 
        'y', 'z']
    
    __PAUSE_SOUNDS = [
        '.', '!', '?'
    ]

    __VOICE_TITLES_PATH = "data/config/voice_titles.json"

    __VOICE_TITLES = loadData(__VOICE_TITLES_PATH)

    __VOICE_FOLDER_PATH = "data/audio/voice/"
    __VOICE_TITLE_FOLDER_PATH = __VOICE_FOLDER_PATH + "{title}/"
    __VOICE_SOUND_NAME = "{title}_{sound}"

    makeDir(__VOICE_FOLDER_PATH)

    for title in __VOICE_TITLES:
        makeDir(__VOICE_TITLE_FOLDER_PATH.format(title = title))

    __voices_loaded = []
    
    def __init__(self, 
            cat_name: str, 
            voice_title: str, 
            letter_speed: int = 0.08,
            pause_speed: int = 1,
            break_speed: int = 2):


        self.__voice_title = voice_title

        self.__cat_name = cat_name

        self.__loadVoice()

        self.__sentence = []
        self.played_sentence = ""

        self.__letter_speed = letter_speed * 60
        self.__pause_speed = pause_speed * 60
        self.__break_speed = break_speed * 60
        self.__timer_end = self.__letter_speed
        self.__letter_timer = 0


    def setLetterSpeed(self, letter_speed: float):

        """Sets letter speed
        """

        self.__letter_speed = letter_speed * 60


    def setPauseSpeed(self, pause_speed: float):

        """Sets letter speed
        """

        self.__pause_speed = pause_speed * 60


    def setBreakSpeed(self, break_speed: float):

        """Sets letter speed
        """

        self.__break_speed = break_speed * 60


    def __isVoice(self) -> bool:

        """Returns whether voice name is in voice titles json file

        Returns:
            bool: voice exists
        """

        if self.__voice_title in self.__VOICE_TITLES:
            return True
        else:
            printInfo(
                "Error", 
                f"'{self.__voice_title}' voice doesn't exist in '{self.__VOICE_TITLES_PATH}'")

    def setVoiceTitle(self, voice_title: str):

        """Sets the voice title
        """

        if self.__isVoice():
            self.__voice_title = voice_title


    def __isVoiceLoaded(self) -> bool:

        """Returns whether a voice's audio has been loaded

        Returns:
            bool: loaded
        """

        return self.__voice_title in self.__voices_loaded


    def __loadVoice(self):

        """If the audio for the letters aren't loaded, they will be loaded
        """

        if not self.__isVoiceLoaded():
            if self.__isVoice():
                
                for sound in self.__VOICE_SOUNDS:

                    globalVar.audio.addAudio(
                        self.__cat_name, 
                        self.__VOICE_TITLE_FOLDER_PATH.format(
                            title = self.__voice_title) + sound + ".wav", 
                        self.__VOICE_SOUND_NAME.format(
                            title = self.__voice_title,
                            sound = sound),
                        self.__VOICE_TITLES[self.__voice_title])
                
                self.__voices_loaded.append(self.__voice_title)

    def __playLetter(self, letter: str):

        """plays letter
        """
        letter = letter.lower()
        
        if letter in self.__VOICE_SOUNDS:
            globalVar.audio.play(
                self.__cat_name, 
                self.__VOICE_SOUND_NAME.format(
                    title = self.__voice_title,
                    sound = letter))


    def addSentence(self, sentence: str):

        """Sets the sentence
        """

        if not self.__isSentence():
            self.played_sentence = ""

        self.__sentence.append(sentence)


    def __isSentence(self):

        """Returns whether there are any sentences

        Returns:
            bool: not empty
        """
        
        return len(self.__sentence) > 0

    def isEmpty(self):

        """Returns whether there are no sentences left

        Returns:
            bool: empty
        """

        return len(self.__sentence) == 0

    def isPlayed(self) -> bool:

        """Returns whether the sentence has been played

        Returns:
            bool: played
        """

        return self.__isSentence() and self.__sentence[0] == "" and len(self.played_sentence) > 0


    def skip(self, all: bool = False):

        if all:
            self.__sentence = []
        else:
            self.__sentence.pop(0)
        
        self.played_sentence = ""



    def playSentence(self):

        """Plays the sentence
        """
        
        if not self.isPlayed():
            if self.__isSentence():
                if self.__letter_timer >= self.__timer_end:
                    
                    self.__playLetter(self.__sentence[0][0])

                    self.played_sentence += self.__sentence[0][0]
                    
                    if len(self.__sentence[0]) > 1:

                        if self.__sentence[0][0] in self.__PAUSE_SOUNDS:
                            self.__timer_end = self.__pause_speed
                        else:
                            self.__timer_end = self.__letter_speed

                        self.__sentence[0] = self.__sentence[0][1:]
                    
                    else:
                        self.__sentence[0] = ""
                        self.__timer_end = self.__break_speed
                    
                    self.__letter_timer = 0
                
                else:
                    self.__letter_timer += 1 * globalVar.dt

        else:

            if self.__letter_timer >= self.__timer_end:
                self.__sentence.pop(0)

                self.__timer_end = self.__letter_speed

                if self.__isSentence():
                    self.played_sentence = ""
            
            else:
                self.__letter_timer += 1 * globalVar.dt
