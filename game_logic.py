# create the classes for zombies/player/bullet
import config
import pygame
import math

RED = (255, 0, 0) # temp color
YELLOW = (255,255,0)

import pygame

# helper functions
def find_mouse_coords():
    '''
    Calculates the coordinates of the mouse with respect to the 
    center of the screen (player position). The coordinates are
    in terms of the cartesian plane
    '''
    mouse_x, mouse_y = pygame.mouse.get_pos()
    center_x, center_y = config.WIDTH // 2, config.HEIGHT //2

    mouse_x = mouse_x - center_x
    mouse_y = -(mouse_y - center_y) #flip so it behaves like cartesian plane

    return (mouse_x, mouse_y)

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
    _facing: pygame.Rect

    def __init__(self, bullets: int, position: pygame.Rect):
        self._life = 100
        self._num_bullets = bullets
        self._curr_bullets = []
        self._position = position
        self._direction = "right"

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
        mouse_x, mouse_y = find_mouse_coords()

        theta = math.atan2(mouse_y, mouse_x)
        theta = math.degrees(theta)
        if (-45 <= theta <= 45):
            self._direction = "right"
        
        elif (45 < theta <= 135):
            self._direction = "up" 
        
        elif (theta > 135 or -180 <= theta <= -135):
            self._direction = "left"
        
        elif (-135 < theta < -45):
            self._direction = "down"

    # METHODS
    def fire(self):
        self.bullets -= 1
        bullet = Bullet(self.position)
        self._curr_bullets.append(bullet)

    # DRAW METHODS
    def draw(self, SCREEN):
        self.set_direction()
        pygame.draw.rect(SCREEN, RED, self.position, 10)


class Bullet:
    '''
    Class representing a bullet

    Attributes:
        - Position [pygame.rect] 
    '''
    _position: pygame.Rect

    def __init__(self, player_pos: pygame.Rect, dir: pygame.rect):
        self._position = player_pos

    @property 
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position: pygame.Rect):
        self._position = new_position

    
    # METHODS
    def update_bullet(self):
        pass