import config
import math
import pygame

GREEN = (0, 0, 255)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, damage: int, position: tuple[int, int], groups: pygame.sprite.Group):
        super().__init__(groups)
        self._life = 100
        self._damage = damage
        self._direction = "right"
        self._position = position
        self._rect = pygame.rect.Rect((0, 0), (48, 48))
        self._rect.center = position

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self._rect, 10)
