if __name__ == "__main__":
    import main
    exit()

import math
import pygame
from pygame import gfxdraw
import raycaster
from slam import doSlam

points = []
tempPoints = []
rot = 0
dir = 1
carRot = 0
car = [170, 170]

speed = 1
deadCar = [170, 170]
deadCarRot = 0
deadCarError = 0.03
deadCarRotError = 0.04

def update(dt: float, screen, pressed):
    global rot, dir, carRot, car, deadCar, deadCarRot, deadCarError, points, deadCarRotError, tempPoints
    if pygame.K_w in pressed:
        car[0] += math.cos(math.radians(carRot)) * dt *0.1 * speed
        car[1] += math.sin(math.radians(carRot)) * dt *0.1 * speed
        
        deadCar[0] += (math.cos(math.radians(deadCarRot)) + deadCarError) * dt * 0.1 * speed
        deadCar[1] += (math.sin(math.radians(deadCarRot)) + deadCarError) * dt * 0.1 * speed

    if pygame.K_s in pressed:
        car[0] -= math.cos(math.radians(carRot)) * dt *0.1 * speed
        car[1] -= math.sin(math.radians(carRot)) * dt *0.1 * speed

        deadCar[0] -= (math.cos(math.radians(deadCarRot)) + deadCarError) * dt * 0.1 * speed
        deadCar[1] -= (math.sin(math.radians(deadCarRot)) + deadCarError) * dt * 0.1 * speed

    if pygame.K_a in pressed:
        carRot -= dt * 0.3 * speed
        deadCarRot -= dt * 0.3 * (1 + deadCarRotError) * speed
    if pygame.K_d in pressed:
        carRot += dt * 0.3 * speed
        deadCarRot += dt * 0.3 * (1 + deadCarRotError) * speed
    if carRot > 360:
        carRot - 360
    elif carRot < 0:
        carRot + 360
    if deadCarRot > 360:
        deadCarRot - 360
    elif deadCarRot < 0:
        deadCarRot + 360

    for i in range(1):
        rot += dir * dt * 0.3
        hit, pos = raycaster.raycast(car[0], car[1], rot + carRot, 200, 0)
        if hit:
            x = pos[0]-car[0]
            y = pos[1]-car[1]
            angle = math.degrees(math.atan2(y, x)) - carRot + deadCarRot
            length = math.hypot(x, y)
            deadPos = (
                math.cos(math.radians(angle))*length+deadCar[0],
                math.sin(math.radians(angle))*length+deadCar[1]
            )
            points.append(deadPos)
            # tempPoints.append(deadPos)
        if rot >= 90:
            dir = -1
        elif rot <= -90:
            dir = 1
    # if len(tempPoints) >= 50:
    #     dif = doSlam(points, tempPoints)
    #     if dif == None or type(dif[0]) == None:
    #         for point in tempPoints:
    #             points.append(point)
    #     else:
    #         dif = dif[0]
    #         print(dif)
    #         # dif[0, 0] = 0
    #         # dif[0, 1] = 0
    #         # dif[1, 0] = 0
    #         # dif[1, 1] = 0
    #         for point in tempPoints:
    #             points.append(
    #                 [
    #                     dif[0, 0] * point[0] + dif[0, 1] * point[1] + dif[0, 2],
    #                     dif[1, 0] * point[0] + dif[1, 1] * point[1] + dif[1, 2]
    #                 ]
    #             )
    #         point = (deadCar[0], deadCar[1])
    #         newDeadCar = [
    #             dif[0, 0] * point[0] + dif[0, 1] * point[1] + dif[0, 2],
    #             dif[1, 0] * point[0] + dif[1, 1] * point[1] + dif[1, 2]
    #         ]
    #         point = [
    #             deadCar[0] + math.cos(math.radians(deadCarRot)),
    #             deadCar[1] + math.sin(math.radians(deadCarRot))
    #         ]
    #         newDeadCarForw = [
    #             dif[0, 0] * point[0] + dif[0, 1] * point[1] + dif[0, 2],
    #             dif[1, 0] * point[0] + dif[1, 1] * point[1] + dif[1, 2]
    #         ]
    #         deadCar[0] = newDeadCar[0]
    #         deadCar[1] = newDeadCar[1]
    #         print(newDeadCarForw[1] - newDeadCar[1], newDeadCarForw[0] - newDeadCar[0])
    #         deadCarRot = math.degrees(math.atan2(newDeadCarForw[1] - newDeadCar[1], newDeadCarForw[0] - newDeadCar[0]))
    #     tempPoints = []


def draw(screen: pygame.Surface):
    global carRot, car, deadCar, deadCarRot
    gfxdraw.filled_circle(screen, int(deadCar[0]), int(deadCar[1]), 5, (100, 0, 0))
    gfxdraw.filled_circle(screen, int(deadCar[0]), int(deadCar[1] + screen.get_size()[1] / 2), 5, (100, 0, 0))
    gfxdraw.filled_circle(screen, int(deadCar[0] + math.cos(math.radians(deadCarRot))*6), int(deadCar[1] + math.sin(math.radians(deadCarRot))*6), 3, (0, 100, 0))
    gfxdraw.filled_circle(screen, int(deadCar[0] + math.cos(math.radians(deadCarRot))*6), int(deadCar[1] + screen.get_size()[1] / 2 + math.sin(math.radians(deadCarRot))*6), 3, (0, 100, 0))
    
    gfxdraw.filled_circle(screen, int(car[0]), int(car[1]), 5, (255, 0, 0))
    gfxdraw.filled_circle(screen, int(car[0]), int(car[1] + screen.get_size()[1] / 2), 5, (255, 0, 0))
    gfxdraw.filled_circle(screen, int(car[0] + math.cos(math.radians(carRot))*6), int(car[1] + math.sin(math.radians(carRot))*6), 3, (0, 255, 0))
    gfxdraw.filled_circle(screen, int(car[0] + math.cos(math.radians(carRot))*6), int(car[1] + screen.get_size()[1] / 2 + math.sin(math.radians(carRot))*6), 3, (0, 255, 0))

    
    for point in points:
        gfxdraw.filled_circle(screen, int(point[0]), int(point[1]) + int(screen.get_size()[1] / 2), 2, (0, 0, 0))

    for point in tempPoints:
        gfxdraw.filled_circle(screen, int(point[0]), int(point[1]) + int(screen.get_size()[1] / 2), 2, (100, 100, 100))
