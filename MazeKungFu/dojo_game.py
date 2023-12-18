"""
DojoGame class controls the entirety of the game, but especially the first dojo setting of it. It has player movement and flow of control.

Author: @ Sanaa Kapur

Used GPT 3
"""

import pygame
import sys
from opponent import Opponent
import time
from maze import MazeGame

class DojoGame:
    def __init__(self):
        pygame.init()

        #game window setup
        self.width, self.height = 1060, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Kung Fu Fighter")

        #colors
        self.white = (255, 255, 255)

        #background image
        self.background = pygame.image.load("assets/images/dojo_bknd.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        #fighter setup
        self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
        self.fighter_height, self.fighter_width = 200, 200
        self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
        self.fighter_x, self.fighter_y = 0, 600
        self.fighter_speed = 5

        self.direction = 1
        self.clock = pygame.time.Clock()
        self.opponent_start_time = time.time()
        self.dt = 0

        #opponent setup
        self.kf_opponent = Opponent(self)
        
        #timer and health setup
        self.run_time = 120
        self.elapsed_time = 0
        self.health = 40
        self.show_dojo = True  # Add this line to initialize the attribute
        pygame.mixer.music.load("assets/bknd_music.mp3")

        #movement
        self.state = "standing"

    #deduct health from player
    def deduct_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            print("You were defeated by your opponent and failed the black belt test. Game Over")
            pygame.quit()
            sys.exit()
    
    #add health to player
    def add_health(self, damage):
        self.health += damage
        if self.health <= 0:
            print("You were defeated by your opponent and failed the black belt test. Game Over")
            pygame.quit()
            sys.exit()

    #handles quitting
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting")
                pygame.quit()
                sys.exit()

    #moves main player
    def move_fighter(self, keys):
        if keys[pygame.K_l] and self.fighter_x > 0:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
            self.fighter_x -= self.fighter_speed
            self.state = "standing"

        if keys[pygame.K_r] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_standing.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
            self.fighter_x += self.fighter_speed
            self.state = "standing"

        if keys[pygame.K_p] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_punch.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
            self.state = "attacking"

        if keys[pygame.K_k] and self.fighter_x < self.width - self.fighter_width:
            self.fighter_image = pygame.image.load("assets/images/kung_fu_fighter_kick.png")
            self.fighter_height, self.fighter_width = 200, 200
            self.fighter_image = pygame.transform.scale(self.fighter_image, (self.fighter_height, self.fighter_width))
            self.state = "attacking"

    #prevents characters from going off the screen 
    def check_boundaries(self):
        if self.fighter_x <= 0 or self.fighter_x >= self.width - self.fighter_width:
            self.direction *= -1
    
    #handles health and collisions
    def update_health(self):
        elapsed_time = time.time() - self.opponent_start_time
        
        if elapsed_time > self.kf_opponent.timer_duration:
            self.kf_opponent.update_fsm(self.kf_opponent.TIME_UP)

            opponent_state = self.kf_opponent.get_state()
            if opponent_state == self.kf_opponent.LEFT:
                self.kf_opponent.move_left()
            elif opponent_state == self.kf_opponent.RIGHT:
                self.kf_opponent.move_right()
            elif opponent_state == self.kf_opponent.ATTACK:
                # Check for proximity to the opponent and deduct health
                if (
                    self.fighter_x < self.kf_opponent.x + self.kf_opponent.fighter_width
                    and self.fighter_x + self.fighter_width > self.kf_opponent.x
                ):
                    self.deduct_health(10)
                self.kf_opponent.perform_attack()
            if self.state == "attacking" and opponent_state != self.kf_opponent.ATTACK:
                if (
                    self.fighter_x < self.kf_opponent.x + self.kf_opponent.fighter_width
                    and self.fighter_x + self.fighter_width > self.kf_opponent.x
                ):
                    self.add_health(10)
            self.opponent_start_time = time.time()

    #updates pygame display
    def update_display(self):
        self.screen.fill(self.white)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.fighter_image, (self.fighter_x, self.fighter_y))
        self.kf_opponent.draw(self.screen)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {self.health}", True, (255, 0, 0))
        self.screen.blit(health_text, (10, 10))

    def run(self):
        print("Hello, and welcome to your black belt test. Today, we will test both your physical and mental abilities through 2 tests. You will need to survive both to win. Good luck, fighter!")
        running = True
        start_time = time.time()
        pygame.mixer.music.play(-1)

        print("Entering game loop...")
        while running and (time.time() - start_time) < 30:  # Change the total run time as needed
            print(time.time() - start_time)
            self.dt += self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting")
                    running = False

            self.handle_events()

            keys = pygame.key.get_pressed()
            self.move_fighter(keys)

            self.check_boundaries()

            # Update opponent's state
            elapsed_time = time.time() - self.opponent_start_time
            if elapsed_time > self.kf_opponent.timer_duration:
                self.update_health()
                self.kf_opponent.update_fsm(self.kf_opponent.TIME_UP)

                opponent_state = self.kf_opponent.get_state()
                print(f"Opponent state after TIME_UP transition: {opponent_state}")

                if opponent_state == self.kf_opponent.LEFT:
                    self.kf_opponent.move_left()
                elif opponent_state == self.kf_opponent.RIGHT:
                    self.kf_opponent.move_right()
                elif opponent_state == self.kf_opponent.ATTACK:
                    self.kf_opponent.perform_attack()

                self.opponent_start_time = time.time()

                # Print opponent's state again to see if it changed during actions
                print(f"Opponent state after actions: {self.kf_opponent.get_state()}")

            # Update opponent's movement
            opponent_state = self.kf_opponent.get_state()
            if opponent_state == self.kf_opponent.LEFT:
                self.kf_opponent.move_left()
            elif opponent_state == self.kf_opponent.RIGHT:
                self.kf_opponent.move_right()
            elif opponent_state == self.kf_opponent.ATTACK:
                self.kf_opponent.perform_attack()

            
            self.update_display()

            pygame.display.flip()

            self.elapsed_time += 1

            # Check for game over condition
            if self.health <= 0:
                print("You were killed. Game Over")
                running = False

            # Check if the player spent 60 seconds in the dojo
            if (time.time() - start_time) > 30 and not self.show_dojo:
                print("Entering Dojo")
                self.show_dojo = False
        
        while (time.time() - start_time) < 60:
            self.maze_game = MazeGame(21, 21, 30)
            self.maze_game.run()

        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = DojoGame()
    game.run()
