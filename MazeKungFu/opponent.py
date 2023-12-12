import pygame
from fsm import FSM
import random 
import time
import sys

class Opponent(pygame.sprite.Sprite):
    ATTACK, DEAD, LEFT, RIGHT, TIME_UP, HEALTH_ZERO = "a", "d", "l","r", "t", "h"
    def __init__(self, game, x=20, y=20):
        super().__init__()
        self.game = game
        self.width, self.height = 1060, 800
        self.timer_duration = 3
        self.health = 100
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
        
        self.fsm.add_transition(self.TIME_UP, self.LEFT, self.move_right, self.RIGHT)
        #self.fsm.add_transition(self.TIME_UP, self.LEFT, self.perform_attack, self.ATTACK)

        self.fsm.add_transition(self.TIME_UP, self.RIGHT, self.move_left, self.LEFT)
        #self.fsm.add_transition(self.TIME_UP, self.RIGHT, self.perform_attack, self.ATTACK)

        self.fsm.add_transition(self.TIME_UP, self.ATTACK, self.move_right, self.RIGHT)
        #self.fsm.add_transition(self.TIME_UP, self.ATTACK, self.perform_attack, self.RIGHT)

        # New transition: When health reaches zero, go to DEAD state
        self.fsm.add_transition(self.HEALTH_ZERO, self.LEFT, self.perform_dead, self.DEAD)
        self.fsm.add_transition(self.HEALTH_ZERO, self.RIGHT, self.perform_dead, self.DEAD)
        self.fsm.add_transition(self.HEALTH_ZERO, self.ATTACK, self.perform_dead, self.DEAD)

    def update_fsm(self, input_symbol):
        # Update FSM based on input event (e.g., TIME_UP or HEALTH_ZERO)
        #print(input_symbol, self.get_state())
        self.fsm.process(input_symbol)
        self.check_health()
    def get_state(self):
        # TODO: Return the maze bot's current state
        return self.fsm.current_state

    def perform_attack(self):
        rand = random.random()
        if rand < 0.5:
            self.change_graphics("assets/images/opp_standing.png")  
        else:
            self.change_graphics("assets/images/opp_standing.png")  
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

    def handle_collision(self, player_instance):
        if self.check_collision(player_instance.fighter_x, player_instance.fighter_y, player_instance.fighter_width, player_instance.fighter_height):
            self.health -= 20  
            self.check_health()
            self.update_fsm(self.HEALTH_ZERO)  
            print("Player touched opponent! Opponent's health:", self.health)

    def move_left(self):
        #randomize pixel movement amount and if you are sending attack or left/right into fsm
        if(self.x > self.width/2):
            distance = random.randint(30, 50)
        else:
            distance = random.randint(10, 30)
        self.x -= distance

    def move_right(self):
        if(self.x < self.width/2):
            distance = random.randint(30, 50)
        else:
            distance = random.randint(10, 30)
        self.x += distance  
    
    def check_health(self):
        if self.health <= 0:
            self.update_fsm(self.HEALTH_ZERO)

    def perform_dead(self):
        print("dead")
        pygame.quit()
        sys.exit()        

    def draw(self, screen):
        screen.blit(self.fighter_image, (self.x, self.y))    
