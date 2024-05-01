import cv2
import numpy as np
import numpy.ma as ma
import math
from bin import Bin
from time import sleep
from slam import getError

world = Bin(1, -1, 1, "add")

# shiftSize = 2
rotSize = 0

shiftCount = 3
rotCount = 0

best = None
bestError = None


seen = Bin(world.binSize, world.minVal, world.maxVal, world.mode)
seen.binPoints(
    [
        [0, 0],
        [10, 10],
        [5, 5],
    ]
)

world.binPoints(
    [
        [0, 0],
        [1, 1],
        [1, 0],
        [0, 1],
        [10, 10],
        [5, 5],
    ]
)

# for r in range(-rotCount, rotCount+1):
#         seen = Bin(world.binSize, world.minVal, world.maxVal, world.mode)
#         seen.binPoints(rotatePoints(tempPoints, math.sin(math.radians(r * rotSize)), math.cos(math.radians(r * rotSize))), 1)
#         seen.binPoints(rotatePoints(notBlockedPointsSmall, math.sin(math.radians(r * rotSize)), math.cos(math.radians(r * rotSize))), -1)
xSize = seen.array.shape[1]
ySize = seen.array.shape[0]
r = 0
for x in range(-shiftCount, shiftCount+1):
    for y in range(-shiftCount, shiftCount+1):
        print(x, y)
        worldArray = world.getArea(-seen.xShift+x, -seen.yShift+y, xSize-seen.xShift+x, ySize-seen.yShift+y)
        seenArray = seen.array
        error = getError(worldArray, seenArray)
        # print(error)
        error += (abs(x*world.binSize) + abs(y*world.binSize) + abs(r*rotSize)) / (shiftCount*world.binSize*2+rotCount*rotSize) * 0.5
        # print(error)
        if (best == None or error < bestError) and not math.isnan(error):
            print("new best:", error, (x*world.binSize, y*world.binSize, r*rotSize))
            best = (x*world.binSize, y*world.binSize, r*rotSize)
            bestError = error
print(best)