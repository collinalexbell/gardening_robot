import world
import pygame

def test_load_pygame_image():
    file_name = 'robot.png'
    img = world.load_pygame_img(file_name)
    assert type(img) == pygame.Surface
	
def test_robot_init():
    robot = world.Robot(30,30, None)
    assert type(robot.sprites['up_s']) == pygame.Surface
    assert type(robot.sprites['up_l']) == pygame.Surface
    assert type(robot.sprites['up_r']) == pygame.Surface
    assert type(robot.sprites['left_s']) == pygame.Surface
    assert type(robot.sprites['left_l']) == pygame.Surface
    assert type(robot.sprites['left_r']) == pygame.Surface
    assert type(robot.sprites['right_s']) == pygame.Surface
    assert type(robot.sprites['right_l']) == pygame.Surface
    assert type(robot.sprites['right_r']) == pygame.Surface
    assert type(robot.sprites['down_s']) == pygame.Surface
    assert type(robot.sprites['down_l']) == pygame.Surface
    assert type(robot.sprites['down_r']) == pygame.Surface

def test_sense_gardens():
    test_world = world.World()
    test_world.add_robot(30,30)
    test_world.add_garden(40,30)

    #Test garden in front
    first_measurement = test_world.robots[0].sense_garden('front')
    test_world.robots[0].move()
    test_world.robots[0].act()
    second_measurement = test_world.robots[0].sense_garden('front')
    assert first_measurement < second_measurement



def test_garden_in_world():
    test_world = world.World()
    test_world.add_garden(50,60)
    assert len(test_world.get_gardens()) == 1
    assert test_world.get_gardens()[0].x == 50
    assert test_world.get_gardens()[0].y == 60


