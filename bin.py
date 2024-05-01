if __name__ == "__main__":
    import main
    exit()


import numpy as np
import copy


class Bin:
    def __init__(self, binSize=1, minVal = -10, maxVal = 10, mode = "set"):
        self.array = np.zeros((1, 1))
        self.binSize = binSize
        self.xShift = 0
        self.yShift = 0
        self.minVal = minVal
        self.maxVal = maxVal
        self.mode = mode

    def binPoints(self, points, val = 1):
        if len(points) == 0:
            return
        x, y = np.array([int(i[0] / self.binSize) + self.xShift for i in points]), np.array([int(i[1] / self.binSize) + self.yShift for i in points])
        max_x, max_y = max(max(x), self.array.shape[1]-1), max(max(y), self.array.shape[0]-1)
        min_x, min_y = min(min(x), 0), min(min(y), 0)
        if min_x < 0:
            self.xShift -= min_x
            x -= min_x
        if min_y < 0:
            self.yShift -= min_y
            y -= min_y
            
        if min_x < 0 or min_y < 0 or max_x >= self.array.shape[1] or max_y >= self.array.shape[0]:
            array = np.zeros((max_y - min_y + 1, max_x - min_x + 1))
            array[-min_y : self.array.shape[0] - min_y, -min_x : self.array.shape[1] - min_x] = self.array
            self.array = array
        # intPoints = [(int(i[0] / binSize), int(i[1] / binSize)) for i in points]
        for point in zip(x, y):
            if self.mode == "add":
                self.array[point[1], point[0]] = max(min(self.array[point[1], point[0]] + val, self.maxVal), self.minVal)
            elif self.mode == "set":
                self.array[point[1], point[0]] = max(min(val, self.maxVal), self.minVal)

    def get(self, x, y):
        x += self.xShift
        y += self.yShift
        if x < 0 or y < 0 or x >= self.array.shape[1] or y >= self.array.shape[0]:
            return None
        return self.array[y, x]

    def copy(self):
        newBin = Bin(self.binSize)
        newBin.array = copy.deepcopy(self.array)
        newBin.xShift = self.xShift
        newBin.yShift = self.yShift
        return newBin

    def getArea(self, x1, y1, x2, y2):
        x1 += self.xShift
        y1 += self.yShift
        x2 += self.xShift
        y2 += self.yShift
        min_x = min(x1, 0)
        min_y = min(y1, 0)
        max_x = max(x2, self.array.shape[1])
        max_y = max(y2, self.array.shape[0])
        if min_x < 0:
            x1 -= min_x
            x2 -= min_x
        if min_y < 0:
            y1 -= min_y
            y2 -= min_y
        if min_x < 0 or min_y < 0 or max_x >= self.array.shape[1] or max_y >= self.array.shape[0]:
            array = np.zeros((max_y - min_y + 2, max_x - min_x + 2))
            array[-min_y : self.array.shape[0] - min_y, -min_x : self.array.shape[1] - min_x] = self.array
            return array[y1:y2, x1:x2]
        else:
            return copy.deepcopy(self.array)[y1:y2, x1:x2]
