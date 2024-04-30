if __name__ == "__main__":
    import main
    exit()


import cv2
import numpy as np
import math


def binPoints(points, binSize=1):
    x, y = [i[0] for i in points], [i[1] for i in points]
    max_x, max_y = max(x), max(y)

    image = np.zeros((int((max_y) / binSize + 1), int((max_x) / binSize + 1)))

    intPoints = [(int(i[0] / binSize), int(i[1] / binSize)) for i in points]
    for point in intPoints:
        image[point[1], point[0]] = 1
    # image[intPoints] = 255
    return image

def rotateAndTransformPoints(points, x, y, r):
    newPoints = []
    for point in points:
        newPoints.append([
            point[0] * math.cos(math.radians(r)) + point[1] * -math.sin(math.radians(r)) + x,
            point[0] * math.sin(math.radians(r)) + point[1] * math.cos(math.radians(r)) + y
        ])
    return newPoints

def rotateAndTransformPoint(point, x, y, r):
    return [
        point[0] * math.cos(math.radians(r)) + point[1] * -math.sin(math.radians(r)) + x,
        point[0] * math.sin(math.radians(r)) + point[1] * math.cos(math.radians(r)) + y
    ]

def doSlam(points, tempPoints):
    if len(points) < 100:
        return None
    pointsBin = binPoints(points, 10)
    tempPointsBin = binPoints(tempPoints, 10)
    cv2.imshow("points", cv2.resize(pointsBin, (0,0), fx=10, fy=10))
    cv2.imshow("tempPoints", cv2.resize(tempPointsBin, (0,0), fx=10, fy=10))
    return None

    # if len(points) < len(tempPoints):
    #     print("slam missing points")
    #     return None
    # print("slam")
    # pointToUse = np.array(points[len(points) - len(tempPoints) : len(points)])
    # pointToShift = np.array(tempPoints)
    # pointToUseNP = np.float32(pointToUse)
    # pointToShiftNP = np.float32(pointToShift)
    # return cv2.estimateAffinePartial2D(pointToShiftNP, pointToUseNP)
