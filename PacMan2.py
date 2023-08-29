import pygame
import sys
import copy
from pygame.locals import *
from board import b
# import pacman_board as pb

import pacman_constants as C
import GameObjects as gos

# screen = pygame.display.set_mode([C.WIDTH, C.HEIGHT])

class PacMan:
    def __init__(self, b):
        self.level = copy.deepcopy(b)   # the board layout
        # self.font = pygame.font.SysFont('freesansbold.ttf', 20)
        self.game_objects = []  # Player, board and ghosts
        self.game_speed = 2 # how quickly objects move on board
        self.score = 0      # player score
        self.direction_command = C.Direction.RIGHT   # Current keyboard input value
        self.game_counter = 0
        self.is_playing = False
        self.power_counter = 0
        self.power_up = False
        self.player = None
        
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode([C.WIDTH, C.HEIGHT])

        self.init_pacman_objects()
        self.init_pacman()
    
    def init_pacman(self):
        for obj in self.game_objects:
            obj.initialize_pacman_object()
    
    def init_pacman_objects(self):
        self.game_objects.append(gos.PacmanBoard(0, 0, self, self.level))
        self.game_objects.append(gos.Player(450, 663, self))
        self.player = self.game_objects[1]
        self.game_objects.append(gos.Ghostt(56, 58, self, 'blue', 'dead','powerup', C.Direction.RIGHT, (450, 663)))
        self.game_objects.append(gos.Ghostt(450, 388, self, 'red', 'dead','powerup', C.Direction.UP, (450, 663)))
        self.game_objects.append(gos.Ghostt(440, 438, self, 'orange', 'dead','powerup', C.Direction.UP, (450, 663)))
        self.game_objects.append(gos.Ghostt(440, 438, self, 'pink','dead','powerup', C.Direction.UP, (450, 663)))
        


    def run_game(self):
        self.timer.tick(C.FPS)
        for event in pygame.event.get():
            self.process_event(event)
        for obj in self.game_objects:
            obj.update()
        self.update_game()
        pygame.display.flip()
    
    def update_game(self):
        self.game_time_counter()
        if self.game_counter > 180:
            self.is_playing = True
        if self.power_up:
            self.check_power_up()
    def check_power_up(self):
        if self.power_counter < 600:
            self.power_counter += 1
        else:
            self.power_up = False
    
    def process_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.direction_command = C.Direction.RIGHT
            if event.key == pygame.K_LEFT:
                self.direction_command = C.Direction.LEFT     
            if event.key == pygame.K_UP:
                self.direction_command = C.Direction.UP
            if event.key == pygame.K_DOWN:
                self.direction_command = C.Direction.DOWN
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and self.direction_command == C.Direction.RIGHT: 
                self.direction_command = self.player.cur_direction
            if event.key == pygame.K_LEFT and self.direction_command == C.Direction.LEFT:
                self.direction_command = self.player.cur_direction     
            if event.key == pygame.K_UP and self.direction_command == C.Direction.UP:
                self.direction_command = self.player.cur_direction
            if event.key == pygame.K_DOWN and self.direction_command == C.Direction.DOWN:
                self.direction_command = self.player.cur_direction

    def game_time_counter(self):
        if self.game_counter == 600:
            self.game_counter = 0
        else:
            self.game_counter += 1

p = PacMan(b)
while True:
    p.run_game()