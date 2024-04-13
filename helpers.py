import math

def arcuatestartend(length, location):
    #flip arcuate central location by 180 degrees to fit CANVAS angle plot
    if location == 0:
        location = 360
    else:
        location = 360 - location
    
    #divide length by 2 to get distance to move from center to get to start or end of arcuate
    space = length/2

    #determine starting arcuate location, then convert to radians
    arcstart = location - space
    if arcstart < 0:
        arcstart = 360 + arcstart
    arcstart = arcstart*(math.pi/180)
    
    #determine ending arcuate location, then convert to radians
    arcend = location + space
    if arcend > 360:
        arcend = arcend - 360
    arcend = arcend*(math.pi/180)

    return (arcstart, arcend)
