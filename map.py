import pygame

# Tile map with walls represented by 'W' and empty spaces by '.'
test_map = [
    "WWWWWW",
    "W....W",
    "W....W"
]


class Tiles:
    def __init__(self, type: str, pos: tuple[int, int]):
        self.type = type  # Type of tile (Wall or Empty)
        self.pos = pos  # Position of the tile

    def draw(self, screen, TILE_SIZE):
        # Draw tile on the screen at the specified position
        if self.type == 'wall':
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos[0], self.pos[1], TILE_SIZE, TILE_SIZE))  # White for walls
        else:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.pos[0], self.pos[1], TILE_SIZE, TILE_SIZE))  # Black for empty space


class Map:
    def __init__(self, tile_map, TILE_SIZE):
        self.tiles = []
        for row_index, row in enumerate(tile_map):
            for col_index, tile in enumerate(row):
                tile_type = 'wall' if tile == 'W' else 'empty'  # Determine tile type
                self.tiles.append(Tiles(tile_type, (col_index * TILE_SIZE, row_index * TILE_SIZE)))



