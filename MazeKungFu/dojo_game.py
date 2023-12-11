import pygame
import sys
from opponent import opponent  # Updated import statement
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

        # Updated instantiation using the new name
        self.kf_opponent = opponent()



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
        self.kf_opponent.draw()  # Draw opponent
        elapsed_time = time.time() - self.opponent_start_time

        if elapsed_time > self.kf_opponent.timer_duration:
            self.kf_opponent.fsm.process(self.kf_opponent.TIME_UP)
            self.opponent_start_time = time.time()

    def update_display(self):
        self.screen.fill(self.white)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.fighter_image, (self.fighter_x, self.fighter_y))
        pygame.display.flip()

    def run(self):
        self.opponent_start_time = time.time()

        while True:
            self.handle_events()

            keys = pygame.key.get_pressed()
            self.move_fighter(keys)

            self.check_boundaries()

            self.update_opponent()  # Update opponent

            self.update_display()

            self.clock.tick(30)

if __name__ == "__main__":
    game = dojo_game()
    game.run()
