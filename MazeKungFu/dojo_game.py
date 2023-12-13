import pygame
import sys
from opponent import Opponent  # Updated import statement
import time

class dojo_game:
    def __init__(self):
        pygame.init()

        # Set up display
        self.width, self.height = 1060, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Kung Fu Fighter")

        # Colors
        self.white = (255, 255, 255)

        # Load background
        self.background = pygame.image.load("assets/images/dojo_bknd.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Load kung fu fighter
        self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
        self.fighter_height, self.fighter_width = 200, 200
        self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
        
        self.fighter_x, self.fighter_y = 0, 600
        self.fighter_speed = 5

        # Set initial direction
        self.direction = 1  # 1 for right, -1 for left

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()
        self.opponent_start_time = time.time()  # Initialize opponent_start_time
        self.dt = 0
        self.timer = 3000


        # Updated instantiation using the new name
        self.kf_opponent = Opponent(self)



    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def move_fighter(self, keys):
        if keys[pygame.K_LEFT] and self.fighter_x > 0:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
            self.fighter_x -= self.fighter_speed

        if keys[pygame.K_RIGHT] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
            self.fighter_x += self.fighter_speed

        if keys[pygame.K_UP] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_punch.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))

        if keys[pygame.K_DOWN] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_kick.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))

    def check_boundaries(self):
        if self.fighter_x <= 0 or self.fighter_x >= self.width - self.fighter_width:
            self.direction *= -1
    
    def update_opponent(self):
        elapsed_time = time.time() - self.opponent_start_time
        if elapsed_time > self.kf_opponent.timer_duration:
            self.kf_opponent.update_fsm(self.kf_opponent.TIME_UP)  # Update FSM with the correct input symbol

            # Get the opponent's current state
            opponent_state = self.kf_opponent.get_state()

            # Update the opponent's position based on the current state
            if opponent_state == self.kf_opponent.LEFT:
                self.kf_opponent.move_left()
            elif opponent_state == self.kf_opponent.RIGHT:
                self.kf_opponent.move_right()

            self.opponent_start_time = time.time()


    def update_display(self):
        self.screen.fill(self.white)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.fighter_image, (self.fighter_x, self.fighter_y))
        self.kf_opponent.draw(self.screen)  # Draw opponent
        
    def run(self):
        # Main game loop
        running = True
        self.opponent_start_time = time.time()
        while running:
            # Set fps to 120
            self.dt += self.clock.tick(120)

            # Handle closing the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Only update every 120 fps
            if self.dt > 120:
                self.dt = 0
                self.kf_opponent.update_fsm(self.kf_opponent.TIME_UP)

                self.handle_events()

                keys = pygame.key.get_pressed()
                self.move_fighter(keys)

                self.check_boundaries()

                self.update_opponent()  # Update opponent

                self.update_display()
            pygame.display.flip()

#if __name__ == "__main__":
    #game = dojo_game()
    #game.run()
