import config
import math
import pygame
from player import Player
import os

GREEN = (0, 0, 255)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, damage: int, position: tuple[int, int], groups: pygame.sprite.Group):
        super().__init__(groups)
        self._health = 100
        self._damage = damage
        self._direction = config.Direction.RIGHT
        self._position = position
        # Update collision rectangle to match sprite size (1.5x tile size)
        self._rect = pygame.rect.Rect((0, 0), (int(config.TILE_SIZE * 1.5), int(config.TILE_SIZE * 1.5)))
        self._rect.center = position
        self.previous_time = pygame.time.get_ticks()
        self._animation_frame = 0
        self._animation_timer = 0
        self._moving = False
        self._load_sprites()
        self.movement_timer = pygame.time.get_ticks()

    def _load_sprites(self):
        """Load all animation sprites for the zombie."""
        sprite_path = "sprites"
        self._sprites = {
            config.Direction.RIGHT: [],
            config.Direction.LEFT: [],
            config.Direction.UP: [],
            config.Direction.DOWN: []
        }
        
        try:
            # Load right direction sprites
            self._sprites[config.Direction.RIGHT].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Right.png")))
            self._sprites[config.Direction.RIGHT].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Right_Motion_1.png")))
            self._sprites[config.Direction.RIGHT].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Right.png")))
            
            # Load left direction sprites
            self._sprites[config.Direction.LEFT].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Left.png")))
            self._sprites[config.Direction.LEFT].append(pygame.image.load(os.path.join(sprite_path, "Zombie_left_Motion_1.png")))
            self._sprites[config.Direction.LEFT].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Left.png")))
            
            # Load up direction sprites
            self._sprites[config.Direction.UP].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Up.png")))
            self._sprites[config.Direction.UP].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Up_Motion_1.png")))
            self._sprites[config.Direction.UP].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Up_Motion_2.png")))
            
            # Load down direction sprites
            self._sprites[config.Direction.DOWN].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Front.png")))
            self._sprites[config.Direction.DOWN].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Front_Motion_1.png")))
            self._sprites[config.Direction.DOWN].append(pygame.image.load(os.path.join(sprite_path, "Zombie_Front_Motion_2.png")))
            
            # Scale all sprites to 1.5x tile size
            scaled_size = (int(config.TILE_SIZE * 1.5), int(config.TILE_SIZE * 1.5))
            for direction in self._sprites:
                for i in range(len(self._sprites[direction])):
                    self._sprites[direction][i] = pygame.transform.scale(self._sprites[direction][i], scaled_size)
        except pygame.error as e:
            print(f"Error loading zombie sprites: {e}")
            raise

    def update_animation(self):
        """Update the animation frame based on time."""
        current_time = pygame.time.get_ticks()
        if current_time - self._animation_timer > 150:  # Change frame every 150ms
            max_frames = len(self._sprites[self._direction])
            
            if self._moving and max_frames > 1:
                self._animation_frame = (self._animation_frame + 1) % max_frames
            else:
                self._animation_frame = 0
            self._animation_timer = current_time

    def draw(self, screen):
        self.update_animation()
        try:
            if self._animation_frame < len(self._sprites[self._direction]):
                self._animation_frame = self._animation_frame % len(self._sprites[self._direction])
            current_sprite = self._sprites[self._direction][self._animation_frame]
            sprite_rect = current_sprite.get_rect(center=self._rect.center)
            screen.blit(current_sprite, sprite_rect)
        except IndexError:
            print(f"Error: Tried to access frame {self._animation_frame} for direction {self._direction}")
            print(f"Available frames: {len(self._sprites[self._direction])}")
            raise

        if self._health <= 0:
            self.kill()

    def update(self, movex, movey, player: Player):
        self._rect.x = self._position[0] + movex
        self._rect.y = self._position[1] + movey

        # Update direction based on movement
        if abs(movex) > abs(movey):
            self._direction = config.Direction.RIGHT if movex > 0 else config.Direction.LEFT
        else:
            self._direction = config.Direction.DOWN if movey > 0 else config.Direction.UP
        
        self._moving = movex != 0 or movey != 0

        if self._rect.colliderect(config.PLAYER_RECT) and pygame.time.get_ticks() - self.previous_time >= 1000:
            self.previous_time = pygame.time.get_ticks()
            player._health = max(player._health - self._damage, 0)
            player.previous_time = pygame.time.get_ticks()


    def valid_move(self, new_rect, map):
        for tile in map.walls:
            if new_rect.colliderect(tile.rect):
                return False
        return True

    def move(self, map):
        zombie_center = self._rect.center
        player_center = config.PLAYER_RECT.center
        
        # Calculate movement direction
        dx = 0
        dy = 0
        move_speed = 5
        
        # Horizontal movement
        if player_center[0] < zombie_center[0]:
            dx = -move_speed
        elif player_center[0] > zombie_center[0]:
            dx = move_speed
            
        # Vertical movement    
        if player_center[1] < zombie_center[1]:
            dy = -move_speed
        elif player_center[1] > zombie_center[1]:
            dy = move_speed
        if pygame.time.get_ticks() - self.movement_timer >= 100:
            self.movement_timer = pygame.time.get_ticks()
            temp_rect = self._rect.copy()
            temp_rect.x += dx
            if self.valid_move(temp_rect, map):
                self._position = (self._position[0] + dx, self._position[1])
            else:
                temp_rect.x -= dx
            temp_rect.y += dy
            if self.valid_move(temp_rect, map):
                self._position = (self._position[0], self._position[1] + dy)
        

    
