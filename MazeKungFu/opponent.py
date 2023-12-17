import pygame
from fsm import FSM
import random 
import time
import sys

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


    def init_fsm(self):
        # randomize input (self.left/self.right/self.attack)
        self.fsm.add_transition(self.TIME_UP, self.LEFT, self.choose_move, None)
        self.fsm.add_transition(self.TIME_UP, self.RIGHT, self.choose_move, None)
        self.fsm.add_transition(self.TIME_UP, self.ATTACK, self.choose_move, None)
        
    def update_fsm(self, input_symbol):
        # Update FSM based on input event (e.g., TIME_UP or HEALTH_ZERO)
        #print(input_symbol, self.get_state())
        self.fsm.process(input_symbol)
        
    def get_state(self):
        # TODO: Return the maze bot's current state
        return self.fsm.current_state
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
        


    def perform_attack(self):
        self.x -= 0
        rand = random.random()
        if rand < 0.5:
            self.change_graphics("assets/images/opp_punching.png")  
        else:
            self.change_graphics("assets/images/opp_kicking.png")  
    def change_graphics(self, image_path):
        new_image = pygame.image.load(image_path)
        new_image = pygame.transform.scale(new_image, (self.fighter_height, self.fighter_width))
        self.fighter_image = new_image
    def check_collision(self, player_x, player_y, player_width, player_height):
    # Check for collision with the player
        if (
            self.x < player_x + player_width and
            self.x + self.fighter_width > player_x and
            self.y < player_y + player_height and
            self.y + self.fighter_height > player_y
        ):
            return True
        return False
            
    def move_left(self):
        #self.change_graphics("assets/images/opp_standing.png")
        distance = random.randint(5, 15)
        self.x -= distance
        if self.x < 0:
            self.x = 0

    def move_right(self):
        #self.change_graphics("assets/images/opp_standing.png")
        distance = random.randint(5, 15)
        self.x += distance
        if self.x > self.width - self.fighter_width:
            self.x = self.width - self.fighter_width

    def perform_dead(self):
        print("dead")
        #pygame.quit()
        #sys.exit()      
    def is_contacting_player(self, player_x, player_y, player_width, player_height):
        # Check for collision with the player
        if (
            self.x < player_x + player_width and
            self.x + self.fighter_width > player_x and
            self.y < player_y + player_height and
            self.y + self.fighter_height > player_y
        ):
            return True
        return False
  

    def draw(self, screen):
        screen.blit(self.fighter_image, (self.x, self.y))    
