from world import Robot
import pygame

SCREEN_X = 1080
SCREEN_Y = 720

def robot_walk():
    
    import time
    robot = Robot()
    print(type(robot))
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Create the screen

    backdrop = pygame.Rect(0, 0, SCREEN_X, SCREEN_Y) #Create the whole screen so you can draw on it

    while True:
        screen.fill((0,0,0))
        screen.blit(robot.sprites['up_r'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['up_l'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['up_s'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.fill((0,0,0))
        screen.blit(robot.sprites['right_r'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['right_l'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['right_s'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['left_r'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['left_l'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['left_s'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['down_l'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['down_r'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)
        screen.fill((0,0,0))
        screen.blit(robot.sprites['down_s'],backdrop) #'Blit' on the backdrop
        pygame.display.flip()
        time.sleep(.5)

if __name__ == "__main__":
    print("Hello, please select a graphic demo")
    demos = [{"name":"In place robot sprites", "function":robot_walk}]

    for index, demo in enumerate(demos):
        print("{}. {}".format(index, demo['name']))

    selection = int(input('Please type number for demo: '))

    if(selection < len(demos)):
        demos[selection]['function']()
    

