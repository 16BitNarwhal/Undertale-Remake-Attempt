import random
import pygame as pg
import math
import time
from settings import *

'''class ButtonGroup(pg.sprite.Group):

    def __init__(self, game):
        super().__init__()
        self.game = game

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            pg.draw.rect(surface, ORANGE, (spr.rect.topleft, (spr.width, spr.height)))
            pg.draw.rect(surface, BLACK, ((spr.rect.x+5, spr.rect.y+5), (spr.width-10, spr.height-10)))
            pg.draw.rect(surface, ORANGE, ((spr.rect.x+10, spr.rect.y+10), (spr.width-20, spr.height-20)))
            self.game.draw_text(spr.text, 60, WHITE, spr.rect.x+120, spr.rect.y+10)
            
        self.lostsprites = []'''

class Player(pg.sprite.Sprite):
    def __init__(self, game, img):
        super().__init__()
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = HDISTANCE + (GAMEWIDTH/2)
        self.rect.y = VDISTANCE + (GAMEHEIGHT/2)
        self.health = HEALTH

        self.game.all_sprites.add(self)
        
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
    def __init__(self, game, img):
        super().__init__()
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = HDISTANCE
        self.rect.y = VDISTANCE

        self.game.all_sprites.add(self)

class HealthBar(pg.sprite.Sprite):
    def __init__(self, game, left, top):
        super().__init__()
        self.game = game
        self.left = left
        self.top = top

        self.rectHP = pg.Rect(self.left, self.top, 100, 20)
        self.rectLoss = pg.Rect(self.left + 100, self.top, 0, 20)
        
    def update(self):
        self.rectHP.width = self.game.player.health
        self.rectLoss.x = self.left + self.game.player.health
        self.rectLoss.width = 100 - self.game.player.health

    def draw(self, screen):
        pg.draw.rect(screen, GREEN, self.rectHP)
        pg.draw.rect(screen, RED, self.rectLoss)

class EnemyAttack(pg.sprite.Sprite):
    def __init__(self, game, img):
        super().__init__()
        self.game = game
        self.image = img
        self.direction = random.choice(DIRECTIONS)

        if self.direction == 'goUP' or self.direction == 'goDOWN':
            self.image = pg.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect()
        self.speed = random.randint(1,4)

        self.game.all_sprites.add(self)
        self.game.attacks.add(self)

    def update(self):
        if self.direction == 'goUP':
            self.rect.y -= self.speed
        
        elif self.direction == 'goDOWN':
            self.rect.y += self.speed

        elif self.direction == 'goRIGHT':
            self.rect.x += self.speed
        
        else:
            self.rect.x -= self.speed

class Boss(pg.sprite.Sprite):
    def __init__(self, game, img):
        super().__init__()
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - HDISTANCE + 50
        self.rect.y = 10

        self.game.all_sprites.add(self)
    
    def update(self):
        pass

class AttackBoss(pg.sprite.Sprite):
    def __init__(self, game, img):
        super().__init__()
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(HDISTANCE, HDISTANCE + GAMEWIDTH - 25)
        self.rect.y = random.randint(VDISTANCE, VDISTANCE + GAMEHEIGHT - 25)
        self.start = time.time()
        self.elapsedTime = 3 - math.floor(time.time() - self.start)

        self.game.all_sprites.add(self)

    def update(self):
        self.elapsedTime = 3 - math.floor(time.time() - self.start)

class Button(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        super().__init__()
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.click = pg.mouse.get_pressed()
        self.mouse = pg.mouse.get_pos()

        self.game.all_sprites.add(self)
    
    def update(self):
        if (self.click[0] == 1) and (self.rect.x + self.rect.width >= self.mouse[0] >= self.rect.x) and (self.rect.y + self.rect.width >= self.mouse[1] >= self.rect.y):
            self.click = pg.mouse.get_pressed()
            self.mouse = pg.mouse.get_pos()
            self.game.all_sprites.remove(self.game.atkBtn)
            self.game.all_sprites.remove(self.game.healBtn)