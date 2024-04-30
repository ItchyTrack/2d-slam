# from
# https://sakshibadoni053.medium.com/digital-differential-analyzer-dda-algorithm-using-python-fe50cad44608

import numpy as np

def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
   
    # calculate steps required for generating pixels 
   
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)
         
    #calculate increment in x & y for each steps
    Xinc = float(dx / steps)
    Yinc = float(dy / steps)
    
    coordinates = []
    for i in range(0, int(steps + 1)):
		 # Draw pixels
        coordinates.append([int(x1), int(y1)])
        x1 += Xinc
        y1 += Yinc
    return coordinates
