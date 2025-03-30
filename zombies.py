import config
import math
import pygame

GREEN = (0, 0, 255)
class Zombie:
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
    
    def set_direction(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x, center_y = config.WIDTH // 2, config.HEIGHT //2

        mouse_x = mouse_x - center_x
        mouse_y = -(mouse_y - center_y) #flip so it behaves like cartesian plane

        theta = math.atan2(mouse_y, mouse_x)
        theta = math.degrees(theta)
        if (0 <= theta <= 45 and 315 < theta < 360):
            self._direction = "right"
        
        elif (45 < theta <= 135):
            self._direction = "up:" 
        
        elif (135 < theta <= 225):
            self._direction = "left"
        
        elif (225 < theta <= 315):
            self._direction = "down"
    
    def draw(self, surface: pygame.surface):
        self.set_direction()
        pygame.draw.rect(surface, GREEN, self.position, 10)
