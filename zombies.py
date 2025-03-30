import config
import math
import pygame
from player import Player

GREEN = (0, 0, 255)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, damage: int, position: tuple[int, int], groups: pygame.sprite.Group):
        super().__init__(groups)
        self._health = 100
        self._damage = damage
        self._direction = "right"
        self._position = position
        self._rect = pygame.rect.Rect((0, 0), (48, 48))
        self._rect.center = position
        self.previous_time = pygame.time.get_ticks()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self._rect, 10)
        if self._health <= 0:
            self.kill()

    def update(self, movex, movey, player: Player):
        self._rect.x = self._position[0] + movex
        self._rect.y = self._position[1] + movey

        if self._rect.colliderect(config.PLAYER_RECT) and pygame.time.get_ticks() - self.previous_time >= 1000:
            self.previous_time = pygame.time.get_ticks()
            player._health = max(player._health - self._damage, 0)
    
