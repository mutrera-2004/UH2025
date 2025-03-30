import pygame
import config
import math

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
        self._direction = config.Direction.RIGHT
        self._theta = 0

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, new_health: int):
        self._life = max(0, min(new_health, 100))

    @property
    def bullets(self):
        return self._num_bullets

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
        mouse_x, mouse_y = config.find_mouse_coords()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x, center_y = config.WIDTH // 2, config.HEIGHT // 2

        mouse_x = mouse_x - center_x
        mouse_y = -(mouse_y - center_y)  # flip so it behaves like cartesian plane

        theta = math.atan2(mouse_y, mouse_x)
        self._theta = math.degrees(theta)
        if -45 <= theta <= 45:
            self._direction = config.Direction.RIGHT

        elif 45 < theta <= 135:
            self._direction = config.Direction.UP

        elif theta > 135 or -180 <= theta <= -135:
            self._direction = config.Direction.LEFT

        elif -135 < theta < -45:
            self._direction = config.Direction.DOWN
    
    @property
    def theta(self):
        return self._theta
    
    def draw(self, screen):
        self.set_direction()
        pygame.draw.rect(screen, (255, 0, 0), self.position, 10)

