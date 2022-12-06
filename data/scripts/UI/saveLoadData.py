from json import load, dump
from os import path as osPath, mkdir, listdir
from glob import glob
from data.scripts.UI.printInfo import printInfo
from pygame import Surface, image as py_image
from data.scripts.basic import createMask
import data.scripts.globalVar as globalVar
globalVar.init()


def searchFiles(path: str, file_extension: str) -> list:

    """Searches a path for certain file type and returns a list of paths

    Returns:
        list: paths to files
    """    

    file_list = []

    for filename in glob(f'{path}*.{file_extension}'):
        file_list.append(filename)

    return file_list

def searchSubDir(path: str) -> list:

    """Searches a directory for all sub directories

    Returns:
        list:subdirectories
    """    

    return listdir(path)

def makeDir(path: str):

    """Creates a directory
    """    

    if not osPath.isdir(path):
        mkdir(path)


def saveData(path: str, data: dict, replace: bool = False):

    """Saves dict as a json file (include .json)

    Raises:
        Exception: File already exists
    """  

    if not replace:
        
        if not osPath.isfile(path):
            with open(path, 'w') as json_file:
                dump(data, json_file, indent=3)
        else:
            printInfo("info", f"'{path}' already exists")

    else:
        with open(path, 'w') as json_file:
            dump(data, json_file, indent=3)



def loadData(path: str) -> dict:

    """Loads dictonary saved on a json file based on the path 

    Returns:
        dict: dictonary loaded from file
    """    

    if osPath.isfile(path):
        with open(path, 'r') as json_file:
            return load(json_file)
    else:
        printInfo("info", f"'{path}' doesn't exist")
        saveData(path, {})
        return {}


# Return filename from path
def getFilename(path: str) -> str:

    """Returns a filename from a path

    Returns:
        str: Filename of the path
    """    

    return osPath.basename(path).split(".", 1)[0]


def loadImg(path: str, image_name: str = None, create_mask: bool = False) -> str:

    """Loads image from a path and adds it to the global image dict

    Raises:
        ValueError: Image not found
        ValueError: Image path not str

    Returns:
        str: Image name
    """        

    if image_name == None:
        image_name = getFilename(path)
    
    if type(path) == str:
        try:
            globalVar.image_dict[image_name] = py_image.load(path)
            printInfo("info", f"'{image_name}' img loaded")
            
            if create_mask:
                globalVar.mask_dict[image_name] = createMask(globalVar.image_dict[image_name])
            
            return image_name

        except:
            raise ValueError('Image not found')

    else:
        raise ValueError('Image path not a string')


def loadImgPath(path: str, create_mask: bool = False) -> list:

    """Loads all .png images within a folder path

    Returns:
        list: image names
    """    

    image_list = []
    
    for eachImage in searchFiles(path, "png"):

        image_list.append(loadImg(eachImage, create_mask = create_mask))

    return image_list


def getImg(img_name: str) -> Surface:

    """Returns img from global image dict

    Returns:
        Surface: img surface
    """

    return globalVar.getImage(img_name)
