import pygame
from fsm import FSM
import random 
import time
import sys

class OpponentFSM(pygame.sprite.Sprite):
    ATTACK, DEAD, LEFT, RIGHT, TIME_UP = "a", "d", "l","r", "t"
    def __init__(self, x = 20, y = 20):
        super().__init__()

        width, height = 1060, 800

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.timer_duration = 3
        health = 100
        self.x = x
        self.y = y
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
            # Change graphics to kick
            self.change_graphics("kick_image.png")  # Replace with the actual image file for kick
        else:
            # Change graphics to punch
            self.change_graphics("punch_image.png")  # Replace with the actual image file for punch
    def change_graphics(self, image_path):
        # Load the new image
        new_image = pygame.image.load(image_path)

        # Resize the image to match the fighter's dimensions (adjust as needed)
        new_image = pygame.transform.scale(new_image, (200, 200))

        # Set the new image to the fighter's image attribute
        fighter_image = new_image

    def move_left(self):
        self.x -= 5  # Adjust the speed as needed

    def move_right(self):
        self.x += 5  # Adjust the speed as needed
    
    def perform_dead(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        width, height = 1060, 800
        background = pygame.image.load("MazeKungFu/assets/images/dojo_bknd.png")  # Replace with your background image
        background = pygame.transform.scale(background, (width,height))
        fighter_image = pygame.image.load("MazeKungFu/assets/images/kung_fu_fighter_standing.png")  # Replace with your fighter image
        fighter_height, fighter_width = 200, 200
        fighter_image = pygame.transform.scale(fighter_image, (fighter_height,fighter_width))


    def run(self):
        start_time = time.time()
        background = pygame.image.load("MazeKungFu/assets/images/dojo_bknd.png")  # Replace with your background image
     
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            elapsed_time = time.time() - start_time
            print(elapsed_time)
            if elapsed_time > self.timer_duration:
                self.fsm.process(self.TIME_UP)
                start_time = time.time()
                pygame.display.flip()

            time.sleep(0.5)
        """ 
        

if __name__ == "__main__":
    tl = OpponentFSM()
    tl.run()
