import pygame
import sys
from opponent import Opponent
import time

class DojoGame:
    def __init__(self):
        pygame.init()

        self.width, self.height = 1060, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Kung Fu Fighter")

        self.white = (255, 255, 255)

        self.background = pygame.image.load("assets/images/dojo_bknd.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
        self.fighter_height, self.fighter_width = 200, 200
        self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
        
        self.fighter_x, self.fighter_y = 0, 600
        self.fighter_speed = 5

        self.direction = 1
        self.clock = pygame.time.Clock()
        self.opponent_start_time = time.time()
        self.dt = 0
        self.timer = 3000

        self.kf_opponent = Opponent(self)
        self.run_time = 120
        self.elapsed_time = 0

        self.health = 100
    def deduct_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            # Game over logic (you can customize this according to your game requirements)
            print("You were killed. Game Over")
            pygame.quit()
            sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    def move_fighter(self, keys):
        if keys[pygame.K_l] and self.fighter_x > 0:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
            self.fighter_x -= self.fighter_speed

        if keys[pygame.K_r] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
            self.fighter_x += self.fighter_speed

        if keys[pygame.K_p] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_punch.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))

        if keys[pygame.K_k] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_kick.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))

    def check_boundaries(self):
        if self.fighter_x <= 0 or self.fighter_x >= self.width - self.fighter_width:
            self.direction *= -1
    
    def update_opponent(self):
        elapsed_time = time.time() - self.opponent_start_time
        if elapsed_time > self.kf_opponent.timer_duration:
            self.kf_opponent.update_fsm(self.kf_opponent.TIME_UP)

            opponent_state = self.kf_opponent.get_state()

            if opponent_state == self.kf_opponent.LEFT:
                self.kf_opponent.move_left()
            elif opponent_state == self.kf_opponent.RIGHT:
                self.kf_opponent.move_right()
            elif opponent_state == self.kf_opponent.ATTACK:
                self.kf_opponent.perform_attack()

            # Check for collision with the player
            if self.kf_opponent.is_contacting_player(self.fighter_x, self.fighter_y, self.fighter_width, self.fighter_height):
                self.kf_opponent.handle_collision(self)

            self.opponent_start_time = time.time()


    def update_display(self):
        self.screen.fill(self.white)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.fighter_image, (self.fighter_x, self.fighter_y))
        self.kf_opponent.draw(self.screen)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {self.health}", True, (255, 0, 0))
        self.screen.blit(health_text, (10, 10))

    def update_opponent_state(self):
        elapsed_time = time.time() - self.opponent_start_time
        if elapsed_time > self.kf_opponent.timer_duration:
            self.kf_opponent.update_fsm(self.kf_opponent.TIME_UP)

            opponent_state = self.kf_opponent.get_state()

            if opponent_state == self.kf_opponent.LEFT:
                self.kf_opponent.move_left()
            elif opponent_state == self.kf_opponent.RIGHT:
                self.kf_opponent.move_right()
            elif opponent_state == self.kf_opponent.ATTACK:
                self.kf_opponent.perform_attack()

            # Check for collision with the player
            if self.kf_opponent.is_contacting_player(self.fighter_x, self.fighter_y, self.fighter_width, self.fighter_height):
                self.kf_opponent.handle_collision(self)

            self.opponent_start_time = time.time()

    def update_opponent_movement(self):
        opponent_state = self.kf_opponent.get_state()

        if opponent_state == self.kf_opponent.LEFT:
            self.kf_opponent.move_left()
        elif opponent_state == self.kf_opponent.RIGHT:
            self.kf_opponent.move_right()
        elif opponent_state == self.kf_opponent.ATTACK:
            self.kf_opponent.perform_attack()

    def run(self):
        running = True
        while self.elapsed_time < self.run_time and running:
            self.dt += self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.handle_events()

            keys = pygame.key.get_pressed()
            self.move_fighter(keys)

            self.check_boundaries()

            self.update_opponent_state()
            self.update_opponent_movement()

            self.update_display()

            pygame.display.flip()

            self.elapsed_time += 1


if __name__ == "__main__":
    game = DojoGame()
    game.run()

