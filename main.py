import os

import pygame
from pygame.locals import *


class Game(object):

    FRAMES_PER_SECOND = 30
    RESOLUTION = WIDTH, HEGIHT = 800, 600
    WINDOWS_TITLE = 'Space Invaders v1.0'
    BLACK = (0, 0, 0)

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.done = False
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.WINDOWS_TITLE)

    def update(self):
        # Handle exit events
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE] or keys[K_q]:
            self.done = True
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return
        # TODO: Handle players events here

    def draw(self):
        self.screen.fill(self.BLACK)
        pygame.display.flip()

    def wait(self):
        self.clock.tick(self.FRAMES_PER_SECOND)


def main():
    game = Game()
    while not game.done:
        game.update()
        game.draw()
        game.wait()


main()
