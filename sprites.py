import random
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, img):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = HDISTANCE + (GAMEWIDTH/2)
        self.rect.y = VDISTANCE + (GAMEHEIGHT/2)
        self.health = HEALTH
        
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x >= PLAYERSPEED and not self.rect.x <= HDISTANCE:
            self.rect.x -= PLAYERSPEED
        if keys[pg.K_RIGHT] and self.rect.x <= WIDTH - 25 - PLAYERSPEED and not self.rect.x >= HDISTANCE + GAMEWIDTH - self.rect.width:
            self.rect.x += PLAYERSPEED
        if keys[pg.K_UP] and self.rect.y >= PLAYERSPEED and not self.rect.y <= VDISTANCE:
            self.rect.y -= PLAYERSPEED
        if keys[pg.K_DOWN] and self.rect.y <= HEIGHT - 25 - PLAYERSPEED and not self.rect.y >= VDISTANCE + GAMEHEIGHT - self.rect.height:
            self.rect.y += PLAYERSPEED

class Border(pg.sprite.Sprite):
    def __init__(self, img):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = HDISTANCE
        self.rect.y = VDISTANCE

class HealthBar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.left = HDISTANCE + (GAMEWIDTH/2) - 50
        self.top = VDISTANCE + GAMEWIDTH + 10

        self.rectHP = pg.Rect(self.left, self.top, 100, 20)
        self.rectLoss = pg.Rect(self.left + 100, self.top, 0, 20)
        
    def update(self, playerHealth):
        self.rectHP.width = playerHealth
        self.rectLoss.x = self.left + playerHealth
        self.rectLoss.width = 100 - playerHealth

    def draw(self, screen):
        pg.draw.rect(screen, GREEN, self.rectHP)
        pg.draw.rect(screen, RED, self.rectLoss)

class EnemyAttack(pg.sprite.Sprite):
    def __init__(self, img):
        super().__init__()

        self.image = img
        self.direction = random.choice(DIRECTIONS)

        if self.direction == 'goUP' or self.direction == 'goDOWN':
            self.image = pg.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect()
        self.speed = random.randint(1,4)

    def update(self):
        if self.direction == 'goUP':
            self.rect.y -= self.speed
        
        elif self.direction == 'goDOWN':
            self.rect.y += self.speed

        elif self.direction == 'goRIGHT':
            self.rect.x += self.speed
        
        else:
            self.rect.x -= self.speed