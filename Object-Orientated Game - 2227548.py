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
flying = False
dead = False
rolling = True

screen.blit(ground, (0,640))
#if ship collides with ground then it dies and game restarts

bg0x = 0
bg1x = -screen_width
def rolling_BG():
    if rolling == True:
        global bg0x, bg1x, screen_width
        screen.blit(bg, (bg0x,0))
        screen.blit(bg, (bg1x,0))
        bg0x -= 1
        bg1x -= 1
        if bg0x < -screen_width:
            bg0x = screen_width
        if bg1x < -screen_width:
            bg1x = screen_width

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('assets/ship.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.click = False
        self.explode_counter = 0
        self.dead = False
    def draw(self, screen):
        if dead == False:
            screen.blit(self.image, self.rect)
        else:
            if self.explode_counter < 7:  # Adjusted for 7 images
                explosion_image = pygame.image.load(f'assets/ex{self.explode_counter + 1}.png')
                explosion_rect = explosion_image.get_rect(center=self.rect.center)
                screen.blit(explosion_image, explosion_rect)
                self.explode_counter += 1


    def update(self):
        if flying == True:
            #Falling
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 640:
                self.rect.y += int(self.vel)

        #Jumping/Moving(and rotating to show falling and jumping)
        if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
            self.click = True
            self.vel = -10
            self.image = pygame.transform.rotate(self.original_image, 10)  # Rotate the image when jumping
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False
            self.image = self.original_image

        if self.vel > 0:
            self.image = pygame.transform.rotate(self.original_image, -10)




ship = Spaceship(100, int(screen_height / 2))




#Game loop
run = True
while run:

    clock.tick(fps)

    #in the game loop the background stays moving
    rolling_BG()


    ship.update()
    ship.draw(screen)




    #when ship leaves screen:
    if ship.rect.bottom > 640:
        dead = True
        flying = False
        rolling = False
    if ship.rect.top <0:
        dead = True
        flying = False
        rolling = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and dead == False:
            flying = True

    pygame.display.update()

pygame.quit()