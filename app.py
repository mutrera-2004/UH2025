import pygame

import pygame
screen = pygame.display.set_mode((950, 950))

running = True
black = (0, 0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(black)
    pygame.display.flip()

pygame.quit()