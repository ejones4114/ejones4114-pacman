import pacman_constants as C
class MovementManager:
    def __init__(self, pacman):
        self.pacman = pacman
    
    def not_wall(self, y, x):
        return x >= 900 or self.pacman.level[y // C.TILE_Y][x // C.TILE_X] < 3
    
    def in_lane(self, x, y):
        return 12 <= (x % y) <= 18

    def check_turns(self, obj):
        valid_turns = [False, False, False, False]
        if obj.center_x // C.TILE_X < C.TILE_X: # on the board (not exiting one side)
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

        