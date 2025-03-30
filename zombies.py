import config
import math
import pygame

GREEN = (0, 0, 255)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, damage: int, position: pygame.Rect, groups: pygame.sprite.Group):
        super().__init__(groups)
        self._life = 100
        self._damage = damage
        self._direction = "right"
        self._position = position

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self._position, 10)
