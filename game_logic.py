# create the classes for zombies/player/bullet

RED = (255, 0, 0) # temp color
YELLOW = (255,255,0)

import pygame

class Game:
    '''
    Class representing the Game

    Attributes:
        - game_over [bool]: whether the game is over or not depending
            on the player's health
        - player [Player]: player
        - Zombies [list[Zombie]]: list of existing zombies in the map
    '''
    _game_over = bool

    def __init__(self):
        self._game_over = False

    @property
    def game_over(self):
        return self._game_over


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
        self._num_bullets = bullets
        self._curr_bullets = []
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

    # METHODS
    def fire(self):
        self.bullets -= 1
        bullet = Bullet(self.position)
        self._curr_bullets.append(bullet)

    # DRAW METHODS
    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, RED, self.position, 10)
    


import pygame

class Zombie(pygame.sprite.Sprite):
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

    def __init__(self, player_pos: pygame.Rect, speed: int):
        self._position = player_pos

    @property 
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position: pygame.Rect):
        self._position = new_position

    
    # METHODS
    def update_bullet(self):
        if nor 
        self.position = 
