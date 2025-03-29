import pygame

import map
import game_logic

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


test_player = game_logic.Player(100, pygame.rect.Rect(WIDTH // 2, HEIGHT // 2, TILE_SIZE, TILE_SIZE))
test = map.Map(test_map, TILE_SIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    test.update(event)
    screen.fill(black)
    test.draw(screen, WIDTH, HEIGHT, TILE_SIZE)
    test_player.draw(screen)
    pygame.display.flip()


pygame.quit()