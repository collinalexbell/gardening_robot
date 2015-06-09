import os, sys, math, queue
from PIL import Image
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame
from pygame.locals import *
from gardenbotnn import Garden_Bot_NN

pygame.font.init()



SCREEN_X = 1080
SCREEN_Y = 720

SPRT_RECT_X=0  
SPRT_RECT_Y=0
#This is where the sprite is found on the sheet

LEN_SPRT_X=100
LEN_SPRT_Y=100
#This is the length of the sprite

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
        for collision in collisions:
            if collision[0] == self or collision[1] == self:
                return 1
            else:
                return 0

    def sense_customers(self, direction):
        customers = 0

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
        for customer in customers:
            x_distance = (customer.x-self.x) * unit_direction[0]
            if x_distance > 0:
                sum +=  1 - (math.pow(x_distance/50, 25))
            y_distance = (customer.y-self.y) * unit_direction[1]
            if y_distance > 0:
                sum +=  1 - (math.pow(y_distance/50, 25))
        return sum




                    

def main():
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

    def get_customer(self):
        return self.customers

    def add_robot(self, x, y):
        new_robot = Robot(x,y,self)
        self.robots.append(new_robot)
        self.objects.append(new_robot)

    def print_debug(self):
        font =  pygame.font.Font(None, 16)
        text_front = font.render('garden_sensor front: {}'.format(self.robots[0].sense_garden('front')), 0, pygame.Color(255,255,255))
        text_left = font.render('garden_sensor left: {}'.format(self.robots[0].sense_garden('left')), 0, pygame.Color(255,255,255))
        text_right = font.render('garden_sensor right: {}'.format(self.robots[0].sense_garden('right')), 0, pygame.Color(255,255,255))
        collisions = font.render('Num of collisions: {}'.format(len(detect_collision(self.objects))), 0, pygame.Color(255, 255, 255))
        self.screen.blit(text_front, (800, 620))
        self.screen.blit(text_left, (800, 640))
        self.screen.blit(text_right, (800, 660))
        self.screen.blit(collisions, (800, 680))


        


if __name__ == '__main__':
    main()

