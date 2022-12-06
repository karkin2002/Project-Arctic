from time import strftime, localtime

def printInfo(typeMsg: str, msg: str):

    """Prints message to the terminal with the time and a message type
    """    
    
    timeString = strftime("%H:%M:%S", localtime())
    
    print(f"[{typeMsg.upper()}] {timeString}: {msg}.") ## Displays the time, type of message, and the message itself