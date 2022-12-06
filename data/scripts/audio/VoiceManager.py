
from data.scripts.audio.Voice import Voice
from data.scripts.UI.printInfo import printInfo

class VoiceManager:

    def __init__(self):
        self.__voices = {}

    def addVoice(self, 
            cat_name: str, 
            voice_name: str, 
            voice_title: str,
            letter_speed: float = 0.08,
            pause_speed: int = 1,
            break_speed: int = 2):

        """Adds voice
        """
        
        self.__voices[voice_name] = Voice(
            cat_name, 
            voice_title, 
            letter_speed,
            pause_speed,
            break_speed)

    def isVoice(self, voice_name: str) -> bool:

        """Returns whether the voice exists

        Returns:
            bool: voice exists
        """

        if voice_name in self.__voices:
            return True
        
        else:
            printInfo("Error", f"'{voice_name}' Voice doesn't exist")
            return False

    def getVoice(self, voice_name: str) -> Voice:

        """Returns voice from voices

        Returns:
            Voice: voice
        """
        
        if self.isVoice(voice_name):
            return self.__voices[voice_name]

    def play(self):
        for voice_name in self.__voices:
            self.__voices[voice_name].playSentence()
