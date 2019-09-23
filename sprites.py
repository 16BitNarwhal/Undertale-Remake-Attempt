'''
# sprite classes for game
import pygame as pg
from settings import *

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab on image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

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

    def __init__(self, img):
        super().__init__()

        self.image = img
        self.rect = self.image.get_rect()
        self.change = 0

    def update(self):
        change += 1
        
        pg.transform.scale(self.image, (self.rect.x + change, self.rect.y + change))

'''
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
    def __init__(self, img):
        super().__init__()

        self.image = img
        self.rect = self.image.get_rect()
        self.size = 5

    def update(self):
        self.size += 0.2
