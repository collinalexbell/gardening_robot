from PIL import Image
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame
from pygame.locals import *
from random import randint
import json

def load_pygame_img(file_name):
    """Load img is a function that uses PIL to load a pygame image"""
    img = Image.open(file_name)
    mode = img.mode
    size = img.size
    data = img.tostring()
    #pygame_img = pygame.image.fromstring(data, size, mode) #Load the sheet
    pygame_img = pygame.image.load(file_name)
    return pygame_img

class Garden:
    def __init__(self,x,y,world, config_file = False, config = False):
        self.world = world
        self.sprite = load_pygame_img('orange_garden.png')
        self.x = x
        self.y = y
        self.hp = 10
        self.capacity = 1
        self.used = 0
        if config_file:
            self._load_config_from_json(config_file)
        if config:
            self._load_config(config)


    def remove(self):
        self.world.gardens.remove(self)
        new_x = randint(0, self.world.screenx-100)
        new_y = randint(0, self.world.screeny-100)
        self.world.add_garden(new_x, new_y)

    def harvest(self):
        print('harvested')
        if self.used < self.capacity:
            self.used += 1
            return True
        else:
            return False

    def __del__(self):
        pass

    def _load_config(self, config):
        if type(config) != dict:
            raise TypeError('config must be a dict')
        else:
            if 'garden' in config:
                if type(config['garden']) != dict:
                    raise Exception('garden in config must be a dict')
                for key, item in config['garden'].items():
                   exec("self.%s = %s" % (key,item))

    def _load_config_from_json(self, file_name):
        with open(file_name) as f:
            json_data = f.read()
            data = json.loads(json_data)
        self._load_config(data)

    def is_fully_harvested(self):
        print('{},{}'.format(self.used, self.capacity))
        if self.used >= self.capacity:
            return True
        else:
            return False
