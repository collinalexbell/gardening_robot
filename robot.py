import os
import sys
import math
import queue
from PIL import Image
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame
from pygame.locals import *
from gardenbotnn import Garden_Bot_NN
from gardenbotnn import mutate_dna
from garden import Garden
from customer import Customer
from graphics_geometor import Graphics_Geometor

def load_pygame_img(file_name):
    """Load img is a function that uses PIL to load a pygame image"""

    img = Image.open(file_name)
    mode = img.mode
    size = img.size
    data = img.tostring()
    #pygame_img = pygame.image.fromstring(data, size, mode) #Load the sheet
    pygame_img = pygame.image.load(file_name)
    return pygame_img

class Robot_Sprite:
    """A singleton sprite loader that caches the robot sprites at various angles"""
    class _Robot_Sprite:
        def __init__(self, file_path):
            self.sprite = load_pygame_img('ball_bot.png')
            self.sprites = self._make_sprites()

        def _make_sprites(self):
            sprites = []
            for i in range(360):
                sprites.append(pygame.transform.rotate(self.sprite, i))
            return sprites

        def get_sprite_at_angle(self, angle):
            #Get any angle to the nearest degree
            return self.sprites[int(round(angle%360))]


    instance = None

    def __init__(self, file_path):
        #Load a single sprite
        if not Robot_Sprite.instance:
            Robot_Sprite.instance = Robot_Sprite._Robot_Sprite(file_path)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class Robot:
    def __init__(self, x, y, world, robot = False):
        self.world = world
        self.geometor = Graphics_Geometor()
        self.sprite_object = Robot_Sprite('ball_bot.png')
        self.sprite = self.sprite_object.get_sprite_at_angle(0)
        self.x = x
        self.y = y
        self.real_x = float(x)
        self.real_y = float(y)
        self.blit_queue = queue.Queue()
        self.direction_in_deg = 0
        if robot:
            self.nnet = Garden_Bot_NN(mutate_dna(robot.nnet.encode_dna()))
        self.nnet = Garden_Bot_NN()
        self.num_of_fruit = 0
        self.num_of_fruit_ever = 0
        self.money = 0
        self.CARRYING_CAPACITY = 2
        self.unique_locations = set()
        self.deg_eye_sep = 40
        self.deg_eye_focal = 60
        self._make_eye_angles()


    def load_dna(self, dna):
        self.nnet = Garden_Bot_NN(dna)


    def move(self, step_length):
        x_step =  math.cos(math.radians(self.direction_in_deg))  * step_length
        self.real_x += x_step

#       Assuming that angles are on a standard x-y plane not a graphics plane
        y_step = math.sin(math.radians(self.direction_in_deg)) * step_length
        self.real_y -= y_step
        self.x=int(self.real_x)%self.world.screenx
        self.y=int(self.real_y)%self.world.screeny

    def turn(self, deg):
        self.direction_in_deg += deg
        self.direction_in_deg = self.direction_in_deg % 360
        new_deg = self.direction_in_deg
        self.sprite = self.sprite_object.get_sprite_at_angle(new_deg)
        self._make_eye_angles()


    def on_customer(self, collisions):
        for collision in collisions:
            if collision[0] == self and type(collision[1]) == Customer and self.num_of_fruit > 0:
                self.sell_fruit(collision[1])
            if collision[0] == self and type(collision[1]) == Customer and self.num_of_fruit > 0:
                self.sell_fruit(collision[0])
        return self.money

    def _make_eye_angles(self):
        self.eye_angles = {}
        dir = self.direction_in_deg
        right_eye_min = dir - (self.deg_eye_sep/2) - (self.deg_eye_focal/2)
        right_eye_max = dir - (self.deg_eye_sep/2) + (self.deg_eye_focal/2)

        left_eye_min = dir + (self.deg_eye_sep/2) - (self.deg_eye_focal/2)
        left_eye_max = dir + (self.deg_eye_sep/2) + (self.deg_eye_focal/2)

        self.eye_angles['left'] = (left_eye_min%360, left_eye_max%360)
        self.eye_angles['right'] = (right_eye_min%360, right_eye_max%360)

    def _sense_objects(self, objs, direction):
        sum = 0
        line_of_sight = 400
        self.geometor.set_origin((self.x, self.y))
        for obj in objs:
            robot_eye_angle = self.eye_angles[direction]
            #print(robot_eye_angle)
            #print('{}, {}'.format(obj.x, obj.y))
            if self.geometor.is_in_angle((obj.x, obj.y), robot_eye_angle):
                robot_point = (self.x, self.y)
                obj_point = (obj.x, obj.y)
                distance = self.geometor.get_distance(robot_point, obj_point)
                sum +=  (math.pow(1 - distance/line_of_sight, 2))
        return sum


    def sense_gardens(self, direction):
        gardens = self.world.get_gardens()
        return self._sense_objects(gardens,direction)


    def sense_customers(self, direction):
        customers = self.world.get_customers()
        return self._sense_objects(customers, direction)


    def collect_garden(self):
        self.num_of_fruit += 1
        self.num_of_fruit_ever += 1


    def sell_fruit(self):
        self.money = self.num_of_fruit
        self.num_of_fruit = 0


    def sense_fullness(self):
        return self.num_of_fruit/self.CARRYING_CAPACITY


    def think_and_act(self):
       self.process_inputs()
       self.nnet.run_net()
       self.process_outputs()


    def process_inputs(self):
        #Clock needs to fire every tick. Set the stimulus to threshold + 1
        self.nnet.neurons['clock']['stimulus'] = self.nnet.neurons['clock']['threshold'] + 1

        #Garden Neurons
        self.nnet.neurons['garden_left']['stimulus'] += self.sense_gardens('left')
        self.nnet.neurons['garden_right']['stimulus'] += self.sense_gardens('right')

        #Customer Neurons
        self.nnet.neurons['customer_left']['stimulus'] += self.sense_customers('left')
        self.nnet.neurons['customer_right']['stimulus'] += self.sense_customers('right')

        #Fruit Level
        self.nnet.neurons['food_level']['stimulus'] += self.sense_fullness()


    def process_outputs(self):
        left_turn = self.nnet.neurons['left_turn']['output']
        right_turn = self.nnet.neurons['right_turn']['output']
        tail_motor = self.nnet.neurons['tail_motor']['output']

        #IF we didnt turn and motor is activated

        turn_xor = left_turn ^ right_turn

        if tail_motor and not turn_xor:
            self.move(10)

        if left_turn and turn_xor:
            self.turn(10)
        if right_turn and turn_xor:
            self.turn(10)


    def add_to_unique_locations(self, x, y):
        self.unique_locations.add((x,y))

    def num_of_unique_locations(self):
        return len(self.unique_locations)


    def get_fitness(self):
        return  self.num_of_fruit_ever + self.money









