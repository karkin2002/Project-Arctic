from pygame import mixer
from data.scripts.UI.printInfo import printInfo
from data.scripts.UI.saveLoadData import getFilename

## Sets volume of audio class
def setAudioVolume(audio, value):
    audio.set_volume(value/100)
        


## Sets num of audio channels
def setNumChannels(value: int):

    """Sets number of audio channels (how many sounds you caan play at once).
    """

    mixer.set_num_channels(value)

## Gets the num of audio channels
def getNumChannels() -> int:

    """Returns num of audio channels.

    Returns:
        int: num of audio channels
    """

    return mixer.get_num_channels()

## Adds a new channel
def addChannel():

    """Adds a new audio channel.
    """

    setNumChannels(getNumChannels()+1)

## finds an empty channel, creates new if no empty
def findChannel(max_channels: int) -> mixer.Channel:

    """Finds a channel with no audio playing, otherwise creates a new one,
    otherwise return None.

    Returns:
        Channel: empty channel
    """

    audioChannel = mixer.find_channel()
    
    if audioChannel != None:
        return audioChannel
    
    else:
        if getNumChannels() < max_channels:
            addChannel()
            printInfo("Info", f"Added new Channel [{getNumChannels()}]")
            return mixer.Channel(getNumChannels()-1)

        else:
            printInfo("Info", f"findChannel - Max Channels reached [{getNumChannels()}]")





## Audio Category
class AudioCategory:
    def __init__(self, name, volume, channel = False):
        self.name = name
        self.volume = volume
        self.mute = False

        self.audioDict = {}
    

    ## Returns the name of the audio category
    def getName(self) -> str:

        """Returns the name of the audio category.

        Returns:
            str: audio category name
        """

        return self.name
    
    ## Returns the volume of an audio
    def getVolume(self) -> float:

        """Returns volume of the audio category

        Returns:
            float: volume
        """

        return self.volume
    
    ## checks if an audio is in the audioDict
    def isAudio(self, name: str) -> bool:

        """Returns whether an audio is in audio dict

        Returns:
            bool: audio in audio dict
        """

        if name in self.audioDict:
            return True
        else:
            printInfo("Error", f"isAudio - Audio doesn't exist [{name}]")

    ## returns a audio class
    def __getAudio(self, name: str):

        """Returns audio from audio dict

        Returns:
            Audio: audio
        """

        return self.audioDict[name]

    # Sets the volume of the category
    def setCatVolume(self, overallVolume: float, value: float):

        """Sets the category volume
        """

        self.volume = value
        for eachAudio in self.audioDict:
            self.setAudioVolume(eachAudio, overallVolume)

    ## Sets the volume of an audio
    def setAudioVolume(self, name: str, overallVolume: float, value: float = None):
        
        """Sets the volume of an audio
        """
        
        if self.isAudio(name):
            audio = self.__getAudio(name)
            if value != None:
                audio.setVolume(value)

                # (overall*(category/100))*(audio/100)
                volumeValue = (overallVolume * (self.volume/100)) * (audio.getVolume()/100)
                setAudioVolume(audio.getAudio(), volumeValue)
        
        else:
            printInfo("Error", f"setAudioVolume - Audio doesn't exist [{name}]")

    ## Adds audio to the audioDict and sets its volume, doesn't play the audio
    def addAudio(self, name: str, dir: str, overallVolume: float, volume: float = 50):

        """Adds audio to audio dict, sets its volume (doesn't play the audio)
        """

        if name == None:
            name = getFilename(dir)
        self.audioDict[name] = Audio(name, dir, volume)
        self.setAudioVolume(name, overallVolume, value = None)
        
        printInfo("INFO", f"New audio added [{self.name}] [{name}]")

    ## Plays audio
    def playAudio(self, name: str, max_channels: int, loops: int = 0):

        """Plays audio
        """

        self.__getAudio(name).play(max_channels, loops)

    ## Finds which channel an audio is playing in
    def __findChannelByAudio(self, name: str) -> mixer.Channel:

        """Returns a channel which an audio is playing in

        Returns:
            Channel: channel with audio playing
        """

        audio = self.__getAudio(name).audio
        for eachChannel in range(getNumChannels()):
            if mixer.Channel(eachChannel).get_sound() == audio:
                return eachChannel

    ## Pauses an audio
    def pauseAudio(self, name: str):

        """Pauses an audio
        """

        mixer.Channel(self.__findChannelByAudio(name)).pause()

    ## Unpauses an audio
    def unpauseAudio(self, name: str):

        """Unpauses an audio
        """

        mixer.Channel(self.__findChannelByAudio(name)).unpause()

    ## Queues an audio after another audio on a channel
    def queueAudio(self, audio_name: str, audio_queue_name: str):

        """Queues an audio after another audio on a specific channel
        """

        if self.isAudio(audio_name) and self.isAudio(audio_queue_name):
            channel = self.__findChannelByAudio(audio_name)
            mixer.Channel(channel).queue(self.__getAudio(audio_queue_name).getAudio())

        else:
            printInfo("Error", f"queueAudio - audio_name or audio_queue_name name is invalid [{audio_name, audio_queue_name}]")



## Audio
class Audio:

    """Class for individual audio
    """

    def __init__(self, name: str, dir: str, volume: float = 50):
        self.name = name
        self.setVolume(volume)

        self.audio = mixer.Sound(dir) 

    def getName(self):
        return self.name

    def getVolume(self):
        return self.volume

    def setVolume(self, value):
        self.volume = value

    def getAudio(self):
        return self.audio

    def play(self, max_channels, loops = 0):
        channel = findChannel(max_channels)
        if channel != None:
            channel.play(self.audio, loops)







## Class used for all audio on the UI
class UIAudio:

    """Handles all UI audio
    """

    def __init__(self, 
            volume: float, 
            max_channels: int = 16, 
            frequency: int = 44100, 
            size: int = -16, 
            channels: int = 2, 
            buffer: int = 512, 
            device_name: str = None):
        
        self.volume = volume

        self.cat_dict = {}

        mixer.pre_init(frequency, size, channels, buffer, device_name) # Initialising the mixer
        mixer.init()

        self.max_channels = max_channels

        if max_channels < getNumChannels():
            setNumChannels(max_channels)
        
    ## Returns whether the category exists
    def __isCat(self, cat_name: str):

        if cat_name in self.cat_dict:
            return True
        
        else:
            printInfo("Error", f"'{cat_name}' audio cat doen't exist")
            return False

    ## Retruns the audio cat object
    def __getAudioCat(self, cat_name):
        if self.__isCat(cat_name):
            return self.cat_dict[cat_name]

    ## Adds a new Audio Cat to a dict
    def addCat(self, cat_name: str, volume: float = 50):

        """Adds a new category
        """

        if not cat_name in self.cat_dict:
            self.cat_dict[cat_name] = AudioCategory(cat_name, volume)
            printInfo("Info", f"'{cat_name}' audio cat created")

        else:
            printInfo("Info", f"'{cat_name}' audio cat already exists")

    ## Adds an audio to an audioCat
    def addAudio(self, cat_name: str, dir: str, audio_name: str = None , volume: float = 50):

        """Adds a new audio to an category
        """

        self.__getAudioCat(cat_name).addAudio(audio_name, dir, self.volume, volume)
    
    ## Sets the volume of the audioCat
    def setCatVolume(self, cat_name: str, value: float):

        """Sets the category volume
        """

        self.__getAudioCat(cat_name).setCatVolume(self.volume, value)

    ## Sets the audio in the audioCat
    def setAudioVolume(self, cat_name: str, audio_name: str, value: float):

        """Sets an audio's volume
        """

        self.__getAudioCat(cat_name).setAudioVolume(audio_name, self.volume, value)

    ## Plays an audio
    def play(self, cat_name: str, audio_name: str, loops: int = 0):

        """Plays an audio
        """

        if self.__getAudioCat(cat_name).isAudio(audio_name):
            self.__getAudioCat(cat_name).playAudio(audio_name, self.max_channels, loops)

    ## Pauses the audio
    def pause(self, cat_name: str, audio_name: str):

        """Pauses an audio
        """

        if self.__getAudioCat(cat_name).isAudio(audio_name):
            self.__getAudioCat(cat_name).pauseAudio(audio_name)

    ## Unpauses the audio
    def unpause(self, cat_name: str, audio_name: str):

        """Unpauses an audio
        """

        if self.__getAudioCat(cat_name).isAudio(audio_name):
            self.__getAudioCat(cat_name).unpauseAudio(audio_name)

    ## Queue an audio
    def queue(self, cat_name: str, audio_name: str, audio_queue_name: str):

        """Queues an audio
        """

        self.__getAudioCat(cat_name).queueAudio(audio_name, audio_queue_name)