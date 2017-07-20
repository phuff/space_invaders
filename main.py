import pygame
import os

# Special code to center window
os.environ['SDL_VIDEO_CENTERED'] = '1'
FRAMES_PER_SECOND = 30
RESOLUTION = WIDTH, HEGIHT = 800, 600
WINDOWS_TITLE = 'Space Invaders v1.0'


def setup():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption(WINDOWS_TITLE)
    return screen, False, pygame.time.Clock()


def main():
    # Configuracion inicial
    screen, done, clock = setup()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Espera hasta el siguiente frame
        clock.tick(FRAMES_PER_SECOND)
    pygame.quit()


main()
