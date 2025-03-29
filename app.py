import pygame

import map

# Tile map with walls represented by 'W' and empty spaces by '.'
test_map = [
    "..W..W",
    ".W...W",
    ".W...W"
]

WIDTH = 960
HEIGHT = 640

TILE_SIZE = 64
screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
black = (0, 0, 0)

test = map.Map(test_map, TILE_SIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(black)
    for tile in test.tiles:
        tile.draw(screen, TILE_SIZE)
    pygame.display.flip()


pygame.quit()