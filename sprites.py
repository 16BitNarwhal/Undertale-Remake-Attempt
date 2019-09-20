# sprite classes for game
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x >= SPEED:
            self.rect.x -= SPEED
        if keys[pg.K_RIGHT] and self.rect.x <= WIDTH - 25 - SPEED:
            self.rect.x += SPEED
        if keys[pg.K_UP] and self.rect.y >= SPEED:
            self.rect.y -= SPEED
        if keys[pg.K_DOWN] and self.rect.y <= HEIGHT - 25 - SPEED:
            self.rect.y += SPEED



class EnemyAttack(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.Surface([5, 5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.size = 5

    def update(self):
        self.size += 0.2

        self.image = pg.Surface([self.size, self.size])
        self.image.fill(WHITE)
        