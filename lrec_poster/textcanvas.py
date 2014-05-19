import pygame, sys
#from pygame.locals import *
import random

pygame.init()

width, height = 1200, 900
width, height = 2500, 1400
width, height = 2560, 1440
#screen = pygame.display.set_mode((width, height), pygame.SRCALPHA | pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

screen.fill((0,0,0))

myFont = pygame.font.Font(None, 30)
lines = open(sys.argv[1]).readlines()
random.shuffle(lines)

for line in lines:
    line = line.strip()
    line = " ".join(line.split()[:15])
    myFont = pygame.font.Font(None, random.randint(25, 100))
    semiTransparent = myFont.render(line, 1, (255,255,255))
    newSurf = pygame.Surface(myFont.size(line))
    newSurf.blit(semiTransparent,(0,0))
    newSurf.set_alpha(random.randint( 100, 220))
    newSurfRect = newSurf.get_rect()
    newSurfRect.center = (random.randint(0,width),random.randint(0,height))
    screen.blit(newSurf, newSurfRect)

    pygame.display.flip()
pygame.image.save(screen, "screenshot.png")

pygame.quit()
sys.exit()

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

