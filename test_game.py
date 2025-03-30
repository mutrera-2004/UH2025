import pygame
import map
from player import Player 
from bullet import Bullet
import config
from game import Game
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
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()
test_game = Game(test, player)
test_game.spawn_zombie(10, zombies)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.bullets -= 1
            bullets.add(Bullet(player.theta, zombies, test.walls, bullets))
            
    test.update()
    screen.fill(black)
    test.draw(screen)
    player.draw(screen)
    for bullet in bullets:
        bullet.update()
        bullet.draw(screen)

    for zombie in zombies:
        zombie.draw(screen)
        
    pygame.display.flip()


pygame.quit()