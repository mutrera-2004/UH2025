"Classes for game and player. Function for firing bullets."

import math
from enum import Enum
import config
import pygame

RED = (255, 0, 0)  # temp color
YELLOW = (255, 255, 0)
GREEN = (0, 0, 255)


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


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


class Player:
    """
    Class representing a Player

    Attributes:
        - life [int]: percentage of health left
        - bullets [int]: number of bullets left on the gun
        - position [pygame.Rect]: position of the object
    """

    _life: int
    _bullets: int
    _position: pygame.Rect
    _facing: pygame.Rect

    def __init__(self, bullets: int, position: pygame.Rect):
        self._life = 100
        self._num_bullets = bullets
        self._position = position
        self._direction = Direction.RIGHT

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, new_health: int):
        self._life = max(0, min(new_health, 100))

    @property
    def bullets(self):
        return self._bullets

    @bullets.setter
    def bullets(self, value: int):
        self._bullets = max(0, value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: pygame.Rect):
        self._position = value

    @property
    def direction(self):
        return self._direction

    def set_direction(self):
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


class Zombie:
    def __init__(self, damage: int, position: pygame.Rect):
        self._life = 100
        self._damage = damage
        self._direction = Direction.RIGHT
        self._position = position

    @property
    def life(self):
        """Zombie's current health."""
        return self._life

    @life.setter
    def life(self, new_health: int):
        """Zombie's current health."""
        self._life = max(0, min(new_health, 100))

    @property
    def damage(self):
        """Damage per hit."""
        return self._damage

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos: pygame.Rect):
        self._position = pos

    def set_direction(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x, center_y = config.WIDTH // 2, config.HEIGHT // 2

        mouse_x = mouse_x - center_x
        mouse_y = -(mouse_y - center_y)  # flip so it behaves like cartesian plane

        theta = math.atan2(mouse_y, mouse_x)
        theta = math.degrees(theta)
        if 0 <= theta <= 45 and 315 < theta < 360:
            self._direction = Direction.RIGHT

        elif 45 < theta <= 135:
            self._direction = Direction.UP

        elif 135 < theta <= 225:
            self._direction = Direction.LEFT

        elif 225 < theta <= 315:
            self._direction = Direction.RIGHT
    
    def draw(self, surface: pygame.surface):
        self.set_direction()
        pygame.draw.rect(surface, GREEN, self.position, 10)


def fire_bullet(x: int, y: int, dir: Direction, zombies: set[Zombie], damage: int):
    if dir == Direction.LEFT:
        x -= 8
    elif dir == Direction.RIGHT:
        x += 8
    elif dir == Direction.DOWN:
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
