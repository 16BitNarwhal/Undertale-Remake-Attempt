import pygame as pg
import random
import time
from settings import *
from sprites import *
import os

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.attacks = pg.sprite.Group()
        
        self.player = Player(self.heart)
        self.all_sprites.add(self.player)

        self.border = Border(self.border)
        self.all_sprites.add(self.border)

        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(str(self.player.health), True, WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (WIDTH // 2, HEIGHT // 2)

        self.startTime = time.time()

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.load_data()
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.attacks.update()

        self.text = self.font.render(str(self.player.health), True, WHITE)

        # elapsed time 0.5 s to add new attack
        self.elapsedTime = time.time() - self.startTime
        if self.elapsedTime >= random.random()*2.5:
            self.startTime = time.time()
            
            # initialize attack
            self.newAttack = EnemyAttack(self.bone, random.choice(DIRECTIONS))

            if self.newAttack.direction == 'goUP':
                self.newAttack.rect.x = random.randint(HDISTANCE+5, HDISTANCE+GAMEWIDTH)
                self.newAttack.rect.y = HEIGHT
            elif self.newAttack.direction == 'goDOWN':
                self.newAttack.rect.x = random.randint(HDISTANCE+5, HDISTANCE+GAMEWIDTH)
                self.newAttack.rect.y = 0
            elif self.newAttack.direction == 'goRIGHT':
                self.newAttack.rect.x = 0
                self.newAttack.rect.y = random.randint(VDISTANCE+5, VDISTANCE+GAMEHEIGHT)
            else:
                self.newAttack.rect.x = WIDTH
                self.newAttack.rect.y = random.randint(VDISTANCE+5, VDISTANCE+GAMEHEIGHT)

            self.all_sprites.add(self.newAttack)
            self.attacks.add(self.newAttack)

        for attack in self.attacks:
            if attack.rect.colliderect(self.player.rect):
                self.player.health -= random.randint(5, 15)
                self.attacks.remove(attack)
                self.all_sprites.remove(attack)

#                if self.player.health <= 0:
#                    self.playing = False
#                    self.running = False

            if (attack.direction == 'goLEFT' and attack.rect.x <= 0) or (attack.direction == 'goRIGHT' and attack.rect.x >= WIDTH) or (attack.direction == 'goUP' and attack.rect.y <= 0) or (attack.direction == 'goDOWN' and attack.rect.y >= HEIGHT):
                self.attacks.remove(attack)
                self.all_sprites.remove(attack)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        self.screen.blit(self.text, self.textRect)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

    def load_data(self):
        # load pictures
        self.bone = pg.image.load(os.path.join('pictures', 'bone.png'))
        self.heart = pg.image.load(os.path.join('pictures', 'hearts.png'))
        self.border = pg.image.load(os.path.join('pictures', 'border.png'))

g = Game()
g.show_start_screen()
while g.running:
    g.load_data()
    g.new()
    g.show_go_screen()

pg.quit()