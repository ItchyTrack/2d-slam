if __name__ == "__main__":
    import main
    exit()

import cv2
import numpy as np
import math
from bin import Bin
from dda import dda

world = Bin(5)

def rotateAndTransformPoints(points, x, y, r, arrayToAddTo = None):
    if arrayToAddTo == None:
        arrayToAddTo = []
    for point in points:
        arrayToAddTo.append([
            point[0] * math.cos(math.radians(r)) + point[1] * -math.sin(math.radians(r)) + x,
            point[0] * math.sin(math.radians(r)) + point[1] * math.cos(math.radians(r)) + y
        ])
    return arrayToAddTo

def rotateAndTransformPoint(point, x, y, r):
    return [
        point[0] * math.cos(math.radians(r)) + point[1] * -math.sin(math.radians(r)) + x,
        point[0] * math.sin(math.radians(r)) + point[1] * math.cos(math.radians(r)) + y
    ]

def doSlam(tempPoints, tempPositions):
    global world
    
    # cv2.imshow("tempPoints", cv2.resize(tempPointsBin, (0,0), fx=5, fy=5))
    notBlockedPoints = np.ndarray((0, 2))
    for i in range(len(tempPoints)):
        point = tempPoints[i]
        pos = tempPositions[i]
        notBlockedPoints = np.concatenate((notBlockedPoints, dda(pos[0]/world.binSize, pos[1]/world.binSize, point[0]/world.binSize, point[1]/world.binSize)))
    for point in notBlockedPoints:
        point[0] = point[0] * world.binSize
        point[1] = point[1] * world.binSize
    
    best = None
    # for x in range(-3, 4):
    #     for y in range(-3, 4):
    #         for r in range(-3, 4):
    #             worldCopy = world.copy()
    #             worldCopy.binPoints(tempPoints)
    #             worldCopy.array
    world.binPoints(tempPoints, 1)
    world.binPoints(notBlockedPoints, -1)
    cv2.imshow("points", cv2.resize((world.array + 10)/20, (0,0), fx=5, fy=5, interpolation = cv2.INTER_NEAREST))
    return 0, 0, 0

    # if len(points) < len(tempPoints):
    #     print("slam missing points")
    #     return None
    # print("slam")
    # pointToUse = np.array(points[len(points) - len(tempPoints) : len(points)])
    # pointToShift = np.array(tempPoints)
    # pointToUseNP = np.float32(pointToUse)
    # pointToShiftNP = np.float32(pointToShift)
    # return cv2.estimateAffinePartial2D(pointToShiftNP, pointToUseNP)
