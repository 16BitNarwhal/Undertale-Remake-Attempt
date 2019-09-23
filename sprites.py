import random
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.health = HEALTH
        
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x >= PLAYERSPEED:
            self.rect.x -= PLAYERSPEED
        if keys[pg.K_RIGHT] and self.rect.x <= WIDTH - 25 - PLAYERSPEED:
            self.rect.x += PLAYERSPEED
        if keys[pg.K_UP] and self.rect.y >= PLAYERSPEED:
            self.rect.y -= PLAYERSPEED
        if keys[pg.K_DOWN] and self.rect.y <= HEIGHT - 25 - PLAYERSPEED:
            self.rect.y += PLAYERSPEED



class EnemyAttack(pg.sprite.Sprite):
    def __init__(self, img):
        super().__init__()

        self.image = img
        self.rect = self.image.get_rect()
        self.speed = random.randint(3,7)

    def update(self):
        self.rect.x -= self.speed