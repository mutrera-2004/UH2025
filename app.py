import pygame

import map
import game_logic
import config
from pytmx.util_pygame import load_pygame


# Tile map with walls represented by 'W' and empty spaces by '.'
pygame.init()
test_map = [
    "..W..W",
    ".W...W",
    ".W...W"
]
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))


mapp = load_pygame(r'data/UH Map.tmx')
print(mapp)

running = True
black = (0, 0, 0)


test_player = game_logic.Player(100, config.PLAYER_RECT)
test_player._position.center = (config.WIDTH // 2, config.HEIGHT // 2)
test = map.Map(mapp)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    test.update()
    screen.fill(black)
    test.draw(screen)
    test_player.draw(screen)
    print(test_player.direction)
    pygame.display.flip()


pygame.quit()