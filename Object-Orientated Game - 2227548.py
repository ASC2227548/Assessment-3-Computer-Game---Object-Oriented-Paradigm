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
ground_move = 0
ground_speed = 4

bg0x = 545
bg1x = -screen_width
def rolling_ground():
    global bg0x, bg1x, screen_width
    screen.blit(ground, (bg0x,545))
    screen.blit(ground, (bg1x,545))
    bg0x += 1
    bg1x += 1
    if bg0x > screen_width:
        bg0x = -screen_width
    if bg1x > screen_width:
        bg1x = -screen_width


#Game loop
run = True
while run:

    clock.tick(fps)

    #Draw the backgound
    screen.blit(bg, (0,0))

    #draw and move the ground
    rolling_ground()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()