import pygame
import config

# Tile map with walls represented by 'W' and empty spaces by '.'
test_map = [
    "WWWWWW",
    "W....W",
    "W....W"
]


class Tiles:
    def __init__(self, type: str, pos: tuple[int, int]):
        self.type = type  # Type of tile (Wall or Empty)
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], config.TILE_SIZE, config.TILE_SIZE)  # Position as a Rect

    def draw(self, screen):
        # Draw tile on the screen at the specified position
        if self.type == 'wall':
            pygame.draw.rect(screen, (255, 255, 255), self.rect)  # White for walls
        else:
            pygame.draw.rect(screen, (0, 0, 0), self.rect)  # Black for empty space

class Map:
    def __init__(self, tile_map):
        self.tiles = []
        self.offset_x = 0  # Horizontal offset to move the map
        self.offset_y = 0  # Vertical offset to move the map
        self.current_time = pygame.time.get_ticks()
        for row_index, row in enumerate(tile_map):
            for col_index, tile in enumerate(row):
                tile_type = 'wall' if tile == 'W' else 'empty'  # Determine tile type
                self.tiles.append(Tiles(tile_type, (col_index * config.TILE_SIZE, row_index * config.TILE_SIZE)))

    def update(self):
        # Move map with continuous scrolling while holding down the arrow keys
        movement_speed = 5  # Adjust movement speed (in pixels)

        # Check for key presses using pygame.key.get_pressed()
        keys = pygame.key.get_pressed()
        if pygame.time.get_ticks() - self.current_time >= 25:
            self.current_time = pygame.time.get_ticks()
            if keys[pygame.K_DOWN]:
                self.offset_y -= movement_speed  # Move map down (pixel-based)
            if keys[pygame.K_UP]:
                self.offset_y += movement_speed  # Move map up (pixel-based)
            if keys[pygame.K_LEFT]:
                self.offset_x += movement_speed  # Move map right (pixel-based)
            if keys[pygame.K_RIGHT]:
                self.offset_x -= movement_speed  # Move map left (pixel-based)

    def draw(self, screen):
        # Draw the tiles on the screen based on the current offset
        for tile in self.tiles:
            # Adjust tile positions using the offsets (pixel-based movement)
            tile.rect.x = tile.pos[0] + self.offset_x
            tile.rect.y = tile.pos[1] + self.offset_y
            tile.draw(screen)

