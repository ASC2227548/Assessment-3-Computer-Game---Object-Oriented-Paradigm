import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

#Screen size when you play
screen_width = 640
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Assessment 3: Jumpy Ship ')

#Load images into game
bg = pygame.image.load('assets/bg.png')
ground = pygame.image.load('assets/ground.jpg')

#game variables
#ground_move = 0
#ground_speed = 4

screen.blit(ground, (0,640))
#if ship collides with ground then it dies and game restarts

bg0x = 0
bg1x = -screen_width
def rolling_BG():
    global bg0x, bg1x, screen_width
    screen.blit(bg, (bg0x,0))
    screen.blit(bg, (bg1x,0))
    bg0x -= 1
    bg1x -= 1
    if bg0x < -screen_width:
        bg0x = screen_width
    if bg1x < -screen_width:
        bg1x = screen_width


#Game loop
run = True
while run:

    clock.tick(fps)

    #in the game loop the background stays moving
    rolling_BG()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()