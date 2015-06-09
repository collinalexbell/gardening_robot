from nose.tools import *
import sys
import sdl2
import sdl2.ext
import inspect

NUM_ON_FIELD_PER_TEAM = 11

WHITE = sdl2.ext.Color(255, 255, 255)
RED = sdl2.ext.Color(255, 0, 0)
BLUE = sdl2.ext.Color(0, 0, 255)

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy

class Team:
    def __init__(self,world, color=BLUE):
        self.players_on_field = []
        self.sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        self.team_color = color

        for i in range(NUM_ON_FIELD_PER_TEAM):
            player_sprite = self.sprite_factory.from_color(self.team_color, size=(10,10))
            self.players_on_field.append(Player(world, player_sprite))

            
def test_team_init():
    world = sdl2.ext.World()
    team = Team(world)

    #Team has NUM_ON_FIELD_PER_TEAM players
    assert len(team.players_on_field) == NUM_ON_FIELD_PER_TEAM






def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    window.show()
    running = True
    world = sdl2.ext.World()

    spriterenderer = SoftwareRenderer(window)
    world.add_system(spriterenderer)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_paddle1 = factory.from_color(WHITE, size=(10, 10))
    sp_paddle2 = factory.from_color(WHITE, size=(10, 10))
    sp_paddle3 = factory.from_color(WHITE, size=(10, 10))
    sp_paddle4 = factory.from_color(WHITE, size=(10, 10))

    player1 = Player(world, sp_paddle1, 10, 250)
    player2 = Player(world, sp_paddle2, 100, 250)
    player3 = Player(world, sp_paddle3, 670, 250)
    player4 = Player(world, sp_paddle4, 770, 250)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if(event.type == sdl2.SDL_KEYDOWN):
                print(event.keysym)
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        world.process()

if __name__ == "__main__":
    sys.exit(run())
