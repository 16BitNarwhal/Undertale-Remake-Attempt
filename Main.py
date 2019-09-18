import pygame

import settings as s
import player

# initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((s.SCREENWIDTH, s.SCREENHEIGHT))
pygame.display.set_caption("Undersea")
clock = pygame.time.Clock()

# game loop
running = True
while running:
    # keep loop running at same speed
    clock.tick(s.FPS)

    # process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # update
    pygame.display.update()

    # draw/render
    screen.fill(s.BLACK)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
quit()