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
    MISSIL_COOLDOWN = 15
    MAX_MISSILS = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.missil_cooldown = 0
        self.missils = []

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
        if keys[K_SPACE] and self.missil_cooldown == 0 and len(self.missils) < self.MAX_MISSILS:
            self.missil_cooldown = self.MISSIL_COOLDOWN
            self.missils.append(Missil(self.x + self.WIDTH // 2, self.y - self.HEGIHT, Direction.UP))
        self.missil_cooldown = max(0, self.missil_cooldown - 1)
        for missil in self.missils:
            missil.update()
        self.missils[:] = [missil for missil in self.missils if missil.is_alive]

    def draw(self, screen):
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, self.COLOR, rect)
        for missil in self.missils:
            missil.draw(screen)


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

class Missil(Base):
    WIDTH = 10
    HEGIHT = 20
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    SPEED = 5

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.is_alive = True

    @property
    def is_enemy(self):
        return self.direction == Direction.DOWN

    def draw(self, screen):
        color = self.WHITE if self.is_enemy else self.GREEN
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(screen, color, rect)

    def update(self):
        if self.direction == Direction.DOWN:
            self.y += self.SPEED
        else:
            self.y += -self.SPEED
        self.is_alive = Game.TOP <= self.y <= (Game.BOTTOM - self.HEGIHT)


class Game(object):

    FRAMES_PER_SECOND = 30
    RESOLUTION = WIDTH, HEGIHT = 800, 600
    LEFT = 0
    RIGHT = WIDTH
    WINDOWS_TITLE = 'Space Invaders v1.0'
    BLACK = (0, 0, 0)
    TOP = 0
    BOTTOM = HEGIHT

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.done = False
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.WINDOWS_TITLE)
        self.player = Player(self.WIDTH // 2 - Player.WIDTH // 2, self.HEGIHT - Player.HEGIHT)
        self.enemies = []
        for i in range(5):
            for j in range(11):
                self.enemies.append(Enemy(70 + (70 * j), 20 + i*70))

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
        for enemy in self.enemies:
            enemy.update()

    def draw(self):
        self.screen.fill(self.BLACK)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
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
