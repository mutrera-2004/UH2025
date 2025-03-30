from enum import Enum
import math
import pygame

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

def distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def generate_glow(glow, radius):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    layers = 30
    glow = pygame.math.clamp(glow, 0, 200)
    for i in range(layers):
        k = i * glow
        k = pygame.math.clamp(k, 0, 200)
        pygame.draw.circle(surf, (k, k, k), surf.get_rect().center, radius - i * 3)
    
    return surf

glow = generate_glow(6, TILE_SIZE * 4)
