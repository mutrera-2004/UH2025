import config
import math
import pygame
import game_logic

GREEN = (0, 0, 255)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, damage: int, position: pygame.Rect):
        self._life = 100
        self._damage = damage
        self._direction = "right"
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
    
    def draw(self, surface: pygame.surface):
        pygame.draw.rect(surface, GREEN, self.position, 10)
