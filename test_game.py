import random
import pygame
from pygame import mixer
import map
from player import Player 
from bullet import Bullet
from zombies import Zombie
import config
from game import Game
from pytmx.util_pygame import load_pygame
import os


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
AI_GF_DEST = 0
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
    # if curr_wave > 1:
    #     gf_glow = config.glow.get_rect(center=AI_GF_DEST)
    #     dark_surface.blit(config.glow, gf_glow)
    glow_rect = config.glow.get_rect(center=config.PLAYER_RECT.center)
    dark_surface.blit(config.glow, glow_rect)
    screen.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

def draw_final_message():
    """Draws the final message sprite at the bottom of the screen."""
    # Load the sprite from the "sprites" folder
    sprite_path = os.path.join("sprites", "HELP.png")
    final_message = pygame.image.load(sprite_path).convert_alpha()
   
    # Get the screen dimensions
    screen_width, screen_height = screen.get_size()
   
    # Scale the sprite to match the screen width and desired height
    final_message = pygame.transform.scale(final_message, (screen_width, 150))
   
    # Position the sprite at the bottom of the screen
    sprite_rect = final_message.get_rect(midbottom=(screen_width // 2, screen_height))
   
    # Draw the sprite on the screen
    screen.blit(final_message, sprite_rect)


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


def spawn_zombie(num_zombies: int, groups: pygame.sprite.Group):
    zombie_counter = num_zombies
    while (zombie_counter > 0):
        tile_num = random.randint(0, len(test.walkable) - 1)
        tile = test.walkable[tile_num]
        # tile.rect.x = tile.pos[0] + test.offset_x
        # tile.rect.y = tile.pos[1] + test.offset_y
        zombie_rect = pygame.rect.Rect((0, 0), (int(config.TILE_SIZE * 1.5), int(config.TILE_SIZE * 1.5)))
        zombie_rect.center = tile.rect.center
        valid_placing = True
        if config.distance(zombie_rect.center, config.PLAYER_RECT.center) <= 450:
            continue
        for wall in test.walls:
            if wall.rect.colliderect(zombie_rect):
                valid_placing = False
                break
        if not valid_placing:
            continue
        zombie = Zombie(30, zombie_rect.center, groups)
        zombie_counter -= 1

AI_GF_DEST = config.PLAYER_RECT.center
rrect = None
TOUCH = False

def draw_ai(AI_GF_DEST, touch):
    global rrect
    x = AI_GF_DEST[0] + test.offset_x
    y = AI_GF_DEST[1] + test.offset_y
    rrect = pygame.rect.Rect((x, y), (config.TILE_SIZE * 1.5, config.TILE_SIZE * 1.5))
    if not touch:
        AI_GF_IMAGE = pygame.image.load("sprites/AI_GF.png")
    else:
        AI_GF_IMAGE = pygame.image.load("sprites/AI_GF_YAYYYY.png")
    scaled_size = (int(config.TILE_SIZE * 1.5), int(config.TILE_SIZE * 1.5))
    AI_GF_IMAGE = pygame.transform.scale(AI_GF_IMAGE, scaled_size)
    screen.blit(AI_GF_IMAGE, rrect)




mixer.init()
sound1 = mixer.Sound("./audio/background.mp3")
sound2 = mixer.Sound("./audio/zombie.mp3")
sound3 = mixer.Sound("./audio/shotgun.mp3")

channel1 = mixer.Channel(0)
channel2 = mixer.Channel(1)
channel3 = mixer.Channel(2)

channel1.play(sound1, -1)
channel2.play(sound2, -1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() - previous_time >= 1000 and not TOUCH:
            previous_time = pygame.time.get_ticks()
            player.bullets -= 1
            bullets.add(Bullet(player.theta, zombies, test.walls, bullets))
            mixer.init()
            mixer.music.load("./audio/shotgun.mp3")
            mixer.music.play()
    
    if new_wave:
        spawn_zombie(zombies_per_wave[curr_wave], zombies)
        new_wave = False


    if not TOUCH:
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
        zombie.move(test)
    
    zombie_healthbars(zombies)
    if curr_wave > 1:
        if config.PLAYER_RECT.colliderect(rrect):
            TOUCH = True
            draw_ai(AI_GF_DEST, True)
        else:
            draw_ai(AI_GF_DEST, False)
    if not TOUCH:
        generate_fog()
    player_healthbar()
    if not zombies:
        curr_wave += 1
        if curr_wave > 1:
            draw_final_message()
            player._health = 100
            draw_ai(AI_GF_DEST, False)
            test.good_ending = True
            sound2.stop()
            sound1.stop()
        
    pygame.display.flip()
