from robot import Robot
from world import World
from robot import Robot_Sprite
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame


def test_robot_creation():
    world = World()
    robot = Robot(5, 5, world)

#   Robot exists
    assert type(robot) == Robot


def test_robot_sprite_class():
    robot_sprite = Robot_Sprite('ball_bot.png')
    robot_sprite2 = Robot_Sprite('ball_bot.png')

#   Robot_Sprite should be singleton
    if robot_sprite == robot_sprite2:
        assert False

#   Robot_Sprite should have a function to return x number of surfaces
    for i in range(360):
        sprite = robot_sprite.get_sprite_at_angle(i)
        assert type(sprite) == pygame.Surface

#   Round to the nearest degree
    sprite20 = robot_sprite.get_sprite_at_angle(20)
    assert robot_sprite.get_sprite_at_angle(20.3) == sprite20
    assert robot_sprite.get_sprite_at_angle(19.6) == sprite20

#   Get negative angles
    sprite270 = robot_sprite.get_sprite_at_angle(270)
    assert robot_sprite.get_sprite_at_angle(-90) == sprite270

#   Get angles over 360
    sprite361 = robot_sprite.get_sprite_at_angle(1)
    assert robot_sprite.get_sprite_at_angle(361) == sprite361


def test_robot_move():
    world = World()
    robot = Robot(5, 5, world)

#   Allow robot to move variable distances per tick
    robot.move(1)

    assert robot.real_x == 6.0
    assert robot.real_y == 5.0

    robot.direction_in_deg = -90
    robot.move(1)
    assert robot.real_x == 6.0
    print(robot.real_y)
    assert robot.real_y == 6.0

#MAKE THESE PASS, AND THE SIMULATION MAY JUST WORK
def test_sense_customers():
    pass

def test_sense_gardens():
    world = World()
    robot = Robot(0, 100, world)
    world.add_garden(50, 100)

    #Should be sensed by both eyes
    assert robot.sense_gardens('left') > 0
    assert robot.sense_gardens('right') > 0

    robot.turn(-20)
    assert robot.sense_gardens('left') > 0
    assert robot.sense_gardens('right') == 0

def test_make_eye_angles():
    world = World()
    robot = Robot(5, 5, world)

    robot.turn(-360)
    robot._make_eye_angles()
    #Start out at 0 therefore eye angles are
    assert robot.eye_angles['left'] == (350,50)
    assert robot.eye_angles['right'] == (310, 10)

    robot.turn(30)
    robot._make_eye_angles()

    assert robot.eye_angles['left'] == (20, 80)
    assert robot.eye_angles['right'] == (340, 40)

def test_constructor_with_mutate():
   pass

def test_age_robot():
    pass

def test_get_ancestors():
    pass

def test_make_id():








