import pygame
import map
from player import Player 
from bullet import Bullet
from zombies import Zombie
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

curr_wave = 1
new_wave = True
zombies_per_wave = [0, 10, 20, 30] # number of zombies that are spawned per wave and 3 waves only NOT 0 index
player = Player(100, config.PLAYER_RECT)
player._position.center = (config.WIDTH // 2, config.HEIGHT // 2)
test = map.Map(mapp)
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()
# test_game = Game(test, player)
# test_game.spawn_zombie()
previous_time = pygame.time.get_ticks()

test_game = Game(test, player)

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

def move_zombie(zombie: Zombie):
    zombie_center = zombie._rect.center
    player_center = config.PLAYER_RECT.center
    
    # Calculate movement direction
    dx = 0
    dy = 0
    move_speed = 2
    
    # Horizontal movement
    if player_center[0] < zombie_center[0]:
        dx = -move_speed
    elif player_center[0] > zombie_center[0]:
        dx = move_speed
        
    # Vertical movement    
    if player_center[1] < zombie_center[1]:
        dy = -move_speed
    elif player_center[1] > zombie_center[1]:
        dy = move_speed
        
    # Check wall collisions before moving
    test_rect = zombie._rect.copy()
    test_rect.x += dx
    test_rect.y += dy
    
    # Only move if won't hit a wall
    can_move_x = True
    can_move_y = True
    for wall in test.walls:
        if test_rect.colliderect(wall.rect):
            if dx != 0:
                can_move_x = False
            if dy != 0:
                can_move_y = False
                
    # Apply valid movements
    if can_move_x:
        zombie._position = (zombie._position[0] + dx, zombie._position[1])
    if can_move_y:
        zombie._position = (zombie._position[0], zombie._position[1] + dy)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() - previous_time >= 1000:
            previous_time = pygame.time.get_ticks()
            player.bullets -= 1
            bullets.add(Bullet(player.theta, zombies, test.walls, bullets))
    
    if new_wave:
        test_game.spawn_zombie(zombies_per_wave[curr_wave], zombies)
        new_wave = False

    if not zombies:
        curr_wave += 1
        new_wave = True
        if curr_wave > 3:
            test.good_ending = True

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
    
    zombie_healthbars(zombies)
    generate_fog()
    player_healthbar()
        
    pygame.display.flip()
