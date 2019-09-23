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
        self.player = Player()
        self.all_sprites.add(self.player)

        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(str(self.player.rect.x) + " " + str(self.player.rect.y), True, WHITE)
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

        # elapsed time 0.5 s to add new attack
        self.elapsedTime = time.time() - self.startTime
        if self.elapsedTime >= random.random()*2.5:
            self.startTime = time.time()
            
            # initialize attack
            self.newAttack = EnemyAttack(self.bone)
            self.newAttack.rect.x = WIDTH
            self.newAttack.rect.y = random.randint(0, HEIGHT)
            self.all_sprites.add(self.newAttack)
            self.attacks.add(self.newAttack)

        for attack in self.attacks:
            if attack.rect.colliderect(self.player.rect):
                self.playing = False
                self.running = False

            if attack.rect.x <= 10:
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

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()