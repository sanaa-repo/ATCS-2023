"""
Opponent class controls the opponent movements and fsm.

Author: @ Sanaa Kapur

Used GPT 3
"""

import pygame
from fsm import FSM
import random 

class Opponent(pygame.sprite.Sprite):
    ATTACK, DEAD, LEFT, RIGHT, TIME_UP = "a", "d", "l","r", "t"
    def __init__(self, game, x=20, y=20):
        super().__init__()
        self.game = game
        self.width, self.height = 1060, 800
        self.timer_duration = 1
        self.x = self.width - 200
        self.y = self.height - 200
        self.load_images()
        self.fsm = FSM(self.LEFT)
        self.init_fsm()

    def load_images(self):
        self.background = pygame.image.load("assets/images/dojo_bknd.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.fighter_image = pygame.image.load("assets/images/opp_standing.png")
        self.fighter_height, self.fighter_width = 200, 200
        self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))

    #creates FSM states
    def init_fsm(self):
        self.fsm.add_transition(self.TIME_UP, self.LEFT, self.choose_move, None)
        self.fsm.add_transition(self.TIME_UP, self.RIGHT, self.choose_move, None)
        self.fsm.add_transition(self.TIME_UP, self.ATTACK, self.choose_move, None)
            
    # Update FSM based on input event (e.g., TIME_UP)
    def update_fsm(self, input_symbol):
        #print(input_symbol, self.get_state())
        self.fsm.process(input_symbol)
    
    #returns current FSM state of opponent
    def get_state(self):
        return self.fsm.current_state
    
    #selects a state/move randomly for opponent
    def choose_move(self):
        rand = random.random()
        if rand < 0.3:
            self.fsm.set_state(self.LEFT)
        elif rand < 0.6:
            self.fsm.set_state(self.RIGHT)
        else:
            self.fsm.set_state(self.ATTACK)
        pygame.time.delay(500)
        self.change_graphics("assets/images/opp_standing.png")
        

    #chooses random attack each time
    def perform_attack(self):
        self.x -= 0
        rand = random.random()
        if rand < 0.5:
            self.change_graphics("assets/images/opp_punching.png")  
        else:
            self.change_graphics("assets/images/opp_kicking.png")  
    #changes graphics
    def change_graphics(self, image_path):
        new_image = pygame.image.load(image_path)
        new_image = pygame.transform.scale(new_image, (self.fighter_height, self.fighter_width))
        self.fighter_image = new_image
    #moves opponent left     
    def move_left(self):
        distance = random.randint(5, 15)
        self.x -= distance
        if self.x < 0:
            self.x = 0
    #moves opponent right
    def move_right(self):
        distance = random.randint(5, 15)
        self.x += distance
        if self.x > self.width - self.fighter_width:
            self.x = self.width - self.fighter_width  
    #draws screen
    def draw(self, screen):
        screen.blit(self.fighter_image, (self.x, self.y))    
