import pygame
from fsm import FSM
import random 
import time
import sys

class opponent(pygame.sprite.Sprite):
    ATTACK, DEAD, LEFT, RIGHT, TIME_UP = "a", "d", "l","r", "t"
    def __init__(self, x = 20, y = 20):
        super().__init__()

        self.width, self.height = 1060, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.timer_duration = 3
        self.health = 100
        self.x = x
        self.y = y
        self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
        self.fighter_height, self.fighter_width = 200, 200
        self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
        self.fsm = FSM(self.LEFT)  # Initialize FSM with the initial state
        self.init_fsm()


    def init_fsm(self):
        self.fsm.add_transition(self.TIME_UP, self.LEFT, self.move_right, self.RIGHT)
        self.fsm.add_transition(self.TIME_UP, self.LEFT, self.perform_attack, self.ATTACK)
        self.fsm.add_transition(self.TIME_UP, self.LEFT, self.perform_dead, self.DEAD)

        self.fsm.add_transition(self.TIME_UP, self.RIGHT, self.move_right, self.LEFT)
        self.fsm.add_transition(self.TIME_UP, self.RIGHT, self.perform_attack, self.ATTACK)
        self.fsm.add_transition(self.TIME_UP, self.RIGHT, self.perform_dead, self.DEAD)

        self.fsm.add_transition(self.TIME_UP, self.ATTACK, self.move_right, self.LEFT)
        self.fsm.add_transition(self.TIME_UP, self.ATTACK, self.perform_attack, self.RIGHT)
        self.fsm.add_transition(self.TIME_UP, self.ATTACK, self.perform_dead, self.DEAD)

    def get_state(self):
        return self.fsm.current_state

    def perform_attack(self):
        rand = random.random()
        if rand < 0.5:
            self.change_graphics("assets/images/kung_fu_fighter_kick.png")  
        else:
            self.change_graphics("assets/images/kung_fu_fighter_punch.png")  
    def change_graphics(self, image_path):
        new_image = pygame.image.load(image_path)
        new_image = pygame.transform.scale(new_image, (self.fighter_height, self.fighter_width))
        self.fighter_image = new_image

    def move_left(self):
        self.x -= 5  # Adjust the speed as needed

    def move_right(self):
        self.x += 5  # Adjust the speed as needed
    def check_health(self):
        if self.health <= 0:
            self.perform_dead()

    def perform_dead(self):
        print("dead")
        pygame.quit()
        sys.exit()

    def draw(self):
        background = pygame.image.load("assets/images/dojo_bknd.png")
        background = pygame.transform.scale(background, (self.width, self.height))

        # Draw background
        self.screen.blit(background, (0, 0))

        # Draw fighter
        self.screen.blit(self.fighter_image, (self.x, self.y))
        
        """
        width, height = 1060, 800
        background = pygame.image.load("MazeKungFu/assets/images/dojo_bknd.png")  
        background = pygame.transform.scale(background, (width,height))
        fighter_image = pygame.image.load("MazeKungFu/assets/images/kung_fu_fighter_standing.png") 
        fighter_height, fighter_width = 200, 200
        fighter_image = pygame.transform.scale(fighter_image, (fighter_height,fighter_width))
        """

    def run(self):
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw()

            elapsed_time = time.time() - start_time
            print(elapsed_time)
            if elapsed_time > self.timer_duration:
                self.fsm.process(self.TIME_UP)
                start_time = time.time()

            pygame.display.flip()

        

