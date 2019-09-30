import random
import pygame as pg
import math
import time
from settings import *

class ButtonGroup(pg.sprite.Group):

    def handle_event(self, event):
        for spr in self.sprites():
            # Check if the sprite has a `handle_event` method.
            if hasattr(spr, 'handle_event'):
               spr.handle_event(event)

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            spr.game.draw_text(spr.text, 25, WHITE, spr.rect.x, spr.rect.y)
            pg.draw.rect(surface, ORANGE, (spr.rect.topleft, (spr.width, spr.height)))
        self.lostsprites = []

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
    def __init__(self, game, x, y, text):
        super().__init__()
        self.game = game
        self.width = 250
        self.height = 100

        self.rect = pg.Rect(x, y, self.width, self.height)

        self.game.buttons.add(self)
    
    def update(self):
        if pg.mouse.get_pressed() and pg.mouse.get_pos().x >= self.rect.x and pg.mouse.get_pos().y >= self.rect.y and pg.mouse.get_pos <= self.rect.x + self.width and pg.mouse.get_pos().y <= self.rect.y + self.height:
            print("This button pressed")