import pygame
import math
import config

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle: int, zombies: set, walls, groups):
        super().__init__(groups)
        self.pos = config.PLAYER_RECT.center
        self.rect = pygame.rect.Rect(self.pos, (20, 20))
        self.angle = angle
        self.speed = 16
        self.damage = 100
        angle = math.radians(angle)
        self.movex = self.speed * math.cos(angle)
        self.movey = self.speed * math.sin(angle)
        self.zombies = zombies
        self.walls = walls

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

    def update(self):
        self.rect.move_ip((self.movex, -self.movey))
        # performence may be a lil slow
        for zombie in self.zombies:
            if zombie._rect.colliderect(self.rect):
                zombie._health -= self.damage
                self.kill()
        for wall in self.walls:
            if wall.rect.colliderect(self.rect):
                self.kill()
