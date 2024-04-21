import pygame
import random
from pygame import mixer
from random import randrange
from pygame.locals import *

pygame.init()
mixer.init()

clock = pygame.time.Clock()
fps = 60

#load music and sounds
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1, 0.0)
explosion_fx = pygame.mixer.Sound('assets/explosion.wav')
explosion_fx.set_volume(0.5)
point_fx = pygame.mixer.Sound('assets/point.wav')
point_fx.set_volume(0.7)


#Screen size when you play
screen_width = 640
screen_height = 640

#set the games name when you play
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Assessment 3: Jumpy Ship ')

#Load images into game
bg = pygame.image.load('assets/bg.png')
ground = pygame.image.load('assets/ground.jpg')
button_img = pygame.image.load('assets/BTN.png')

#font
font = pygame.font.SysFont('Bauhaus 93', 55)
font_1 = pygame.font.SysFont('Bauhaus 93', 20)

#colour
white = (255, 255, 255)

#game variables
flying = False
dead = False
rolling = True
gap = random.randint(150,220)
freq = random.randint(2500,3500)
last_danger = pygame.time.get_ticks() - freq
score = 0
past_dangers = False
explosion_sound_played = False



screen.blit(ground, (0,640))


bg0x = 0
bg1x = -screen_width

#rolling background
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

#define text
def text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))

#define what the reset should do to the variables
def reset():
    global flying, dead, score, past_dangers, last_danger
    flying = False
    dead = False
    score = 0
    past_dangers = False
    last_danger = pygame.time.get_ticks() - freq
    ship.rect.x = 100
    ship.rect.y = int(screen_height / 2)
    ship.vel = 0
    danger_group.empty()
    ship.explode_counter = 0

def sound():
    ex = explosion_fx.play()

#the player class
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
    #if player dies it will itterate through 7 explosion images to create a animation of dying
    def draw(self, screen):
        if dead == False:
            screen.blit(self.image, self.rect)
        else:
            if dead == True and self.explode_counter < 7:  # Adjusted for 7 images
                explosion_image = pygame.image.load(f'assets/ex{self.explode_counter + 1}.png')
                explosion_rect = explosion_image.get_rect(center=self.rect.center)
                screen.blit(explosion_image, explosion_rect)
                self.explode_counter += 1


    def update(self):
        if flying == True:
            #Falling (making sure it doesnt go too fast downwards)
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

#obstacles to avoid during the game
class danger(pygame.sprite.Sprite):
    def __init__(self,x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/danger1.png')
        self.rect = self.image.get_rect()

        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(gap) / 2]
        if pos == -1:
            self.rect.topleft = [x, y + int(gap) / 2]



    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()

#the restart button after you die
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action = False
        #get the mouses position
        pos = pygame.mouse.get_pos()
        #is mouse over button?
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


danger_group = pygame.sprite.Group()
ship = Spaceship(100, int(screen_height / 2))
ship_group = pygame.sprite.GroupSingle(ship)


button = Button(245, 500, button_img)



#Game loop
run = True
while run:

    clock.tick(fps)


    #in the game loop the background stays moving
    rolling_BG()



    ship.update()
    ship.draw(screen)
    danger_group.draw(screen)

    #display game over text when dead and a start screen
    if dead:
        text("Game Over", font, white, 200, 250)
    if dead == False and flying == False:
        text("JUMPY SHIP", font, white, 190, 200)
        text("Click Anywhere to Start", font_1, white, 220, 500)

    # check the score
    if len(danger_group) > 0:
        if ship_group.sprites()[0].rect.left > danger_group.sprites()[0].rect.left \
                and past_dangers == False:
                past_dangers = True
        if past_dangers == True:
            if ship_group.sprites()[0].rect.right < danger_group.sprites()[0].rect.right:
                score += 1
                point_fx.play()
                past_dangers = False

    text(str(score), font, white, 310, 10)

    if dead == False:
        danger_group.update()

    #when the player is not dead and is flying it will randomly create the height of the asteroids
    if dead == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_danger > freq:
            danger_height = random.randint(-120, 208)
            lower = danger(screen_width, int(screen_height / 2) + danger_height , -1)
            top = danger(screen_width, int(screen_height / 2) + danger_height, 1)
            danger_group.add(lower)
            danger_group.add(top)
            last_danger = time_now


    #if player dies to either dangers, top or bottom of the screen it will play the explosion sound and will change dead to true
    if pygame.sprite.groupcollide(ship_group, danger_group, False, False):
        dead = True
        flying = False
        sound()


    #when ship leaves screen:
    if ship.rect.bottom >= 640:
        sound()
        dead = True
        flying = False


        if button.draw() == True:
            reset()
    if ship.rect.top <= 0:
        sound()
        dead = True
        flying = False


        if button.draw() == True:
            reset()

    if dead == True:
        if button.draw() == True:
            reset()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and dead == False:
            flying = True

    pygame.display.update()

pygame.quit()

