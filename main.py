import os

import pygame
from pygame.locals import *


class Base(object):
    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def size(self):
        return (self.WIDTH, self.HEGIHT)

class Player(Base):
    HEGIHT = 20
    WIDTH = 60
    COLOR = (0, 255, 0)
    DX = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, keys):
        if keys[K_LEFT]:
            if (self.x - self.DX) >= Game.LEFT:
                self.x -= self.DX
            else:
                self.x = Game.LEFT
        elif keys[K_RIGHT]:
            if (self.x + self.DX + self.WIDTH) <= Game.RIGHT:
                self.x += self.DX
            else:
                self.x = Game.RIGHT - self.WIDTH

    def draw(self, screen):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, self.COLOR, rect)


class Direction:
    RIGHT = 0
    LEFT  = 1
    UP    = 2
    DOWN  = 3


class Enemy(Base):
    HEGIHT = 25
    WIDTH = 25
    COLOR = (255, 255, 255)
    SPEED = 1
    DIRECTIONS = {
        Direction.RIGHT: (SPEED,      0, 60),
        Direction.LEFT:  (-SPEED,     0, 60),
        Direction.DOWN:  (0,      SPEED,  5),
    }
    INITIAL_MOVEMENT = 0
    MOVEMENTS = [Direction.LEFT, Direction.DOWN, Direction.RIGHT, Direction.DOWN]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.movement = self.INITIAL_MOVEMENT
        self.direction = self.MOVEMENTS[self.movement]
        self.dx, self.dy, self.frames = self.DIRECTIONS[self.direction]

    @property
    def next_movement(self):
        return (self.movement + 1) % len(self.MOVEMENTS)

    def update(self):
        if self.frames == 0:
            self.movement = self.next_movement
            self.direction = self.MOVEMENTS[self.movement]
            self.dx, self.dy, self.frames = self.DIRECTIONS[self.direction]
        else:
            self.x += self.dx
            self.y += self.dy
            self.frames -= 1
        

    def draw(self, screen):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, self.COLOR, rect)


class Game(object):

    FRAMES_PER_SECOND = 30
    RESOLUTION = WIDTH, HEGIHT = 800, 600
    LEFT = 0
    RIGHT = WIDTH
    WINDOWS_TITLE = 'Space Invaders v1.0'
    BLACK = (0, 0, 0)

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.done = False
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.WINDOWS_TITLE)
        self.player = Player(self.WIDTH // 2 - Player.WIDTH // 2, self.HEGIHT - Player.HEGIHT)
        self.enemy = Enemy(70, 20)

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
        self.player.update(keys)
        self.enemy.update()

    def draw(self):
        self.screen.fill(self.BLACK)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
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
