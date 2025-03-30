import random
import pygame
from pygame import mixer
import map
import os
from player import Player 
from bullet import Bullet
from zombies import Zombie
import config
from game import Game
from pytmx.util_pygame import load_pygame


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
previous_time = pygame.time.get_ticks()

while pygame.time.get_ticks() - previous_time <= 300:
    continue

previous_time = pygame.time.get_ticks()

def generate_fog():
    dark_surface = pygame.Surface((config.WIDTH, config.HEIGHT))
    if pygame.time.get_ticks() - player.previous_time <= 250 or player.health <= 30:
        dark_surface.fill((255, 0, 0))
    else:
        dark_surface.fill((0, 0, 0))
    # dark_surface.set_alpha(180)
    glow_rect = config.glow.get_rect(center=config.PLAYER_RECT.center)
    dark_surface.blit(config.glow, glow_rect)
    screen.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

def zombie_healthbars(zombies):
    for zombie in zombies:
        # Draw health bars for zombies
        health_bar_width = 40
        health_bar_height = 6
        health_bar_pos = (zombie._rect.centerx - health_bar_width//2, zombie._rect.bottom + 5)
        
        # Background/empty bar (red)
        pygame.draw.rect(screen, (255, 0, 0),
                        (health_bar_pos[0], health_bar_pos[1], health_bar_width, health_bar_height))
        
        # Filled portion of health bar (green) 
        health_percentage = zombie._health / 100
        current_health_width = health_bar_width * health_percentage
        pygame.draw.rect(screen, (0, 255, 0),
                        (health_bar_pos[0], health_bar_pos[1], current_health_width, health_bar_height))
        

def draw_final_message():
    """Draws the final message sprite at the bottom of the screen."""
    # Load the sprite from the "sprites" folder
    sprite_path = os.path.join("sprites", "HELP.png")
    final_message = pygame.image.load(sprite_path).convert_alpha()
    
    # Get the screen dimensions
    screen_width, screen_height = screen.get_size()
    final_message = pygame.transform.scale(final_message, (screen_width, 150))
    sprite_rect = final_message.get_rect(midbottom=(screen_width // 2, screen_height))
    
    # Draw the sprite on the screen
    screen.blit(final_message, sprite_rect)


def player_healthbar():
    # Draw health bar in top left corner
    health_bar_width = 300
    health_bar_height = 8
    health_bar_pos = (10, 10)  # Fixed position in top left
    
    # Background/empty bar (red)
    pygame.draw.rect(screen, (255, 0, 0), 
                    (health_bar_pos[0], health_bar_pos[1], health_bar_width, health_bar_height))
    
    # Filled portion of health bar (green)
    health_percentage = player.health / 100
    current_health_width = health_bar_width * health_percentage
    pygame.draw.rect(screen, (0, 255, 0),
                    (health_bar_pos[0], health_bar_pos[1], current_health_width, health_bar_height))
    
    # Draw percentage text
    font = pygame.font.Font(None, 24)
    percentage_text = font.render(f"{round(health_percentage * 100)}%", True, (255, 255, 255))
    screen.blit(percentage_text, (health_bar_pos[0] + health_bar_width + 5, health_bar_pos[1]))


def spawn_zombie(num_zombies: int, groups: pygame.sprite.Group):
    zombie_counter = num_zombies
    while (zombie_counter > 0):
        tile_num = random.randint(0, len(test.walkable) - 1)
        tile = test.walkable[tile_num]
        # tile.rect.x = tile.pos[0] + test.offset_x
        # tile.rect.y = tile.pos[1] + test.offset_y
        zombie_rect = pygame.rect.Rect(tile.rect.topleft, (int(config.TILE_SIZE * 1.5), int(config.TILE_SIZE * 1.5)))
        #zombie_rect.center = tile.rect.center
        print(config.PLAYER_RECT.center)
        valid_placing = True
        if config.distance(zombie_rect.center, config.PLAYER_RECT.center) <= 250:
            continue
        for wall in test.walls:
            if wall.rect.colliderect(zombie_rect):
                valid_placing = False
                break
        if not valid_placing:
            continue
        zombie = Zombie(30, zombie_rect.center, groups)
        zombie_counter -= 1


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() - previous_time >= 1000:
            previous_time = pygame.time.get_ticks()
            player.bullets -= 1
            bullets.add(Bullet(player.theta, zombies, test.walls, bullets))
            mixer.init()
            mixer.music.load("./audio/shotgun.mp3")
            mixer.music.play()

    if not zombies:
        test_game.good_ending = True

    test.update()
    screen.fill(black)
    test.draw(screen)
    for tile in test.walkable:
        print(tile.rect.center)
    player.draw(screen)
    for bullet in bullets:
        bullet.update()
        bullet.draw(screen)

    for zombie in zombies:
        zombie.draw(screen)
        zombie.update(test.offset_x, test.offset_y, player)
        zombie.move(test)
    
    zombie_healthbars(zombies)
    generate_fog()
    player_healthbar()
    if test_game.good_ending:
        draw_final_message()
        
    pygame.display.flip()
