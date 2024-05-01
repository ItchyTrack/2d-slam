if __name__ == "__main__":
    import main
    exit()

from dda import dda
import cv2
import math
import random as r
map = cv2.imread("map.png",  cv2.IMREAD_GRAYSCALE)


def raycast(x, y, dir, maxLength, error=0):
    i = 0
    xShift = math.cos(math.radians(dir))
    yShift = math.sin(math.radians(dir))
    points = dda(x, y, x+xShift*maxLength, y+yShift*maxLength)
    for point in points:
        pointX = point[0]
        pointY = point[1]
        length = math.sqrt(pow(pointY-y, 2) + pow(pointX - x, 2))
        try:
            if not (pointY > map.shape[0] or pointY < 0 or pointX > map.shape[1] or pointX < 0):
                if error == 0:
                    if map[int(pointY), int(pointX)] < 100:
                        return True, (pointX, pointY)
                elif map[int(pointY), int(pointX)] < 100:
                    return True, (x+xShift*(x- + r.randrange(-error, error)), y+yShift*(i + r.randrange(-error, error)))
        except:
            pass
        i += 0.1
    return False, (x+xShift*maxLength, y+yShift*maxLength)