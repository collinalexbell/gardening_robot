from garden import Garden
from world import World
import json

world = World()

def test_load_config():
    garden = Garden(0,0,world)
    config = {'garden':{'capacity':5}, 'robot':{'speed':5}}

    garden._load_config(config)
    assert garden.capacity == 5

def test_load_config_from_json():

    garden = Garden(0,0,world)
    config = {'garden':{'capacity':5}, 'robot':{'speed':5}}
    with open('test_config.json', 'w+') as f:
        f.write(json.dumps(config))
    garden._load_config_from_json('test_config.json')
    assert garden.capacity == 5

def test_harvest():
    garden = Garden(0,0,world)
    garden.capacity = 5

    for i in range(5):
        assert garden.harvest()

    assert not garden.harvest()
    assert garden.is_fully_harvested()
