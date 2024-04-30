if __name__ == "__main__":
    import main
    exit()

import cv2
import numpy as np
import math
from bin import Bin

world = Bin(10)

shiftSize = 5
rotSize = 5

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

def doSlam(tempPoints, notBlockedPoints):
    global world
    
    # cv2.imshow("tempPoints", cv2.resize(tempPointsBin, (0,0), fx=5, fy=5))
    
    best = None
    bestError = None
    for x in range(-2, 3):
        for y in range(-2, 3):
            for r in range(-2, 3):
                error = getError(rotateAndTransformPoints(tempPoints, x*shiftSize, y*shiftSize, r*rotSize), rotateAndTransformPoints(notBlockedPoints, x*shiftSize, y*shiftSize, r*rotSize))
                error += (x*shiftSize + y*shiftSize + r*rotSize)
                if best == None or error < bestError:
                    best = (x, y, r)
                    bestError = error
    # cv2.imshow("points", cv2.resize((world.array + 10)/20, (0,0), fx=5, fy=5, interpolation = cv2.INTER_NEAREST))
    if best == None:
        return 0, 0, 0
    tempPoints = rotateAndTransformPoints(tempPoints, best[0], best[1], best[2])
    notBlockedPoints = rotateAndTransformPoints(notBlockedPoints, best[0], best[1], best[2])
    
    world.binPoints(tempPoints, 1)
    world.binPoints(notBlockedPoints, -1)
    return best

    # if len(points) < len(tempPoints):
    #     print("slam missing points")
    #     return None
    # print("slam")
    # pointToUse = np.array(points[len(points) - len(tempPoints) : len(points)])
    # pointToShift = np.array(tempPoints)
    # pointToUseNP = np.float32(pointToUse)
    # pointToShiftNP = np.float32(pointToShift)
    # return cv2.estimateAffinePartial2D(pointToShiftNP, pointToUseNP)

def getError(points, notBlockedPoints):
    error = 0
    for point in points:
        x = int(point[0] / world.binSize + world.xShift)
        y = int(point[1] / world.binSize + world.yShift)

        if x >= 0 and y >= 0 and x < world.array.shape[1] and y < world.array.shape[0]:
            if world.get(x, y) == 0:
                error -= 0.5
            elif world.get(x, y) > 0:
                error -= 1
            else:
                error += 1
        else:
            error -= 0.5

    for point in notBlockedPoints:
        x = int(point[0] / world.binSize + world.xShift)
        y = int(point[1] / world.binSize + world.yShift)
        
        if x >= 0 and y >= 0 and x < world.array.shape[1] and y < world.array.shape[0]:
            if world.get(x, y) == 0:
                error -= 0.5
            elif world.get(x, y) > 0:
                error += 1
            else:
                error -= 1
        else:
            error -= 0.5

    return error
