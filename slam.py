if __name__ == "__main__":
    import main

    exit()

import cv2
import numpy as np
import numpy.ma as ma
import math
from bin import Bin
from time import sleep

world = Bin(4, -2, 2, "add")

# shiftSize = 2
rotSize = 0

shiftCount = 4
rotCount = 0

def rotateAndTransformPoints(points, x, y, r, arrayToAddTo=None):
    if arrayToAddTo == None:
        arrayToAddTo = []
    for point in points:
        arrayToAddTo.append(
            [
                point[0] * math.cos(math.radians(r)) + point[1] * -math.sin(math.radians(r)) + x,
                point[0] * math.sin(math.radians(r)) + point[1] * math.cos(math.radians(r)) + y,
            ]
        )
    return arrayToAddTo


def rotatePoints(points, sinr, cosr, arrayToAddTo=None):
    if arrayToAddTo == None:
        arrayToAddTo = []
    for point in points:
        arrayToAddTo.append([point[0] * cosr + point[1] * -sinr, point[0] * sinr + point[1] * cosr])
    return arrayToAddTo


def rotateAndTransformPoint(point, x, y, r):
    return [
        point[0] * math.cos(math.radians(r)) + point[1] * -math.sin(math.radians(r)) + x,
        point[0] * math.sin(math.radians(r)) + point[1] * math.cos(math.radians(r)) + y,
    ]

def doSlam(tempPoints, notBlockedPointsArrays):
    # sleep(0.01)
    global world
    
    notBlockedPoints = np.ndarray((0, 2))
    notBlockedPointsSmall = np.ndarray((0, 2))
    for notPoints in notBlockedPointsArrays:
        notBlockedPoints = np.concatenate((notBlockedPoints, notPoints))
        notBlockedPointsSmall = np.concatenate((notBlockedPointsSmall, notPoints[(max(len(notPoints) - 4, 0)) : -1]))

    notBlockedPointsBins = Bin(world.binSize, 0, 1)
    notBlockedPointsBins.binPoints(notBlockedPointsSmall, 1)

    # notBlockedPointsSmall = []
    # for y in range(notBlockedPointsBins.array.shape[0]):
    #     y -= notBlockedPointsBins.yShift
    #     for x in range(notBlockedPointsBins.array.shape[1]):
    #         x -= notBlockedPointsBins.xShift
    #         if notBlockedPointsBins.get(x, y) != 0:
    #             notBlockedPointsSmall.append([x * world.binSize, y * world.binSize])
    # print(len(notBlockedPointsSmall))
    # print(len(tempPoints))

    # best = None
    # bestError = None
    # for r in range(-rotCount, rotCount+1):
    #     seen = Bin(world.binSize, world.minVal, world.maxVal, world.mode)
    #     seen.binPoints(rotatePoints(tempPoints, math.sin(math.radians(r * rotSize)), math.cos(math.radians(r * rotSize))), 1)
    #     seen.binPoints(rotatePoints(notBlockedPointsSmall, math.sin(math.radians(r * rotSize)), math.cos(math.radians(r * rotSize))), -1)
    #     xSize = seen.array.shape[1]
    #     ySize = seen.array.shape[0]
    #     for x in range(-shiftCount, shiftCount+1):
    #         for y in range(-shiftCount, shiftCount+1):
                
    #             worldArray = world.getArea(-seen.xShift+x, -seen.yShift+y, xSize-seen.xShift+x, ySize-seen.yShift+y)
    #             seenArray = seen.array
    #             error = getError(worldArray, seenArray)
    #             # print(error)
    #             error += (abs(x*world.binSize) + abs(y*world.binSize) + abs(r*rotSize)) / (shiftCount*world.binSize*2+rotCount*rotSize) * 0.1
    #             # print(error)
    #             if (best == None or error < bestError) and not math.isnan(error):
    #                 print("new best:", error, (x*world.binSize, y*world.binSize, r*rotSize))
    #                 best = (x*world.binSize, y*world.binSize, r*rotSize)
    #                 bestError = error
                
    # if best == None:
    #     best = 0, 0, 0
    # tempPoints = rotatePoints(tempPoints, math.sin(math.radians(best[2])), math.cos(math.radians(best[2])))
    # notBlockedPoints = rotatePoints(notBlockedPoints, math.sin(math.radians(best[2])), math.cos(math.radians(best[2])))
    # for point in tempPoints:
    #     point[0] += best[0]
    #     point[1] += best[1]
    # for point in notBlockedPoints:
    #     point[0] += best[0]
    #     point[1] += best[1]

    world.binPoints(tempPoints, 1)
    world.binPoints(notBlockedPoints, -1)
    return 0, 0, 0 #best

def getError(wolrdArray: np.ndarray, seenArray: np.ndarray):
    global i
    # print("get error")
    # print(wolrdArray.shape)
    # print(seenArray.shape)
    worldMask = (wolrdArray != 0).astype(np.int8)
    seenMask = (seenArray != 0).astype(np.int8)
    w = pow((wolrdArray*seenMask - seenArray*worldMask)/(world.maxVal - world.minVal), 2)[seenMask * worldMask == 1]

    # cv2Image = cv2.resize((wolrdArray - world.minVal)/(world.maxVal - world.minVal), (0,0), fx=world.binSize, fy=world.binSize, interpolation = cv2.INTER_NEAREST)
    # cv2.imshow("wolrdArray", cv2Image)
    # cv2Image = cv2.resize((seenArray - world.minVal)/(world.maxVal - world.minVal), (0,0), fx=world.binSize, fy=world.binSize, interpolation = cv2.INTER_NEAREST)
    # cv2.imshow("seenArray", cv2Image)
    # cv2Image = cv2.resize((wolrdArray*seenMask - world.minVal)/(world.maxVal - world.minVal), (0,0), fx=world.binSize, fy=world.binSize, interpolation = cv2.INTER_NEAREST)
    # cv2.imshow("wolrdArray2", cv2Image)
    # cv2Image = cv2.resize((seenArray*worldMask - world.minVal)/(world.maxVal - world.minVal), (0,0), fx=world.binSize, fy=world.binSize, interpolation = cv2.INTER_NEAREST)
    # cv2.imshow("seenArray2", cv2Image)
    # pows = pow((wolrdArray*seenMask - seenArray*worldMask)/(world.maxVal - world.minVal), 2)
    # cv2Image = cv2.resize(pows, (0,0), fx=world.binSize, fy=world.binSize, interpolation = cv2.INTER_NEAREST)
    # cv2.imshow("pows", cv2Image)
    # print(np.mean(w))
    # if w.size != 0:
    #     cv2Image = cv2.resize(w, (0,0), fx=world.binSize, fy=world.binSize, interpolation = cv2.INTER_NEAREST)
    #     cv2.imshow("array", cv2Image)
    # cv2.waitKey(1000)

    return np.mean(w)
