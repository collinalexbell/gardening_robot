import sdl2.ext

BLACK = sdl2.ext.Color(0, 0, 0)

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(255, 255, 255))
        super(SoftwareRenderer, self).render(components)

class Robot_Entity(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite_positions = Sprite_Positions(sprite)
        self.sprite = self.sprite_positions.up_standing
        self.sprite.position = posx, posy
        self.velocity = Velocity()
        
class Sprite_Positions:
    def __init__(self, master_sprite):
         
        self.up_standing = master_sprite.subsprite((0,0,35,55))
        self.up_steps = [(35,0),(75,0)]
        self.left_standing = (0, 60)
        self.left_steps = [(35,60),(75,60)]
        self.right_standing = (0, 115)
        self.right_steps = [(35,115),(75,115)]
        self.up_standing = (0, 165)
        self.up_steps = [(35,165),(75,165)]




class Robot:
    def __init__(self, world, posx=0, posy=0):
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        self.sprite = factory.from_image('robot.png')
        self.entity = Robot_Entity(world, self.sprite, posx, posy)
        self.forward_tick = 0
        self.go_forward = False
        self.unit_forward = (1,0)

    def act(self):
        print(self.go_forward)
        if self.go_forward:
            forward_multiplier = self.compute_forward_multiplier()
            self.entity.velocity.vx = self.unit_forward[0] * forward_multiplier
            self.entity.velocity.vy = self.unit_forward[1] * forward_multiplier
        else:
            self.entity.velocity.vx = 0
            self.entity.velocity.vy = 0
    
    def compute_forward_multiplier(self):
        #Will go through a 3 tick forward cycle
        if self.forward_tick < 4:
            self.forward_tick += 1
            return self.forward_tick
        elif self.forward_tick == 4:
            self.forward_tick += 1
            return 4
        elif self.forward_tick < 8:
            self.forward_tick += 1
            return 7 - self.forward_tick
        else:
            self.forward_tick = 0
            self.go_forward = False
            return 1


    def forward(self):
        self.go_forward = True


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class Simulation_World:
    def __init__(self, name, width, height):
        sdl2.ext.init()
        self.window = sdl2.ext.Window(name, size=(width, height))
        self.window.show()
        self.world = sdl2.ext.World()

        self.movement = MovementSystem(0, 0, width, height)
        self.spriterenderer = SoftwareRenderer(self.window)

        self.world.add_system(self.movement)
        self.world.add_system(self.spriterenderer)

        self.player1 = Robot(self.world, 0, 250)

        self.running = True

    def start_loop(self):
        while self.running:
            self.game_iteration()

    def game_iteration(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                self.running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_SPACE:
                    pass
                    self.player1.forward()
        self.player1.act()
        self.world.process()
