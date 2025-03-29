# create the classes for zombies/player/bullet
# temp color

RED = (255, 0, 0)

import pygame

class Player:
    '''
    Class representing a Player

    Attributes:
        - life [int]: percentage of health left
        - bullets [int]: number of bullets left on the gun
        - position [pygame.Rect]: position of the object
    '''
    _life: int
    _bullets: int
    _position: pygame.Rect

    def __init__(self, bullets: int, position: pygame.Rect):
        self._life = 100
        self._bullets = bullets
        self._position = position

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


    # DRAW METHODS
    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, RED, self.position, 10)
    


import pygame

class Zombie:
    '''
    Class representing a Zombie

    Attributes:
        - Life [int]: percentage of health remaining
        - Position [pygame.Rect]: position of the zombie
        - Damage [int]: amount of damage the zombie does
    '''
    _life: int
    _position: pygame.Rect
    _damage: int

    def __init__(self, damage: int, position: pygame.Rect):
        self._life = 100
        self._damage = damage
        self._position = position

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value: int):
        self._life = max(0, value) 

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: pygame.Rect):
        self._position = value

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value: int):
        self._damage = max(0, value)

class Bullet:
    '''
    Class representing a bullet

    Attributes:
        - Position [pygame.rect] 
    '''
    _position: pygame.Rect

    def __init__(self, player_pos: pygame.Rect):
        self._position = player_pos

    @property 
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position: pygame.Rect):
        self._position = new_position
