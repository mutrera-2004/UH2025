import pygame

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
    _current_tile: Tiles

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