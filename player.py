import pygame
import config
import math
import os

class Player:
    """
    Class representing a Player

    Attributes:
        - health [int]: percentage of health left
        - bullets [int]: number of bullets left on the gun
        - position [pygame.Rect]: position of the object
        - sprites [dict]: dictionary containing animation sprites for each direction
        - animation_frame [int]: current frame of animation
        - animation_timer [int]: timer for animation updates
        - moving [bool]: whether the player is currently moving
    """

    _health: int
    _bullets: int
    _position: pygame.Rect
    _facing: pygame.Rect
    _sprites: dict
    _animation_frame: int
    _animation_timer: int
    _moving: bool

    def __init__(self, bullets: int, position: pygame.Rect):
        self._health = 100
        self._num_bullets = bullets
        self._position = position
        self._direction = config.Direction.RIGHT
        self._theta = 0
        self._animation_frame = 0
        self._animation_timer = 0
        self._moving = False
        self._load_sprites()

    def _load_sprites(self):
        """Load all animation sprites for the player."""
        sprite_path = "sprites"
        self._sprites = {
            config.Direction.RIGHT: [],
            config.Direction.LEFT: [],
            config.Direction.UP: [],
            config.Direction.DOWN: []
        }
        
        try:
            # Load right direction sprites
            self._sprites[config.Direction.RIGHT].append(pygame.image.load(os.path.join(sprite_path, "Hero_Right.png")))
            self._sprites[config.Direction.RIGHT].append(pygame.image.load(os.path.join(sprite_path, "Hero_Right_Motion_1.png")))
            
            # Load left direction sprites
            self._sprites[config.Direction.LEFT].append(pygame.image.load(os.path.join(sprite_path, "Hero_Left.png")))
            self._sprites[config.Direction.LEFT].append(pygame.image.load(os.path.join(sprite_path, "Hero_Left_Motion_1.png")))
            
            # Load up direction sprites
            self._sprites[config.Direction.UP].append(pygame.image.load(os.path.join(sprite_path, "Hero_Up.png")))
            self._sprites[config.Direction.UP].append(pygame.image.load(os.path.join(sprite_path, "Hero_Up_Motion_1.png")))
            self._sprites[config.Direction.UP].append(pygame.image.load(os.path.join(sprite_path, "Hero_Up_Motion_2.png")))
            
            # Load down direction sprites
            self._sprites[config.Direction.DOWN].append(pygame.image.load(os.path.join(sprite_path, "Hero_Down.png")))
            self._sprites[config.Direction.DOWN].append(pygame.image.load(os.path.join(sprite_path, "Hero_Down_motion_1.png")))  # Note the lowercase 'm'
            self._sprites[config.Direction.DOWN].append(pygame.image.load(os.path.join(sprite_path, "Hero_Down_Motion_2.png")))
            
            # Scale all sprites to 1.5x tile size
            scaled_size = (int(config.TILE_SIZE * 1.5), int(config.TILE_SIZE * 1.5))
            for direction in self._sprites:
                for i in range(len(self._sprites[direction])):
                    self._sprites[direction][i] = pygame.transform.scale(self._sprites[direction][i], scaled_size)
        except pygame.error as e:
            print(f"Error loading sprites: {e}")
            raise

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health: int):
        self._health = max(0, min(new_health, 100))

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
        """Update direction based on keyboard input and mouse position."""
        keys = pygame.key.get_pressed()
        self._moving = False
        old_direction = self._direction
        
        # Handle keyboard movement
        if keys[pygame.K_w]:
            self._direction = config.Direction.UP
            self._moving = True
        elif keys[pygame.K_s]:
            self._direction = config.Direction.DOWN
            self._moving = True
        elif keys[pygame.K_a]:
            self._direction = config.Direction.LEFT
            self._moving = True
        elif keys[pygame.K_d]:
            self._direction = config.Direction.RIGHT
            self._moving = True
        
        # If not moving with keyboard, use mouse position for direction
        if not self._moving:
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
        
        # Reset animation frame when changing directions
        if old_direction != self._direction:
            self._animation_frame = 0
    
    @property
    def theta(self):
        return self._theta

    def update_animation(self):
        """Update the animation frame based on time."""
        current_time = pygame.time.get_ticks()
        if current_time - self._animation_timer > 150:  # Change frame every 150ms
            max_frames = len(self._sprites[self._direction])
            print(f"Direction: {self._direction}, Max frames: {max_frames}, Current frame: {self._animation_frame}, Moving: {self._moving}")
            
            if self._moving and max_frames > 1:
                # When moving and we have animation frames, cycle through them
                self._animation_frame = (self._animation_frame + 1) % max_frames
            else:
                # When standing still or no animation frames, use the first frame
                self._animation_frame = 0
            self._animation_timer = current_time
            print(f"New frame: {self._animation_frame}")
    
    def draw(self, screen):
        self.set_direction()
        self.update_animation()
        
        # Get the current sprite for the current direction and frame
        try:
            current_sprite = self._sprites[self._direction][self._animation_frame]
            # Draw the sprite centered on the player's position
            sprite_rect = current_sprite.get_rect(center=self._position.center)
            screen.blit(current_sprite, sprite_rect)
        except IndexError:
            print(f"Error: Tried to access frame {self._animation_frame} for direction {self._direction}")
            print(f"Available frames: {len(self._sprites[self._direction])}")
            raise

