import pygame
import config
import pytmx

# Tile map with walls represented by 'W' and empty spaces by '.'
test_map = [
    "WWWWWW",
    "W....W",
    "W....W"
]


class Tiles:
    def __init__(self, type: str, tile_image, pos: tuple[int, int]):
        self.type = type  # Type of tile (Wall or Empty)
        if tile_image:
            self.image = pygame.transform.scale(tile_image, (config.TILE_SIZE, config.TILE_SIZE))  # Resize tile image
        else:
            self.image = None  # Empty tile case
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], config.TILE_SIZE, config.TILE_SIZE)  # Position as a Rect

    def draw(self, screen):
        # Draw tile on the screen at the specified position
        if self.image:  # Ensure tile has an image
            screen.blit(self.image, (self.rect.x, self.rect.y))

class Map:
    def __init__(self, tile_map):
        self.tiles = []
        self.walls = []
        self.offset_x = 0  # Horizontal offset to move the map
        self.offset_y = 0  # Vertical offset to move the map
        self.current_time = pygame.time.get_ticks()
        self.tmx_data = tile_map
        # Loop through layers and scale tiles
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        tile = Tiles(None, tile_image, (x * config.TILE_SIZE, y * config.TILE_SIZE))
                        self.tiles.append(tile)

    def valid(self):
        for wall in self.walls:
            if wall.rect.colliderect(config.PLAYER_RECT):
                return False
        return True

    def update(self):
        # Move map with continuous scrolling while holding down the arrow keys
        movement_speed = 5  # Adjust movement speed (in pixels)

        # Check for key presses using pygame.key.get_pressed()
        keys = pygame.key.get_pressed()
        if pygame.time.get_ticks() - self.current_time >= 25:
            self.current_time = pygame.time.get_ticks()
            if self.valid():
                if keys[pygame.K_DOWN]:
                    self.offset_y -= movement_speed  # Move map down (pixel-based)
                if keys[pygame.K_UP]:
                    self.offset_y += movement_speed  # Move map up (pixel-based)
                if keys[pygame.K_LEFT]:
                    self.offset_x += movement_speed  # Move map right (pixel-based)
                if keys[pygame.K_RIGHT]:
                    self.offset_x -= movement_speed  # Move map left (pixel-based)

    def draw(self, screen):
        for tile in self.tiles:
            tile.rect.x = tile.pos[0] + self.offset_x
            tile.rect.y = tile.pos[1] + self.offset_y
            tile.draw(screen)

