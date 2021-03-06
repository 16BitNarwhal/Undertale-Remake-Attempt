import pygame as pg
import random
import time
from settings import *
from sprites import *
import os
import math

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.timer = time.time()
        self.running = True
        self.highscoreColour = WHITE
        self.score = 0
        self.stage = "chooseStage"

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.attacks = pg.sprite.Group()
        self.attackingBoss = pg.sprite.Group()
        # self.buttons = ButtonGroup(self)
        
        self.player = Player(self, self.heart)
        self.healthBar = HealthBar(self, HDISTANCE + (GAMEWIDTH/2) - 50, VDISTANCE + GAMEWIDTH + 10)
        self.boss = Boss(self, self.sans)
        self.border = Border(self, self.border)

        self.startTime = time.time()
        self.startAtkTime = time.time()

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        self.load_data()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.healthBar.update()
        self.attacks.update()

        if self.stage == "chooseStage":
            self.chooseStage()
            self.startTime = time.time()

        elif self.stage == "enemyAttack":
            self.enemyAttack()

            if self.startTime - time.time() >= random.randint(6, 15):
                self.stage == "attackStage"

        elif self.stage == "attackStage":
            self.attackStage()
            self.startTime = time.time()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def enemyAttack(self):
        # scoring
        if (time.time() - self.startAtkTime) >= random.random()*500:
            self.startAtkTime = time.time()

            # initialize attack
            self.newAttackBoss = AttackBoss(self, self.whiteHeart)
            
        for attack in self.attackingBoss:
            if attack.rect.colliderect(self.player.rect):
                # Score update
                self.score += random.randint(5, 25)

                if self.score > self.highscore:
                    self.highscore = self.score
                    self.highscoreColour = GREEN

                self.all_sprites.remove(attack)
                self.attackingBoss.remove(attack)
            
        # bone attack
        if (time.time() - self.startTime) >= random.randint(1, 10)/10:
            self.startTime = time.time()
            
            # initialize attack
            self.newAttack = EnemyAttack(self, self.bone)

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

        for attack in self.attacks:
            if attack.rect.colliderect(self.player.rect):
                self.player.health -= random.randint(5, 15)
                self.attacks.remove(attack)
                self.all_sprites.remove(attack)

                if self.player.health <= 0:
                    self.playing = False
                    self.running = False

            if (attack.direction == 'goLEFT' and attack.rect.x <= 0) or (attack.direction == 'goRIGHT' and attack.rect.x >= WIDTH) or (attack.direction == 'goUP' and attack.rect.y <= 0) or (attack.direction == 'goDOWN' and attack.rect.y >= HEIGHT):
                self.attacks.remove(attack)
                self.all_sprites.remove(attack)

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.healthBar.draw(self.screen)
        '''for button in self.buttons:
            pg.draw.rect(self.screen, ORANGE, (button.rect.topleft, (button.width, button.height)))
            pg.draw.rect(self.screen, BLACK, ((button.rect.x+5, button.rect.y+5), (button.width-10, button.height-10)))
            pg.draw.rect(self.screen, ORANGE, ((button.rect.x+10, button.rect.y+10), (button.width-20, button.height-20)))
            self.draw_text(button.text, 60, WHITE, button.rect.x+120, button.rect.y+10)'''

        self.draw_text("Score: " + str(self.score), 35, WHITE, 150, 75)
        self.draw_text("High score: " + str(self.highscore), 35, self.highscoreColour, 150, 125)
        
        for attack in self.attackingBoss:
            if attack.elapsedTime == 3:
                self.draw_text(str(attack.elapsedTime), 15, GREEN, attack.rect.x + 11, attack.rect.y + 3)

            elif attack.elapsedTime == 2:
                self.draw_text(str(attack.elapsedTime), 15, YELLOW, attack.rect.x + 11, attack.rect.y + 3)

            elif attack.elapsedTime == 1:
                self.draw_text(str(attack.elapsedTime), 15, RED, attack.rect.x + 11, attack.rect.y + 5)

            elif attack.elapsedTime <= 0:
                self.all_sprites.remove(attack)
                self.attackingBoss.remove(attack)
        
        # self.screen.blit(self.timeText, self.timeTextRect)
        # self.screen.blit(self.highTimeText, self.highTimeText)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font('C:\WINDOWS\FONTS\IMPACT.TTF', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def attackStage(self):
        pass

    def chooseStage(self):
        # create buttons
        self.atkBtn = Button(self, WIDTH/2 - 275, HEIGHT/2 + 150, self.fightImg)
        self.healBtn = Button(self, WIDTH/2 + 25, HEIGHT/2 + 150, self.healImg)

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        with open(os.path.join(self.dir, "highscore.txt"), 'w') as f:
            f.write(str(self.highscore))

    def load_data(self):
        # load high score
        self.dir = os.path.dirname(__file__)
        with open(os.path.join(self.dir, "highscore.txt"), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # load pictures
        self.bone = pg.image.load(os.path.join('pictures', 'bone.png'))
        self.heart = pg.image.load(os.path.join('pictures', 'hearts.png'))
        self.border = pg.image.load(os.path.join('pictures', 'border.png'))
        self.sans = pg.transform.scale(pg.image.load(os.path.join('pictures', 'sans.png')), (250, 250))
        self.whiteHeart = pg.image.load(os.path.join('pictures', 'whiteHeart.png'))
        self.fightImg = pg.image.load(os.path.join('pictures', 'fightButton.png'))
        self.healImg = pg.image.load(os.path.join('pictures', 'healButton.png'))

g = Game()
g.show_start_screen()
while g.running:
    g.load_data()
    g.new()
    g.show_go_screen()

pg.quit()