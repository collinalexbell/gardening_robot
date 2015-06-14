from PIL import Image
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame
from pygame.locals import *
from random import randint

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
    def __init__(self,x,y,world):
        self.world = world
        self.sprite = load_pygame_img('orange_garden.png')
        self.x = x
        self.y = y
        self.hp = 10

    def remove(self):
        print(len(self.world.gardens))
        self.world.gardens.remove(self)
        self.world.objects.remove(self)
        print(len(self.world.gardens))
        new_x = randint(0, self.world.screenx)
        new_y = randint(0, self.world.screeny)
        self.world.add_garden(new_x, new_y)
        print(len(self.world.gardens))

    def __del__(self):
        print('Garden was harvested')
        

