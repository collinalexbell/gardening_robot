import os, sys, math, queue
from PIL import Image
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame
from pygame.locals import *
from robot import Robot

pygame.font.init()



SCREEN_X = 1080
SCREEN_Y = 720

SPRT_RECT_X=0  
SPRT_RECT_Y=0
#This is where the sprite is found on the sheet

LEN_SPRT_X=100
LEN_SPRT_Y=100
#This is the length of the sprite




                    

def one_robot_three_gardens_and_one_customer():
    world = World()
    world.add_robot(0,0)
    world.add_garden(200, 200)
    world.add_garden(300, 300)
    world.add_garden(400, 400)
    world.add_customer(200, 400)
    world.run()

def detect_collision(objects):
    rv = []
    for i in range(len(objects)-1):
        for j in range(i+1,len(objects)):
            obj1_rect = Rect(objects[i].x, objects[i].y, objects[i].sprite.get_width(), objects[i].sprite.get_height())
            obj2_rect = Rect(objects[j].x, objects[j].y, objects[j].sprite.get_width(), objects[j].sprite.get_height())
            if obj1_rect.colliderect(obj2_rect):
                rv.append((objects[i], objects[j]))
    if len(rv)>0:
        print(rv[0])
    return rv


class Customer:
    def __init__(self,x,y):
        self.sprite = load_pygame_img('consumer.png')
        self.x = x
        self.y = y

class Garden:
    def __init__(self,x,y):
        self.sprite = load_pygame_img('orange_garden.png')
        self.x = x
        self.y = y
        self.hp = 10

class World:
    def __init__(self):
        pygame.init()
        self.robots = [] 
        self.gardens = []
        self.customers = []
        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Create the screen
        self.objects = []

        self.backdrop = pygame.Rect(0, 0, SCREEN_X, SCREEN_Y) #Create the whole screen so you can draw on it
        self.clock = pygame.time.Clock()

        pygame.event.set_allowed([QUIT, KEYDOWN])

    def run(self):

        self.running = True
        while self.running:
            self.clock.tick(60)
            self.screen.fill((0,0,0))
            self.handle_events()
            for garden in (self.gardens + self.customers):
                self.screen.blit(garden.sprite, (garden.x, garden.y), self.backdrop)
            for robot in self.robots:
                robot.act()
                self.screen.blit(robot.sprite, (robot.x, robot.y), self.backdrop)
                self.print_debug()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                   self.running = False 
     
                # handle user input
                elif event.type == pygame.KEYDOWN:
                    print('keydown')
                    # if the user presses escape, quit the event loop.
                    if(len(self.robots) > 0):
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        if event.key == pygame.K_w:
                            self.robots[0].turn('up')
                        if event.key == pygame.K_s:
                            self.robots[0].turn('down')
                        if event.key == pygame.K_a:
                            self.robots[0].turn('left')
                        if event.key == pygame.K_d:
                            self.robots[0].turn('right')
                            print('right')
                        if event.key == pygame.K_SPACE:
                            self.robots[0].move()

    def add_garden(self, x, y):
        new_garden = Garden(x,y)
        self.gardens.append(new_garden)
        self.objects.append(new_garden)

    def get_gardens(self):
        return self.gardens

    def add_customer(self, x, y):
        new_customer = Customer(x, y)
        self.customers.append(new_customer)
        self.objects.append(new_customer)

    def get_customers(self):
        return self.customers

    def add_robot(self, x, y):
        new_robot = Robot(x,y,self)
        self.robots.append(new_robot)
        self.objects.append(new_robot)

    def print_debug(self):
        font =  pygame.font.Font(None, 16)
        garden_front = font.render('garden_sensor front: {}'.format(self.robots[0].sense_garden('front')), 0, pygame.Color(255,255,255))
        garden_left = font.render('garden_sensor left: {}'.format(self.robots[0].sense_garden('left')), 0, pygame.Color(255,255,255))
        garden_right = font.render('garden_sensor right: {}'.format(self.robots[0].sense_garden('right')), 0, pygame.Color(255,255,255))
        customer_front = font.render('customer_sensor front: {}'.format(self.robots[0].sense_customers('front')), 0, pygame.Color(255,255,255))
        customer_left = font.render('customer_sensor left: {}'.format(self.robots[0].sense_customers('left')), 0, pygame.Color(255,255,255))
        customer_right = font.render('customer_sensor right: {}'.format(self.robots[0].sense_customers('right')), 0, pygame.Color(255,255,255))
        collisions = font.render('Num of collisions: {}'.format(len(detect_collision(self.objects))), 0, pygame.Color(255, 255, 255))
        self.screen.blit(garden_front, (800, 620))
        self.screen.blit(garden_left, (800, 640))
        self.screen.blit(garden_right, (800, 660))
        self.screen.blit(customer_front, (800, 520))
        self.screen.blit(customer_left, (800, 540))
        self.screen.blit(customer_right, (800, 560))
        self.screen.blit(collisions, (800, 680))


        


if __name__ == '__main__':
    one_robot_three_gardens_and_one_customer()

