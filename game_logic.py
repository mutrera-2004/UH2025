"Classes for game and player. Function for firing bullets."

import math
import config
import pygame
from map import Tiles

RED = (255, 0, 0)  # temp color
YELLOW = (255, 255, 0)
GREEN = (0, 0, 255)



class Game:
    """
    Class representing the Game

    Attributes:
        - game_over [bool]: whether the game is over or not depending
            on the player's health
        - player [Player]: player
        - Zombies [list[Zombie]]: list of existing zombies in the map
    """

    _game_over = bool

    def __init__(self):
        self._game_over = False

    @property
    def game_over(self):
        return self._game_over


    def set_direction(self):
        mouse_x, mouse_y = config.find_mouse_coords()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x, center_y = config.WIDTH // 2, config.HEIGHT // 2

        mouse_x = mouse_x - center_x
        mouse_y = -(mouse_y - center_y)  # flip so it behaves like cartesian plane

        theta = math.atan2(mouse_y, mouse_x)
        theta = math.degrees(theta)
        if -45 <= theta <= 45:
            self._direction = Direction.RIGHT

        elif 45 < theta <= 135:
            self._direction = Direction.UP

        elif theta > 135 or -180 <= theta <= -135:
            self._direction = Direction.LEFT

        elif -135 < theta < -45:
            self._direction = Direction.DOWN
