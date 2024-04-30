import sys
import pygame
from pygame.locals import *
import slamMain
pygame.init()

backgroundImage = pygame.image.load("map.png")

font = pygame.font.Font("freesansbold.ttf", 32)

fps = 60
fpsClock = pygame.time.Clock()

size = width, height = backgroundImage.get_size()[0], backgroundImage.get_size()[1] * 2
screen: pygame.surface.Surface = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

buttonUpdates = []
buttonDraws = []

class Button:
    def __init__(self, surface: pygame.Surface, pos, screenPos: tuple, func) -> None:
        self.surface = surface
        self.func = func
        self.pos = pos
        self.screenPos = screenPos
        buttonUpdates.append(self.check)
        buttonDraws.append(self.draw)

    def draw(self, screen: pygame.Surface):
        screen.blit(
            self.surface,
            (self.pos[0] + screen.get_width() * self.screenPos[0], self.pos[1] + screen.get_height() * self.screenPos[1]),
        )
        self.screen = screen

    def check(self):
        mouse = pygame.mouse.get_pos()
        width = self.surface.get_width()
        height = self.surface.get_height()
        mouse = (
            mouse[0] - self.pos[0] - self.screen.get_width() * self.screenPos[0],
            mouse[1] - self.pos[1] - self.screen.get_height() * self.screenPos[1],
        )
        if 0 <= mouse[0] <= width and 0 <= mouse[1] <= height:
            self.func()

def makeTextButton(size: tuple, pos: tuple, color: tuple, text: str, textColor: tuple, screenPos: tuple, func):
    surface = pygame.Surface(size)
    surface.fill(color)
    textSurf = font.render(text, True, textColor)
    surface.blit(textSurf, (size[0] / 2 - textSurf.get_width() / 2, size[1] / 2 - textSurf.get_height() / 2))
    Button(surface, pos, screenPos, func)

background = (255, 255, 255)

def update(dt:float, screen, pressed):
    slamMain.update(dt, screen, pressed)

def draw(screen: pygame.Surface):
    screen.blit(backgroundImage, (0, 0))
    slamMain.draw(screen)
    for draw in buttonDraws:
        draw(screen)

def mainLoop():
    global screen, background, buttonUpdates
    # Game loop.
    dt = 1 / fps
    pressed = []
    while True:
        screen.fill(background)
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                # w, h = event.size
                # if w < 400:
                #     w = 400
                # if h < 300:
                #     h = 300
                screen = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF | RESIZABLE)
            elif event.type == MOUSEBUTTONDOWN:
                for func in buttonUpdates:
                    func()
            elif event.type == pygame.KEYDOWN:
                pressed.append(event.key)
            elif event.type == pygame.KEYUP:
                pressed.remove(event.key)
        update(dt, screen, pressed)

        draw(screen)
        dt = fpsClock.tick(fps)

        pygame.display.flip()
        fpsClock.tick(fps)

mainLoop()
