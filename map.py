import pygame
import config
import pytmx

# Tile map with walls represented by 'W' and empty spaces by '.'
test_map = [
    "WWWWWW",
    "W....W",
    "W....W"
]


def generate_glow(glow, radius):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    layers = 20
    glow = pygame.math.clamp(glow, 0, 200)
    for i in range(layers):
        k = i * glow
        k = pygame.math.clamp(k, 0, 200)
        pygame.draw.circle(surf, (k, k, k), surf.get_rect().center, radius - i * 3)
    
    return surf

glow = generate_glow(15, config.TILE_SIZE * 3)

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
        self.walkable = []
        self.offset_x = 0  # Horizontal offset to move the map
        self.offset_y = 0  # Vertical offset to move the map
        self.current_time = pygame.time.get_ticks()
        self.tmx_data = tile_map
        # Loop through layers and scale tiles
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    wall_flag = self.is_wall(x, y)
                    if tile_image:
                        tile = Tiles(None, tile_image, (x * config.TILE_SIZE, y * config.TILE_SIZE))
                        self.tiles.append(tile)
                        if wall_flag:
                            self.walls.append(tile)
                        else:
                            self.walkable.append(tile)

    def is_wall(self, x, y):
        layer_index = 1  # Layer 2 in Tiled is index 1 (0-based index)
        layer = self.tmx_data.layers[layer_index]
        
        if isinstance(layer, pytmx.TiledTileLayer):
            gid = layer.data[y][x] 
            return gid != 0  # If GID exists, it's a wall
        
        return False

    def valid(self, new_rect):
        for tile in self.walls:
            if new_rect.colliderect(tile.rect):
                return False
        return True
    
    def update(self):
        # Move map with continuous scrolling while holding down the arrow keys
        movement_speed = 5  # Adjust movement speed (in pixels)
        keys = pygame.key.get_pressed()  # Get pressed keys
        
        # Current player position (assuming PLAYER_RECT is defined in config)
        player_rect = config.PLAYER_RECT  # The player's current rectangle
        
        # Checking for key presses and updating the map offset
        if pygame.time.get_ticks() - self.current_time >= 25:
            self.current_time = pygame.time.get_ticks()
            
            # Temporary rectangles to check for collisions
            temp_rect = player_rect.copy()

            if keys[pygame.K_DOWN]:
                temp_rect.y += movement_speed  # Move player down
                if self.valid(temp_rect):  # Check if new position is valid
                    self.offset_y -= movement_speed  # Move map down (pixel-based)
                else:
                    temp_rect.y -= movement_speed
            
            if keys[pygame.K_UP]:
                temp_rect.y -= movement_speed  # Move player up
                if self.valid(temp_rect):  # Check if new position is valid
                    self.offset_y += movement_speed  # Move map up (pixel-based)
                else:
                    temp_rect.y += movement_speed
            
            if keys[pygame.K_LEFT]:
                temp_rect.x -= movement_speed  # Move player left
                if self.valid(temp_rect):  # Check if new position is valid
                    self.offset_x += movement_speed  # Move map right (pixel-based)
                else:
                    temp_rect.x += movement_speed
            
            if keys[pygame.K_RIGHT]:
                temp_rect.x += movement_speed  # Move player right
                if self.valid(temp_rect):  # Check if new position is valid
                    self.offset_x -= movement_speed  # Move map left (pixel-based)
                else:
                    temp_rect.x -= movement_speed

    def draw(self, screen):
        for tile in self.tiles:
            tile.rect.x = tile.pos[0] + self.offset_x
            tile.rect.y = tile.pos[1] + self.offset_y
            tile.draw(screen)
            #pygame.draw.rect(screen, (255,0,0), tile.rect, 2)
        dark_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
        dark_surface.fill((0, 0, 0))
        # dark_surface.set_alpha(180)
        glow_rect = glow.get_rect(center=config.PLAYER_RECT.center)
        dark_surface.blit(glow, glow_rect)
        screen.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
