import math
from enum import Enum
import pygame



PI = math.pi
WIDTH = 900
HEIGHT = 950
TILE_Y = ((HEIGHT - 50) // 32)   # Tile size y in pixels
TILE_X = (WIDTH // 30)           # tile size x in pixels
SHIM = 15               # wiggle factor when crashing into walls, etc
FPS = 60
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
# FONT = pygame.font.Font('freesansbold.ttf', 20)

class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3