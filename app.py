import pygame

import map
from game_logic import Player, fire_bullet, Zombie
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

running = True
black = (0, 0, 0)


player = Player(100, config.PLAYER_RECT)
player._position.center = (config.WIDTH // 2, config.HEIGHT // 2)
test = map.Map(mapp)
test_zombie = Zombie(30, config.ZOMBIE_RECT)
zombies: set[Zombie] = set()
zombies.add(test_zombie)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        elif pygame.key.get_pressed()[pygame.MOUSEBUTTONDOWN]:
            player.bullets -= 1
            bullet_x, bullet_y = player.position.center
            while bullet_x < config.WIDTH and bullet_y < config.HEIGHT:
                fire_bullet(bullet_x, bullet_y, player.direction, zombies)
    test.update()
    screen.fill(black)
    test.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), player.position, 10)
    for zombie in zombies:
        zombie.draw(screen)
    pygame.display.flip()


pygame.quit()