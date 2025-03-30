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
# test_game = Game(test, player)
# test_game.spawn_zombie()
previous_time = pygame.time.get_ticks()

test_game = Game(test, player)
test_game.spawn_zombie(10, zombies)

def generate_fog():
    dark_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
    dark_surface.fill((0, 0, 0))
    # dark_surface.set_alpha(180)
    glow_rect = config.glow.get_rect(center=config.PLAYER_RECT.center)
    dark_surface.blit(config.glow, glow_rect)
    screen.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() - previous_time >= 1000:
            previous_time = pygame.time.get_ticks()
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
        zombie.update(test.offset_x, test.offset_y, player)
    
    print(player._health)

    generate_fog()
        
    pygame.display.flip()


pygame.quit()