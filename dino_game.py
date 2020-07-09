import pygame
import neat
import os
from pygame.locals import *
import random

pygame.init()

#initialising and setting up the font
pygame.font.init()
stat_font = pygame.font.SysFont("couriernew", 30)

#getting all the pictures we need
#Dinosaur
dino_pic = pygame.image.load(os.path.join("data", "dino_.png"))
dino_run1 = pygame.image.load(os.path.join("data", "dino_1.png"))
dino_run2 = pygame.image.load(os.path.join("data", "dino_2.png"))
dino_duck1 = pygame.image.load(os.path.join("data", "dino_ducking1.png"))
dino_duck2 = pygame.image.load(os.path.join("data", "dino_ducking2.png"))

#Bird
bird1 = pygame.image.load(os.path.join("data", "ptera1.png"))
bird2 = pygame.image.load(os.path.join("data", "ptera2.png"))

#Cactus
cactus_pic = pygame.image.load(os.path.join("data", "cacti-small.png"))
cactus_many = pygame.image.load(os.path.join("data", "cacti-big.png"))

#Ground
ground_pic = pygame.image.load(os.path.join("data", "ground.png"))

#Game Features
game_over = pygame.image.load(os.path.join("data", "game_over.png"))
replay = pygame.image.load(os.path.join("data", "replay_button.png"))

speed = 8

class Dino:
    def __init__(self):
        self.Img = dino_pic
        self.WIDTH,self.HEIGHT = 44,48
        self.Img = pygame.transform.scale(self.Img,(self.WIDTH,self.HEIGHT))
        self.img = self.Img
        #starting position of dino
        self.x = 60
        self.y = 170
        self.g = -0.25 #gravity effect
        self.vel = 7
        self.animation_time = 3
        self.img_count = 0
        self.t = 0
        self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)

        self.runimg1 = pygame.transform.scale(dino_run1, (self.WIDTH,self.HEIGHT))
        self.runimg2 = pygame.transform.scale(dino_run2,
                                              (self.WIDTH, self.HEIGHT))
        self.duckimg1 = pygame.transform.scale(dino_duck1,
                                              (self.WIDTH + 15, self.HEIGHT))
        self.duckimg2 = pygame.transform.scale(dino_duck2,
                                              (self.WIDTH + 15, self.HEIGHT))

        self.run_imgs = [self.runimg1,self.runimg2]
        self.imgs = [self.img, self.runimg1, self.runimg2]
        self.duck_imgs = [self.duckimg1,self.duckimg2]

        self.count = 0
        self.isJump = False
        self.isDuck = False

    def jump(self):
        self.y -= self.vel
        self.isJump = True

    def update(self):
        if self.y < 170:
            self.vel = self.vel + self.g*self.t #v = u+at
            self.y -= self.vel
            self.t += 0.15

        #if we're done jumping, we refresh all variables
        if self.y > 170:
            self.y = 170 #so that it doesn't go too high up
            self.t = 0
            self.vel = 7
            self.isJump = False

        if self.isDuck:
            self.hitbox = pygame.Rect(self.x + 5, self.y + 20, self.WIDTH + 12, self.HEIGHT - 20)
            self.img = self.duck_imgs[int(self.count) % 2]
            self.count += 0.2
        elif self.isJump:
            self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)
            self.img = self.Img
        else:
            self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)
            self.img = self.run_imgs[int(self.count) % 2]
            self.count += 0.2

    def draw(self,win):
        win.blit(self.img, (self.x,self.y))
        #hitbox check, red rectangle
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class Bird:
    def __init__(self,x):
        self.x = x
        self.WIDTH,self.HEIGHT = 50,40
        self.wing_flap = [pygame.transform.scale(bird1,
                        (self.WIDTH, self.HEIGHT)),pygame.transform.scale(bird2,
                        (self.WIDTH, self.HEIGHT))]
        self.img = None
        self.allowed = False
        self.passed = False 
        self.heights = [175,150,107,10,20]
        self.y = random.choice(self.heights)
        self.speed = 8
        self.count = 0
        self.indicator = 1
        self.hitbox0 = pygame.Rect(self.x, self.y + 10, self.WIDTH, self.HEIGHT - 12)

    def set_height(self):
        self.y = random.choice(self.heights)

    #generate a bird if its allowed then reset
    def update(self):
        if self.allowed:
            self.set_height()
            self.allowed = False
        self.img = self.wing_flap[int(self.count)%2] #smooth animation
        self.count += 0.1

        self.x -= self.speed

        self.hitbox0 = pygame.Rect(self.x, self.y + 10, self.WIDTH,
                                   self.HEIGHT - 12)

    def detect_collide(self, dino):
        return self.hitbox0.colliderect(dino.hitbox)

    def get_width(self):
        return self.WIDTH

    def get_height(self):
        return (self.HEIGHT-12)

    def draw(self,win):
        self.img = self.wing_flap[int(self.count) % 2] #keep this
        win.blit(self.img, (self.x, self.y))

class Cactus:
    gap = 450
    def __init__(self,x):
        self.x = x
        self.width = 45
        self.height = 44
        self.speed = 8
        self.img1 = pygame.transform.scale(cactus_pic,(self.width,self.height))
        self.img2 = pygame.transform.scale(cactus_many,(self.width+5,self.height))
        self.y = 175
        self.count = 0
        self.img = None
        self.indicator = 0
        self.passed = False

        self.cactus_choice = random.choice((1,2))
        if self.cactus_choice == 1:
            self.hitbox0 = pygame.Rect(self.x, self.y, self.width, self.height)
        elif self.cactus_choice == 2:
            self.hitbox0 = pygame.Rect(self.x, self.y, self.width+5, self.height)


    def get_width(self):
        if self.cactus_choice == 1:
            return self.width
        elif self.cactus_choice == 2:
            return int(self.width+5)


    def get_height(self):
        if self.cactus_choice == 1 or self.cactus_choice == 2:
            return self.height


    def update(self):
        if self.cactus_choice == 1 or self.cactus_choice == 2:
            self.x -= self.speed
            if self.cactus_choice == 1:
                self.hitbox0 = pygame.Rect(self.x, self.y, self.width, self.height)
            else:
                self.hitbox0 = pygame.Rect(self.x, self.y, self.width+5, self.height)

    def detect_collide(self, dino):
        return self.hitbox0.colliderect(dino.hitbox)

    def draw(self, win):
        if self.cactus_choice == 1:
            win.blit(self.img1, (self.x, self.y))
        elif self.cactus_choice == 2:
            win.blit(self.img2,(self.x,self.y))



class Ground:
    def __init__(self):
        self.ground_length = 1202
        self.img1 = ground_pic
        self.img2 = ground_pic
        self.img1_x = 0
        self.img1_y = 200
        self.img2_x = self.img1_x + self.ground_length
        self.img2_y = self.img1_y
        self.speed = 8

    def draw(self, win):
        win.blit(self.img1, (self.img1_x, self.img1_y))
        win.blit(self.img2, (self.img2_x, self.img2_y))

    def update(self):
        self.img1_x -= self.speed
        self.img2_x -= self.speed

        if self.img1_x + self.ground_length < 0:
            self.img1_x = self.img2_x + self.ground_length
        elif self.img2_x + self.ground_length < 0:
            self.img2_x = self.img1_x + self.ground_length

def draw_window(win, dinos, cacti, ground, score_value):
    win.fill((240,240,240))
    for cactus in cacti:
        cactus.draw(win)


    score = stat_font.render("Score: " + str(int(score_value)), True,
                             (200, 200, 200))
    win.blit(score, (680,30))
    ground.draw(win)
    for dino in dinos:
        dino.draw(win)


    pygame.display.update()

def main(genomes, config):
    nets = []
    ge = []
    dinos = []
    #every genome has its own network
    for a, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        dinos.append(Dino())
        g.fitness = 0
        ge.append(g)


    ground = Ground()
    cacti = [Cactus(1350)]
    win = pygame.display.set_mode((800,230))
    clock = pygame.time.Clock()
    score_value = 0
    gameover = game_over
    replay_button = replay

    run = True
    play = True
    dead = False

    frame_rate = 60

    while play:
        if not dead:
            draw_window(win,dinos,cacti,ground,score_value)

        while run:
            clock.tick(frame_rate)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if len(dinos) <= 0:
                play = False
                break

            for x,dino in enumerate(dinos):
                dino.update()
                ge[x].fitness += 0.1
                output = nets[x].activate((8*100, dino.y, cacti[0].y, dino.y-cacti[0].y,
                                           cacti[0].x - dino.x, cacti[0].get_height(),
                                           cacti[0].get_width()))


                action = (output.index(max(output)))
                if action == 0:
                    dino.isJump = True
                    dino.isDuck = False
                    if dino.isJump == True:
                        dino.jump()
                else:
                    dino.isDuck = True
                    dino.isJump = False
                    if dino.isJump == True:
                        dino.jump()

            add_cactus = False
            rem = []
            for cactus in cacti:
                for x,dino in enumerate(dinos):
                    if cactus.detect_collide(dino):
                        ge[x].fitness -= 1
                        dinos.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                    if not cactus.passed and cactus.x < dino.x + 5:
                        cactus.passed = True
                        if len(cacti) <= 1:
                            add_cactus = True

                if cactus.x + cactus.get_width() + 5 < 0:
                    rem.append(cactus)

                cactus.update()

            if add_cactus:
                score_value += 1
                for g in ge:
                    g.fitness += 5
                if score_value > 10:
                    choice = random.choice((1,2))
                else:
                    choice = 1

                if choice == 1:
                    cacti.append(Cactus(random.randint(500,600)))
                else:
                    cacti.append(Bird(random.randint(500,600)))

            for r in rem:
                cacti.remove(r)


            ground.update()
            draw_window(win,dinos,cacti,ground, score_value)


            pygame.display.update()

            if dead:
                run = False

#main()
"""Here, we get information out of the config file
and collect the relevant statistics about the generations to show"""
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)  # defining all the subheadings we used in our config textfile

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)  # this is for displaying our statistics on the screen

    winner = p.run(main, 50)  # run main 50 times


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)

