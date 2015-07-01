import os, sys, math, queue
import random
from PIL import Image
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame
from pygame.locals import *
from robot import Robot
from garden import Garden
from customer import Customer
import collections
import copy
import time
import threading


pygame.font.init()

def load_pygame_img(file_name):
    """Load img is a function that uses PIL to load a pygame image"""
    img = Image.open(file_name)
    mode = img.mode
    size = img.size
    data = img.tostring()
    #pygame_img = pygame.image.fromstring(data, size, mode) #Load the sheet
    pygame_img = pygame.image.load(file_name)
    return pygame_img

SCREEN_X = 1080
SCREEN_Y = 720

SPRT_RECT_X=0
SPRT_RECT_Y=0
#This is where the sprite is found on the sheet

LEN_SPRT_X=100
LEN_SPRT_Y=100
#This is the length of the sprite


def make_background():
    backdrop = pygame.Rect(0, 0, SCREEN_X, SCREEN_Y) #Create the whole screen so you can draw on it
    bk_image = pygame.Surface([SCREEN_X,SCREEN_Y])
    bk_image = bk_image.convert_alpha()
    img = load_pygame_img('floor_texture_small.jpg')
    for i in range(math.ceil(SCREEN_X/img.get_width())):
        for j in range(math.ceil(SCREEN_Y/img.get_height())):
            x = i * img.get_width()
            y = j * img.get_height()
            bk_image.blit(img, (x, y), backdrop)
    return bk_image



def ten_robots_three_gardens_and_one_customer():
    world = World()
    for i in range(30):
        world.add_robot(0,0)
    world.add_garden(400, 200)
    world.add_garden(400, 600)
    world.add_garden(100, 400)
    world.add_customer(800, 600)
    world.add_customer(200,200)
    world.add_customer(800, 100)
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
        #print(rv[0])
        pass
    return rv



class World:
    def __init__(self):
        pygame.init()
        self.robots = []
        self.screenx = SCREEN_X
        self.screeny = SCREEN_Y
        self.gardens = []
        self.customers = []
        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Create the screen
        self.objects = []
        self.background = make_background()

        self.backdrop = pygame.Rect(0, 0, SCREEN_X, SCREEN_Y) #Create the whole screen so you can draw on it
        self.clock = pygame.time.Clock()

        pygame.event.set_allowed([QUIT, KEYDOWN])

    def run(self):

        self.running = True
        self.time = time.time()
        while self.running:
            self.screen.blit(self.background, (0,0), self.backdrop)
            self.handle_events()
            processes = []
            for garden in (self.gardens + self.customers):
                self.screen.blit(garden.sprite, (garden.x, garden.y), self.backdrop)
            #Start threads to make the robots think and act
            for robot in self.robots:
                p = threading.Thread(target = robot.think_and_act)
                processes.append(p)
                p.start()

            #Wait until all threads have finished before...
            for process in processes:
                process.join()

            #Sensing gardens and whatnot
            self.detect_and_act_on_robot_garden_collisions()
            self.detect_and_act_on_robot_customer_collisions()

            for robot in self.robots[0:10]:
                self.screen.blit(robot.sprite, (robot.x, robot.y), self.backdrop)
            pygame.display.flip()
            if time.time() - self.time >= 20:
                self.next_gen(30)
                self.time = time.time()


    def handle_events(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                   self.running = False

                # handle user input
                elif event.type == pygame.KEYDOWN:
                    # if the user presses escape, quit the event loop.
                    if(len(self.robots) > 0):
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        if event.key == pygame.K_w:
                            self.robots[0].turn('up')
                        if event.key == pygame.K_s:
                            self.robots[0].turn('down')
                        if event.key == pygame.K_a:
                            self.robots[0].turn(10)
                        if event.key == pygame.K_d:
                            self.robots[0].turn(-10)
                        if event.key == pygame.K_m:
                            self.next_gen(30)
                        if event.key == pygame.K_SPACE:
                            self.robots[0].move(10)

    def add_garden(self, x, y):
        new_garden = Garden(x,y, self, config_file = 'config.json')
        self.gardens.append(new_garden)

    def get_gardens(self):
        return self.gardens

    def add_customer(self, x, y):
        new_customer = Customer(x, y)
        self.customers.append(new_customer)

    def get_customers(self):
        return self.customers

    def get_robots(self):
        return self.robots

    def add_robot(self, x, y, robot = 0):
        if robot:
            new_robot = robot
        else:
            new_robot = Robot(x,y,self)
        self.robots.append(new_robot)

    def next_gen(self, percentage):
        scored_robots = {}
        for robot in self.robots:
            score = robot.get_fitness()
            if score in scored_robots.keys():
                scored_robots[score].append(robot)
            else:
                scored_robots[score] = [robot]

        winners = []

        #Start with highest scoring robot
        class BreakIt(Exception): pass
        try:
            for score_set in reversed(sorted(scored_robots)):
                for robot in scored_robots[score_set]:
                    if len(winners) < len(self.robots) * percentage/100:
                        winners.append(robot)
                    else:
                        raise BreakIt
        except BreakIt:
            pass

        len_bots = len(self.robots)

        self.robots = []

        for robot in winners:
            self.robots.append(robot.age())

        for i in range(len_bots-len(winners)):
            #Select robot randomly
            selected = random.choice(winners)
            self.robots.append(Robot(0,0,self, selected))

        for garden in self.gardens:
            garden.remove()




    def detect_and_act_on_robot_garden_collisions(self):
        remove_these_gardens = []
        for robot in self.robots:
            for garden in self.gardens:
                robot_rect = Rect(robot.x, robot.y, robot.sprite.get_width(), robot.sprite.get_height())
                garden_rect = Rect(garden.x, garden.y, garden.sprite.get_width(), garden.sprite.get_height())
                if robot_rect.colliderect(garden_rect):
                    if robot.get_last_garden() != garden:
                        if robot.collect_garden(garden):
                            garden.harvest()
                    if garden.is_fully_harvested() and garden not in remove_these_gardens:
                        remove_these_gardens.append(garden)

        for garden in remove_these_gardens:
            garden.remove()

    def detect_and_act_on_robot_customer_collisions(self):
        for robot in self.robots:
            for customer in self.customers:
                robot_rect = Rect(robot.x, robot.y, robot.sprite.get_width(), robot.sprite.get_height())
                customer_rect = Rect(customer.x, customer.y, customer.sprite.get_width(), customer.sprite.get_height())
                if robot_rect.colliderect(customer_rect):
                    robot.sell_fruit()













if __name__ == '__main__':
    ten_robots_three_gardens_and_one_customer()

