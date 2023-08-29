import pygame
import pacman_constants as C
class GameObjects:
    def __init__(self, x, y, pacman):
        self.pos_x = x
        self.pos_y = y
        self.pacman = pacman
    def initialize_pacman_object(self):
        print('game objects')
    def update(self):
        print('game objects')       
    def display(self):
        print('game objects')

class PlayerBaseState:
    def __init__(self, player):
        self.player = player
    def enter_player_state(self, state_manager):
        pass
    
    def update_player_state(self, state_manager):
        pass

class PlayerRunningState(PlayerBaseState):
    def enter_player_state(self, state_manager):
        self.player.is_alive = True

    def update_player_state(self, state_manager):
        if self.player.is_alive:
            self.player.tally_points()
        else:
            state_manager.switch_state(state_manager.player_dead_state)

class PlayerDeadState(PlayerBaseState):
    def enter_player_state(self, state_manager):
        pass
    
    def update_player_state(self, state_manager):
        pass
    
class PlayerStartState(PlayerBaseState):
    def enter_player_state(self, state_manager):
        pass
    
    def update_player_state(self, state_manager):
        if state_manager.pacman.game_counter > 180 and not state_manager.player.is_alive:
            state_manager.switch_player_state(state_manager.player_running_state)

class PlayerStateManager:
    def __init__(self, pacman, player):
        self.pacman = pacman
        self.player = player
        self.cur_state = PlayerBaseState(player)
        self.player_start_state = PlayerStartState(player)
        self.player_running_state = PlayerRunningState(player)
        self.player_dead_state = PlayerDeadState(player)
        self.cur_state = self.player_start_state
    
    def init_state(self):
        pass

    def update_player_state(self):
        self.cur_state.update_player_state(self)

    def switch_player_state(self, new_player_state):
        self.cur_state = new_player_state
        new_player_state.enter_player_state(self)





class Player(GameObjects):

    def __init__(self, x, y, pacman):
        super().__init__(x, y, pacman)
        self.manager = PlayerStateManager(pacman, self)
        self.lives = 3
        self.is_alive = False
        self.center_x = x + 23
        self.center_y = y + 24
        self.cur_direction = C.Direction.RIGHT
        self.valid_turns = [False, False, False, False]
        self.player_images = []
        self.dsply_cnt = 0
    
    def initialize_pacman_object(self):
        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'Images/{i}.png'), (45, 45)))

    def update(self):
        self.manager.update_player_state() # Gives us directions player can move
        
        self.check_turns()
        self.direction_update() 
        if self.pacman.is_playing:
            self.move()
        self.display()
        self.update_dsply_cnt()
    
    def direction_update(self):
        if self.pacman.direction_command == C.Direction.RIGHT and self.valid_turns[0]:
            self.cur_direction = C.Direction.RIGHT
        if self.pacman.direction_command == C.Direction.LEFT and self.valid_turns[1]:
            self.cur_direction = C.Direction.LEFT
        if self.pacman.direction_command == C.Direction.UP and self.valid_turns[2]:
            self.cur_direction = C.Direction.UP
        if self.pacman.direction_command == C.Direction.DOWN and self.valid_turns[3]:
            self.cur_direction = C.Direction.DOWN
    
    def update_dsply_cnt(self):
        self.dsply_cnt += 1
        if self.dsply_cnt > 19:
            self.dsply_cnt = 0
    
    def not_wall(self, y, x):
        return x >= 900 or self.pacman.level[y // C.TILE_Y][x // C.TILE_X] < 3
    
    def in_lane(self, x, y):
        return 12 <= (x % y) <= 18

    def check_turns(self):
        self.valid_turns = [False, False, False, False]
        if self.center_x // C.TILE_X < C.TILE_X: # on the board (not exiting one side)
            if self.cur_direction == C.Direction.LEFT:
                self.valid_turns[0] = self.not_wall(self.center_y, self.center_x + C.SHIM) # turn right
            if self.cur_direction == C.Direction.RIGHT:
                self.valid_turns[1] = self.not_wall(self.center_y, self.center_x - C.SHIM)# turn left
            if self.cur_direction == C.Direction.DOWN:
                self.valid_turns[2] = self.not_wall(self.center_y - C.SHIM, self.center_x) # turn up
            if self.cur_direction == C.Direction.UP:
                self.valid_turns[3] = self.not_wall(self.center_y + C.SHIM, self.center_x) # turn down

            if self.cur_direction == C.Direction.UP or self.cur_direction == C.Direction.DOWN:
                if self.in_lane(self.center_x, C.TILE_X):
                    if self.not_wall(self.center_y + C.SHIM, self.center_x):
                        self.valid_turns[3] = True
                    if self.not_wall(self.center_y - C.SHIM, self.center_x):
                        self.valid_turns[2] = True
                if self.in_lane(self.center_y, C.TILE_Y):
                    if self.not_wall(self.center_y, self.center_x - C.TILE_X):
                        self.valid_turns[1] = True
                    if self.not_wall(self.center_y, self.center_x + C.TILE_X):
                        self.valid_turns[0] = True
            if self.cur_direction == C.Direction.LEFT or self.cur_direction == C.Direction.RIGHT:
                if self.in_lane(self.center_x, C.TILE_X): 
                    if self.not_wall(self.center_y + C.TILE_Y, self.center_x):
                        self.valid_turns[3] = True
                    if self.not_wall(self.center_y - C.TILE_Y, self.center_x):
                        self.valid_turns[2] = True
                if self.in_lane(self.center_y, C.TILE_Y): 
                    if self.not_wall(self.center_y, self.center_x - C.SHIM):
                        self.valid_turns[1] = True
                    if self.not_wall(self.center_y, self.center_x + C.SHIM):
                        self.valid_turns[0] = True
        else:
            self.valid_turns[0] = True
            self.valid_turns[1] = True
        
    def move(self):
        if self.cur_direction == C.Direction.RIGHT and self.valid_turns[0]:
            self.pos_x += self.pacman.game_speed
        if self.cur_direction == C.Direction.LEFT and self.valid_turns[1]:
            self.pos_x -= self.pacman.game_speed
        if self.cur_direction == C.Direction.UP and self.valid_turns[2]:
            self.pos_y -= self.pacman.game_speed
        if self.cur_direction == C.Direction.DOWN and self.valid_turns[3]:
            self.pos_y += self.pacman.game_speed
        
        self.update_center_pos()
    
    def update_center_pos(self):
        self.center_x = self.pos_x + 23
        self.center_y = self.pos_y + 24
        if self.pos_x > 900:
            self.pos_x = -47
        elif self.pos_x < -50:
            self.pos_x = 897

    def display(self):
        if self.cur_direction == C.Direction.RIGHT:
            self.pacman.screen.blit(self.player_images[self.dsply_cnt // 5], (self.pos_x, self.pos_y)) 
        elif self.cur_direction == C.Direction.LEFT:
            self.pacman.screen.blit(pygame.transform.flip(self.player_images[self.dsply_cnt // 5], True, False), (self.pos_x, self.pos_y)) 
        elif self.cur_direction == C.Direction.UP:
            self.pacman.screen.blit(pygame.transform.rotate(self.player_images[self.dsply_cnt // 5], 90), (self.pos_x, self.pos_y))
        elif self.cur_direction == C.Direction.DOWN:
            self.pacman.screen.blit(pygame.transform.rotate(self.player_images[self.dsply_cnt // 5], 270), (self.pos_x, self.pos_y))
    
    def tally_points(self):
        # Must make sure we are on the board
        if 0 < self.pos_x < 870:
            if self.pacman.level[self.center_y // C.TILE_Y][self.center_x // C.TILE_X] == 1:
                self.pacman.level[self.center_y // C.TILE_Y][self.center_x // C.TILE_X] = 0
                self.pacman.score += 10
            if self.pacman.level[self.center_y // C.TILE_Y][self.center_x // C.TILE_X] == 2:
                self.pacman.level[self.center_y // C.TILE_Y][self.center_x // C.TILE_X] = 0
                self.pacman.score += 50
                self.pacman.power_up = True
                self.pacman.power_counter = 0

class GhostBaseState:
    def __init__(self, ghost, ghost_manger):
        self.ghost = ghost
        self.ghost_manager = ghost_manger
    def enter_ghost_state(self):
        pass
    def update_ghost_state(self):
        pass

class GhostStateManager:
    def __init__(self, pacman, ghost):
        self.pacman = pacman
        self.ghost = ghost
        self.cur_state = GhostBaseState(ghost, self)
        self.ghost_start_state = GhostStartState()
        self.ghost_attack_state = GhostAttackState()
        self.ghost_dead_state = GhostDeadState()
        self.cur_state = self.ghost_start_state

    def update_ghost_state(self):
        self.cur_state.update_ghost_state(self)

    def switch_ghost_state(self, new_ghost_state):
        self.cur_state = new_ghost_state
        new_ghost_state.enter_ghost_state(self)


class GhostStartState:
    def update_ghost_state(self, ghost_manager):
        if ghost_manager.pacman.is_playing:
            ghost_manager.switch_ghost_state(ghost_manager.ghost_attack_state)

    def enter_ghost_state(self, new_ghost_state):
        self.cur_state = new_ghost_state

class GhostAttackState:
    def update_ghost_state(self, ghost_manager):

        if ghost_manager.pacman.power_up:
            ghost_manager.switch_ghost_state(ghost_manager.ghost_dead_state)

    def enter_ghost_state(self, ghost_manager):
        ghost_manager.ghost.is_scared = False

class GhostDeadState:
    def update_ghost_state(self, ghost_manager):
        if not ghost_manager.pacman.power_up:
            ghost_manager.switch_ghost_state(ghost_manager.ghost_attack_state)

    def enter_ghost_state(self, ghost_manager):
        ghost_manager.ghost.is_scared = True

    

class Ghostt(GameObjects):
    def __init__(self, x, y, pacman, color, dead, powerup, direction, target):
        super().__init__(x, y, pacman)
        self.state_manager = GhostStateManager(pacman, self)
        self.images = []
        self.cur_direction = direction
        self.target = target
        self.center_x = self.pos_x + 22
        self.center_y = self.pos_y + 22
        self.is_scared = False
        self.is_moving = False
        self.is_alive = True
        self.in_the_box = True

        self.load_images(color, dead, powerup)
        self.rect = self.display()
    
    def display(self):
        if self.is_alive and not self.is_scared:
            self.pacman.screen.blit(self.images[0], (self.pos_x, self.pos_y))
        elif self.is_scared:
            self.pacman.screen.blit(self.images[2], (self.pos_x, self.pos_y))
        else:
            self.pacman.screen.blit(self.images[1], (self.pos_x, self.pos_y))
        
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))

        return ghost_rect

    def update(self):
        self.state_manager.update_ghost_state()
        self.display()

    def load_images(self,color, dead, powerup):
        self.images.append(pygame.transform.scale(pygame.image.load(f'Images/{color}.png'), (45, 45)))
        self.images.append(pygame.transform.scale(pygame.image.load(f'Images/{dead}.png'), (45, 45)))
        self.images.append(pygame.transform.scale(pygame.image.load(f'Images/{powerup}.png'), (45, 45)))

class PacmanBoard(GameObjects):
    def __init__(self, x, y, pacman, board):
        super().__init__(x, y, pacman)
        self.board = board
        self.flicker = False
        self.board_count = 0
    
    def initialize_pacman_object(self):
        self.display()
    
    def keep_board_count(self):
        if self.board_count > 40:
            self.board_count = 0
        else:
            self.board_count += 1
    
    def to_flicker(self):
        return self.board_count < 20
    
    def update(self):
        self.keep_board_count()
        self.flicker = self.to_flicker()
        self.display()
    
    def display(self):
        self.pacman.screen.fill('black')
        if self.pacman.power_up:
            pygame.draw.circle(self.pacman.screen, 'red', (450,450), 100)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.pacman.screen, 'white', ((col * C.TILE_X) + (.5 * C.TILE_X), row * C.TILE_Y + (.5 * C.TILE_Y)), 4)
                if self.board[row][col] == 2 and not self.flicker:
                    pygame.draw.circle(self.pacman.screen, 'white', ((col * C.TILE_X) + (.5 * C.TILE_X), row * C.TILE_Y + (.5 * C.TILE_Y)), 10)
                if self.board[row][col] == 3:
                    pygame.draw.line(self.pacman.screen, 'blue', (col * C.TILE_X + (.5 * C.TILE_X), (row * C.TILE_Y)), (col * C.TILE_X + (.5 * C.TILE_X), row * C.TILE_Y + C.TILE_Y))
                if self.board[row][col] == 4:
                    pygame.draw.line(self.pacman.screen, 'blue', (col * C.TILE_X, row * C.TILE_Y + (.5 * C.TILE_Y)), (col * C.TILE_X + C.TILE_X, (row * C.TILE_Y + (.5 * C.TILE_Y))))
                if self.board[row][col] == 5:
                    pygame.draw.arc(self.pacman.screen, 'blue', [(C.TILE_X * col - (.4 * C.TILE_X) - 2), row * C.TILE_Y + (C.TILE_Y * .5), C.TILE_X, C.TILE_Y], 0, C.PI/2, 3)
                if self.board[row][col] == 6:
                    pygame.draw.arc(self.pacman.screen, 'blue', [(C.TILE_X * col + (.5 * C.TILE_X)), row * C.TILE_Y + (C.TILE_Y * .5), C.TILE_X, C.TILE_Y], C.PI/2, C.PI, 3)
                if self.board[row][col] == 7:
                     pygame.draw.arc(self.pacman.screen, 'blue', [(C.TILE_X * col + (.5 * C.TILE_X)) , row * C.TILE_Y - (C.TILE_Y * .4), C.TILE_X, C.TILE_Y], C.PI, 3*C.PI/2, 3)
                if self.board[row][col] == 8:
                    pygame.draw.arc(self.pacman.screen, 'blue', [(C.TILE_X * col - (.4 * C.TILE_X)) , row * C.TILE_Y - (C.TILE_Y * .4), C.TILE_X, C.TILE_Y], 3*C.PI/2, 2*C.PI, 3)
                if self.board[row][col] == 9:
                    pygame.draw.line(self.pacman.screen, 'white', (col * C.TILE_X, row * C.TILE_Y + (.5 * C.TILE_Y)), (col * C.TILE_X + C.TILE_X, (row * C.TILE_Y + (.5 * C.TILE_Y))))
