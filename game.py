from collections import deque
import pygame
from map import Map
import config
from game_logic import Player, Zombie, Bullet

class Game:
    def __init__(self, map: Map, player: Player=None, zombies: set[Zombie]=set()):
        self.map = map
        self.player = player
        self.zombies = zombies
        if self.player is None:
            self.player = Player(30, pygame.Rect())
        self.bullets = deque()
        self.game_over = False
    
    def fire_bullet(self):
        if self.player.bullets == 0:
            return
        bullet = Bullet(self.player.position)
    
    def game_status(self) -> bool:
        """Returns `True` if the game is in progress and `False` if it's over"""
        return self.player.life > 0

    def get_player(self) -> Player:
        return self.player
    
    def spawn_zombie(self, zombie: Zombie):
        self.zombies.add(zombie)