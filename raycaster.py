if __name__ == "__main__":
    import main
    exit()

import cv2
import math
import random as r
map = cv2.imread("map.png",  cv2.IMREAD_GRAYSCALE)


def raycast(x, y, dir, maxLength, error=0):
    i = 0
    xShift = math.cos(math.radians(dir))
    yShift = math.sin(math.radians(dir))
    while i <= maxLength:
        try:
            if not (y+yShift*i > map.shape[0] or y+yShift*i < 0 or x+xShift*i > map.shape[1] or x+xShift*i < 0):
                if error == 0:
                    if map[int(y+yShift*i), int(x+xShift*i)] < 100:
                        return True, (x+xShift*i, y+yShift*i)
                elif map[int(y+yShift*i), int(x+xShift*i)] < 100:
                    return True, (x+xShift*(i + r.randrange(-error, error)), y+yShift*(i + r.randrange(-error, error)))
        except:
            pass
        i += 0.5
    return False, (x+xShift*maxLength, y+yShift*maxLength)