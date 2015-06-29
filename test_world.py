from world import World
import world as w
import pygame

def test_load_pygame_img():
    file_name = 'robot.png'
    img = w.load_pygame_img(file_name)
    assert type(img) == pygame.Surface


def test_garden_in_world():
    test_world = World()
    test_world.add_garden(50,60)
    assert len(test_world.get_gardens()) == 1
    assert test_world.get_gardens()[0].x == 50
    assert test_world.get_gardens()[0].y == 60


def test_next_gen():
    world = World()
    for i in range (10):
        world.add_robot(0,0)

    robots = world.get_robots()

    #Select percentage for robots to keep
    percent_to_keep = 30

    winners = robots[0:3]

    #Make the winers win
    for winner in winners:
        winner.collect_garden()
        print('winner_id_in_test{}'.format(winner.id))

    #Call next gen
    world.next_gen(percent_to_keep)

    next_gen_robots = world.get_robots()

    #Make sure that there are 3 parents and 7 decendants
    for robot in next_gen_robots:
        is_winner = False
        is_decendant = False
        for winner in winners:
            if winner.id == robot.id:
                is_winner = True
            if winner.id in robot.get_ancestors():
                is_decendant = True
        print('winner_id:{}, robot.id:{}'.format(winner.id, robot.id))
        print('ancestors{}'.format(robot.get_ancestors()))
        assert is_winner or is_decendant













