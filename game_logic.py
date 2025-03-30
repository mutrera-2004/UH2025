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
