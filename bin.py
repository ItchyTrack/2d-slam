if __name__ == "__main__":
    import main
    exit()


import numpy as np
import copy


class Bin:
    def __init__(self, binSize=1, minVal = -10, maxVal = 10):
        self.array = np.zeros((1, 1))
        self.binSize = binSize
        self.xShift = 0
        self.yShift = 0
        self.minVal = minVal
        self.maxVal = maxVal

    def binPoints(self, points, val = 1):
        x, y = np.array([int(i[0] / self.binSize) + self.xShift for i in points]), np.array([int(i[1] / self.binSize) + self.yShift for i in points])
        max_x, max_y = max(max(x), self.array.shape[1]), max(max(y), self.array.shape[0])
        min_x, min_y = min(min(x), 0), min(min(y), 0)
        if min_x < 0:
            self.xShift -= min_x
            x += self.xShift
        if min_y < 0:
            self.yShift -= min_y
            y += self.yShift
            
        if min_x < 0 or min_y < 0 or max_x >= self.array.shape[1] or max_y >= self.array.shape[0]:
            array = np.zeros((max_y - min_y + 2, max_x - min_x + 2))
            array[-min_x : self.array.shape[0] - min_x, -min_y : self.array.shape[1] - min_y] = self.array
            self.array = array
        # intPoints = [(int(i[0] / binSize), int(i[1] / binSize)) for i in points]
        for point in zip(x, y):
            self.array[point[1], point[0]] = max(min(self.array[point[1], point[0]] + val, self.maxVal), self.minVal)
 
    def get(self, x, y):
        return self.array[y, x]

    def copy(self):
        newBin = Bin(self.binSize)
        newBin.array = copy.deepcopy(self.array)
        newBin.xShift = self.xShift
        newBin.yShift = self.yShift
        return newBin
