import pygame

import map
import game_logic
import config
from pytmx.util_pygame import load_pygame


# map = load_pygame(r'data/UH Map.tmx')
# print(map)


# Tile map with walls represented by 'W' and empty spaces by '.'
pygame.init()
test_map = [
    "..W..W",
    ".W...W",
    ".W...W"
]
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

running = True
black = (0, 0, 0)


test_player = game_logic.Player(100, pygame.rect.Rect(0, 0, config.TILE_SIZE, config.TILE_SIZE))
test_player._position.center = (config.WIDTH // 2, config.HEIGHT // 2)
test = map.Map(test_map)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    test.update()
    screen.fill(black)
    test.draw(screen)
    test_player.draw(screen)
    pygame.display.flip()


pygame.quit()