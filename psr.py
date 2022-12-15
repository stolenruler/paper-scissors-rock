import pygame as pg
from random import randint, uniform
import math

#generate object which is coloured as paper, scissors, rock
class Node:
    def __init__(self):
        self.x = randint(0,WIDTH-30)
        self.y = randint(0,HEIGHT-50)
        self.rect = pg.Rect(self.x,self.y,30,50)
        self.xspeed = randint(-3,3)
        self.yspeed = randint(-3,3)
    
    def draw(self, nodetype):
        #depending on the 'type', sets the photo as paper, scissors or rock
        if nodetype == 0:
            image = './images/paper.png'
        elif nodetype == 1:
            image = './images/scissors.png'
        else:
            image = './images/rock.png'
        
        image = pg.image.load(image).convert_alpha()
        image = pg.transform.scale(image, (30, 50))
        screen.blit(image, (self.x,self.y))

    def collision(self, nodetype):
        #if paper collides with scissors, it becomes a scissor
        if nodetype == 0:
            for scissor in s:
                if pg.Rect.colliderect(scissor.rect, self.rect):
                    p.remove(self)
                    s.append(self)
                    self.draw(1)
                    break
        
        #if scissors collides with rock, it becomes a rock
        if nodetype == 1:
            for rock in r:
                if pg.Rect.colliderect(rock.rect, self.rect):
                    s.remove(self)
                    r.append(self)
                    self.draw(2)
                    break
        
        #if rock collides with paper, it becomes a paper
        if nodetype == 2:
            for paper in p:
                if pg.Rect.colliderect(paper.rect, self.rect):
                    r.remove(self)
                    p.append(self)
                    self.draw(0)
                    break
    
    def move(self, speed_mod):
        #moves the object based on some given speed
        self.x = min(self.x+self.xspeed,WIDTH-30)
        self.y = min(self.y+self.yspeed,HEIGHT-50)
        #updates the 'hitbox' of the object to be where it moved
        self.rect = pg.Rect(self.x,self.y,30,50)

        #if the object is outside of the box, then change the speed so that 'bounces' towards the center-ish
        if self.x >= WIDTH-30:
            self.xspeed = randint(-3,1)*speed_mod
        elif self.x <= 0:
            self.xspeed = randint(1,3)*speed_mod
        if self.y >= HEIGHT-50:
            self.yspeed = randint(-3,1)*speed_mod
        elif self.y <= 0:
            self.yspeed = randint(1,3)*speed_mod
        if self.xspeed == 0:
            self.xspeed = randint(-3,3)*speed_mod
        if self.yspeed == 0:
            self.yspeed = randint(-3,3)*speed_mod

#now, create a object for the button, which we use for the 'speed modification' buttons
class Button:
    def __init__(self):
        pass

    def draw(self, buttontype):
        #draws the button for the pause, play, fast forward, and rewind buttons
        if buttontype == 0: 
            #select the image 
            image = './images/fastforward.png'
            #defines where to put the image
            self.x = 510
            self.y = 510
            #loads, displays, and makes a 'hitbox' for the image
            image = pg.image.load(image).convert_alpha()
            screen.blit(image, (self.x,self.y))
            self.surface = pg.Surface((self.x,self.y))
            self.rect = pg.Rect(self.x, self.y, 61, 40)
        elif buttontype == 1:
            #follows same logic as above
            image = './images/rewind.png'
            image = pg.image.load(image).convert_alpha()
            self.x = 310
            self.y = 510
            screen.blit(image, (self.x,self.y))
            self.surface = pg.Surface((self.x,self.y))
            self.rect = pg.Rect(self.x, self.y, 61, 40)
        else:
            #if moving, display pause. if paused, display play button
            if speed_mod == 0:
                image = './images/play.png'
            else:
                image = './images/pause.png'
            
            image = pg.image.load(image).convert_alpha()
            self.x = 420
            self.y = 510
            screen.blit(image, (self.x,self.y))
            self.surface = pg.Surface((self.x,self.y))
            self.rect = pg.Rect(self.x, self.y, 61, 40)

    #defines what happens when the mouse is clicked
    def click(self, speed_mod, buttontype):
        #gets the mouse position, and checks if the mouse has been clicked
        x, y = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            #if clicked, see if we click on the button
            if self.rect.collidepoint(x, y):
                #if we clicked on the button, see what the button type is, and adjust the speed modifier based on that
                if buttontype == 0:
                    speed_mod *= 1.5
                elif buttontype == 1:
                    speed_mod *= 1/1.5
                else:
                    if speed_mod == 0:
                        speed_mod = 1
                    else:
                        speed_mod = 0
            
            #updates the speed of all the objects

            for i in p:
                i.xspeed *=speed_mod
                i.yspeed *=speed_mod
            for i in s:
                i.xspeed *=speed_mod
                i.yspeed *=speed_mod
            for i in r:
                i.xspeed *=speed_mod
                i.yspeed *=speed_mod
            
            return speed_mod

speed_mod = 1

#initialize pygame
pg.init()

#initialize game and screen parameters
fps = 24
timer = pg.time.Clock()
font = pg.font.Font('freesansbold.ttf',28)
WIDTH = 960
HEIGHT = 600
pg.display.set_caption('Paper Scissors Rock: The Game')
screen = pg.display.set_mode([WIDTH, HEIGHT])

#load images and define how many of each to have
psr_totals = [10,10,10]

#set background and load images
bg = pg.image.load('./images/grass.jpg')
bg = pg.transform.scale(bg, (WIDTH, HEIGHT))
scoreboard = pg.image.load('./images/scoreboard.png')
scoreboard = pg.transform.scale(scoreboard, (297, 64))
banner = pg.image.load('./images/banner.png')
banner = pg.transform.scale(banner, (400, 60))

p = []
s = []
r = []
#makes 10 paper, 10 scissors, and 10 rocks, and appends them to a list (which contains all the paper, scissors and rocks)
for i in range(psr_totals[0]):
    Paper = Node()
    p.append(Paper)
for i in range(psr_totals[1]):
    Scissors = Node()
    s.append(Scissors)
for i in range(psr_totals[2]):
    Rock = Node()
    r.append(Rock)

#initializes the buttons
fastforward = Button()
rewind = Button()
pauseplay = Button()

run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    screen.blit(bg, (0,0))
    screen.blit(banner, (280, 500))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            speed_mod = fastforward.click(speed_mod, 0)
            speed_mod = rewind.click(speed_mod, 1)
            speed_mod = pauseplay.click(speed_mod, 2)

        
    for i in p:
        i.move(speed_mod)
        i.draw(0)
        i.collision(0)
    for i in s:
        i.move(speed_mod)
        i.draw(1)
        i.collision(1)
    for i in r:
        i.move(speed_mod)
        i.draw(2)
        i.collision(2)
    
    fastforward.draw(0)
    rewind.draw(1)
    pauseplay.draw(2)

    pcount = len(p)
    scount = len(s)
    rcount = len(r)
    paper_text = font.render(f'{pcount}', True, 'black')
    scissors_text = font.render(f'{scount}', True, 'black')
    rock_text = font.render(f'{rcount}', True, 'black')
    speed_text = font.render(f'{speed_mod}', True, 'black')
    screen.blit(scoreboard, (352,50))
    screen.blit(paper_text, (382,60))
    screen.blit(scissors_text, (484,60))
    screen.blit(rock_text, (587,60))
    screen.blit(speed_text, (630, 510))

    if pcount == 30:
        print("Paper Won!")
        run =  False
    if scount == 30:
        print("Scissors Won!")
        run = False
    if rcount == 30:
        print("Rock Won!")
        run = False
    
    pg.display.flip()
pg.quit()
