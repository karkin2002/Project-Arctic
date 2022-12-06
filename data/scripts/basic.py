from pygame import Surface, mask as pymask, transform as pytrans, Surface as pysurf, Rect
from math import sin, cos, sqrt
from time import time


## ------ Math  ------ ##

## Returns a x or y, from an x or y input
def sinWave(value, origin, wavelength, amplitude):
    return sin(value/wavelength) * amplitude + origin

## Returns distance between two points
def distanceBetweenPoints(x1,y1,x2,y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

## Expoentially move towards a point
def exponential(point1, point2, velocity, exponentialValue, dt):
    distance = abs(point1 - point2)

    distanceVelocity = distance / exponentialValue

    if point1 > point2:
        point1 -= (velocity * distanceVelocity) * dt
    
    elif point1 < point2:
        point1 += (velocity * distanceVelocity) * dt

    return point1

## Checks whether a point is in a circle
def inCircle(circlePos,r,pointPos): 
    return ((pointPos[0] - circlePos[0]) * (pointPos[0] - circlePos[0]) + 
        (pointPos[1] - circlePos[1]) * (pointPos[1] - circlePos[1]) <= r * r)

def circleCoord(radius: float, degree: float) -> tuple:
    
    """Returns coord around a circle

    Returns:
        tuple: coord
    """

    return (
        radius * cos(degree),
        radius * sin(degree))


## ------  Collide  ------ ##

## Create a mask from an image
def createMask(image: Surface) -> pymask:

    """Creates mask from Surface (used for collision)

    Returns:
        mask: mask of surface
    """

    return pymask.from_surface(image)


## Checks if the mask is collides with another
def isMaskCollision(mask_1: pymask, mask_pos_1: tuple, mask_2: pymask, mask_pos_2: tuple) -> bool:

    """Returns whether two masks overlap

    Returns:
        bool: masks overlap
    """
    
    if Rect(mask_pos_1[0], mask_pos_1[1], mask_1.get_size()[0], mask_1.get_size()[1]).colliderect(Rect(mask_pos_2[0], mask_pos_2[1], mask_2.get_size()[0], mask_2.get_size()[1])):
        offset = (round(mask_pos_2[0] - mask_pos_1[0]), round(mask_pos_2[1] - mask_pos_1[1]))

        return mask_1.overlap(mask_2, offset) != None
    
    else:
        return False


## Checks if the mask is collides with another
def isMaskCollidepoint(mask: pymask, mask_pos: tuple, collide_pos: tuple) -> bool:

    """Returns whether two masks overlap

    Returns:
        bool: masks overlap
    """

    return isMaskCollision(mask, mask_pos, POINT_MASK, collide_pos)



## ------  Time  ------ ##

## Returns the time in seconds
def getTime():
    return time()

## Shows the amount of time passed in seconds
def timeElapsed(oldTime):
    return time() - oldTime

## Enter the time in seconds until the timer ends
def setTimer(seconds):
    return time() + seconds

## Retruns True if the timer is done
def isTimer(timer):
    return timer - time() <= 0


## ------  Surface  ------ ##

def rotSurf(surf: Surface, angle: int):

    """Rotates surf & returns it & it's center pos.

    Returns:
        surf: rotated surface
        tuple: center pos of rotated surface
    """

    if angle % 360 != 0:
        rotatedSurf = pytrans.rotate(surf, angle)
    else:
        rotatedSurf = surf
        

    rotatedSurfCenter = (int(rotatedSurf.get_width()/2), int(rotatedSurf.get_height()/2))
    

    return rotatedSurf, rotatedSurfCenter

def alphaSurf(surf: Surface, alpha: int) -> Surface:
    
    """Creates an alpha copy of a surf

    Returns:
        surface: alpha surface copy
    """    
    
    if alpha < 255:
        alpha_surf = Surface((surf.get_width(), surf.get_height()))
        alpha_surf.set_colorkey((0,0,0))
        alpha_surf.set_alpha(alpha)
        alpha_surf.blit(surf, (0, 0))
    
    else:
        alpha_surf = surf

    return alpha_surf



global POINT_MASK

point_surf = Surface((1,1))
point_surf.fill((1, 1, 1))

POINT_MASK = createMask(point_surf)