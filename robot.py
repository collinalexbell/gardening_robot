import os, sys, math, queue
from PIL import Image
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame
from pygame.locals import *
from gardenbotnn import Garden_Bot_NN
from garden import Garden

def load_pygame_img(file_name):
    """Load img is a function that uses PIL to load a pygame image"""
    img = Image.open(file_name)
    mode = img.mode
    size = img.size
    data = img.tostring()
    #pygame_img = pygame.image.fromstring(data, size, mode) #Load the sheet
    pygame_img = pygame.image.load(file_name)
    return pygame_img


class Robot:
    def __init__(self, x, y, world):
        self.world = world
        robot_sprites = load_pygame_img('robot.png')
        self.sprites = self.make_sprites(robot_sprites)
        self.x = x
        self.y = y
        self.blit_queue = queue.Queue()
        self.sprite = self.sprites['right_s']
        self.direction = 'right'
        self.nnet = Garden_Bot_NN()

    def make_sprites(self, robot_sprites):
        
        sprites = {}
        sprites['down_s'] = robot_sprites.subsurface(pygame.Rect(0,0,35,55))
        sprites['down_l'] = robot_sprites.subsurface(pygame.Rect(38,0,35,55))
        sprites['down_r'] = robot_sprites.subsurface(pygame.Rect(79,0,35,55))
        sprites['left_s'] = robot_sprites.subsurface(pygame.Rect(0,56,35,55))
        sprites['left_l'] = robot_sprites.subsurface(pygame.Rect(38,56,35,55))
        sprites['left_r'] = robot_sprites.subsurface(pygame.Rect(79,56,35,55))
        sprites['right_s'] = robot_sprites.subsurface(pygame.Rect(0,111,35,55))
        sprites['right_l'] = robot_sprites.subsurface(pygame.Rect(38,111,35,55))
        sprites['right_r'] = robot_sprites.subsurface(pygame.Rect(79,111,35,55))
        sprites['up_s'] = robot_sprites.subsurface(pygame.Rect(3,166,35,55))
        sprites['up_l'] = robot_sprites.subsurface(pygame.Rect(40,166,35,55))
        sprites['up_r'] = robot_sprites.subsurface(pygame.Rect(82,166,35,55))


        self.up_steps = [(35,0),(75,0)]
        self.left_standing = (0, 60)
        self.left_steps = [(35,60),(75,60)]
        self.right_standing = (0, 115)
        self.right_steps = [(35,115),(75,115)]
        self.up_standing = (0, 165)
        self.up_steps = [(35,165),(75,165)]

        return sprites

    def move(self):
        step_size = 2
        if self.direction == 'up':
            unit = (0, -1)
        if self.direction == 'left':
            unit = (-1,0)
        if self.direction == 'right':
            unit = (1, 0)
        if self.direction == 'down':
            unit = (0, 1)

        print("{},{}".format(unit[0], unit[1]))
        if self.blit_queue.empty():
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_l'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_l'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_l'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_l'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_l'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_l'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_r'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_r'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_r'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_r'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_r'})
            self.blit_queue.put({'d_pos':(unit[0]*step_size, unit[1]*step_size), 'sprite':self.direction + '_r'})

    def turn(self, direction):
        self.direction = direction
        self.blit_queue.put({'d_pos':(0,0), 'sprite':self.direction + '_s'})



        

    def act(self):
        if(not self.blit_queue.empty()):
            nex = self.blit_queue.get()
            #print('{},{}'.format(self.x, self.y))
            self.x += nex['d_pos'][0]
            self.y += nex['d_pos'][1]
            self.sprite = self.sprites[nex['sprite']]
            return True
        return False

    def on_garden(self, collisions):
        gardens = self.world.get_gardens
        for collision in collisions:
            if (collision[0] == self and type(collision[1])) == Garden or (collision[1] == self and type(collision[0]) == Garden):
                return 1

        return 0

    def get_unit_direction(self, direction):
        if direction == 'front':
            if self.direction == 'up':
                unit_direction = (0,-1)
            if self.direction == 'left':
                unit_direction = (-1,0)
            if self.direction == 'right':
                unit_direction = (1, 0)
            if self.direction == 'down':
                unit_direction = (0,1)

        if direction == 'left':
            if self.direction == 'up':
                unit_direction = (-1,0)
            if self.direction == 'left':
                unit_direction = (0,1)
            if self.direction == 'right':
                unit_direction = (0, -1)
            if self.direction == 'down':
                unit_direction = (1, 0)

        if direction == 'right':
            if self.direction == 'up':
                unit_direction = (1,0)
            if self.direction == 'left':
                unit_direction = (0,-1)
            if self.direction == 'right':
                unit_direction = (0, 1)
            if self.direction == 'down':
                unit_direction = (-1, 0)
        return unit_direction



    def sense_garden(self, direction):
        unit_direction = self.get_unit_direction(direction)
        gardens = self.world.get_gardens()
        sum = 0
        line_of_sight = 400
        for garden in gardens:
            x_distance = (garden.x-self.x) * unit_direction[0]
            if x_distance > 0 and x_distance < line_of_sight:
                sum +=  (math.pow(1 - x_distance/line_of_sight, 2))
            y_distance = (garden.y-self.y) * unit_direction[1]
            if y_distance > 0 and y_distance < line_of_sight:
                sum +=  (math.pow(1 - y_distance/line_of_sight, 2))
        return sum

    def sense_customers(self, direction):
        unit_direction = self.get_unit_direction(direction)
        customers = self.world.get_customers()
        sum = 0
        line_of_sight = 400
        for customer in customers:
            x_distance = (customer.x-self.x) * unit_direction[0]
            if x_distance > 0:
                sum +=  (math.pow(1 - x_distance/line_of_sight, 2))
            y_distance = (customer.y-self.y) * unit_direction[1]
            if y_distance > 0:
                sum +=  (math.pow(1 - y_distance/line_of_sight, 2))
        return sum


