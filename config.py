import pygame
from enum import Enum

WIDTH = 960
HEIGHT = 640

TILE_SIZE = 64
PLAYER_RECT = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)
ZOMBIE_RECT = pygame.rect.Rect(20, 20, TILE_SIZE, TILE_SIZE)

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

def find_mouse_coords():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    center_x = WIDTH // 2
    center_y = HEIGHT //2 

    relative_x = mouse_x - center_x
    relative_y = -(mouse_y - center_y)

    return (relative_x, relative_y)
