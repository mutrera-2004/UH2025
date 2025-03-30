from collections import deque
import pygame
import random
import config
from map import Map, Tiles
from bullet import Bullet
from player import Player
from zombies import Zombie

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
        self.bullets.append(bullet)
    
    def game_status(self) -> bool:
        """Returns `True` if the game is in progress and `False` if it's over"""
        return self.player.life > 0

    def get_player(self) -> Player:
        return self.player
    
    def spawn_zombie(self, num_zombies: int):
        for i in range(num_zombies):
            tile_num = random.randint(0, len(self.map.walkable) - 1)
            tile = self.map.walkable[tile_num]
            zombie = Zombie(30, tile.rect)
            self.zombies.add(zombie)


def fire_bullet(x: int, y: int, dir: config.Direction, zombies: set[Zombie], damage: int):
    if dir == config.Direction.LEFT:
        x -= 8
    elif dir == config.Direction.RIGHT:
        x += 8
    elif dir == config.Direction.DOWN:
        y += 8
    else:
        y -= 8

    for zombie in zombies:
        p1, p2 = zombie.position.topleft, zombie.position.topright
        p3, p4 = zombie.position.bottomleft, zombie.position.bottomright
        if p1 <= x <= p2 and p3 <= y <= p4:
            zombie.life -= damage
            if zombie.life <= 0:
                zombies.remove(zombie)
            break