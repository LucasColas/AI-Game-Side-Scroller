import pygame
from pygame.locals import *
import os
import sys
import math
import random
import visualize
import neat

#Initialize
pygame.font.init()
W, H = 800, 437
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('images','bg.png')).convert()

bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

Stat_Font = pygame.font.SysFont("comicsans", 20)

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1,8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images','0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))

        elif self.jumping:
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x,self.y+3,self.width-8,self.height-35)

            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
            win.blit(self.slide[self.slideCount//10], (self.x,self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0

            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-13)

        #pygame.draw.rect(win, (255,0,0),self.hitbox, 2)

    def get_distance(self, obstacles):
        for obstacle in obstacles:
            if obstacle.x > self.x:
                return [obstacle.x, obstacle.y]

class saw(object):
    rotate = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),
    pygame.image.load(os.path.join('images', 'SAW1.PNG')),
    pygame.image.load(os.path.join('images', 'SAW2.PNG')),
    pygame.image.load(os.path.join('images', 'SAW3.PNG'))]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4
        self.passed = False
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)


    def draw(self,win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y))
        self.rotateCount += 1

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class spike(saw):
    picture = pygame.image.load(os.path.join('images', 'spike.png'))
    img = pygame.transform.scale(picture, (48, 330))

    def __init__(self, x, y, width, height):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.hitbox = (self.x + 10, self.y, 28,315)

        self.passed = False
    def draw(self,win):
        self.hitbox = (self.x + 10, self.y, 28,315)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

"""
def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score

    return last

def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 30
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumpin = False

        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0

"""


runner = player(200, 313, 64, 64)

def redrawWindow(runners, obstacles, score, gen):
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2,0))
    #text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    #runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)

    for runner in runners:
        runner.draw(win)

    #win.blit(text, (700, 10))
    white = (255, 255, 255)
    score_text = Stat_Font.render("Score : " + str(score), 1, white)
    win.blit(score_text, (W - 10 - score_text.get_width(), 10))

    if gen == 0:
        gen = 1

    gen_text = Stat_Font.render("Gen : " + str(gen), 1, white)
    win.blit(gen_text, (W - 15 - gen_text.get_width(), 10))

    pygame.display.update()


#pygame.time.set_timer(USEREVENT+1, 500)
#pygame.time.set_timer(USEREVENT+2, 3000)
speed = 30
obstacles = [saw(810, 310, 64, 64)]
pause = 0
fallSpeed = 0


def main(genomes, config):

    global bgX
    global bgX2
    global gen

    gen += 1

    nets = []
    ge = []
    runners = []
    obstacles = [saw(810, 310, 64, 64)]

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        runners.append(player(200, 313, 64, 64))
        g.fitness = 0
        ge.append(g)


    run = True
    score = 0

    while run and len(runners) > 0:
        gen += 1
        bgX -= 1.4
        bgX2 -= 1.4

        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        """
        if pause > 0:
            pause += 1
            if pause > fallSpeed * 2:
                endScreen()
        """
        clock.tick(80)

        #score = speed//10 - 3


        for x, runner in enumerate(runners):
            #runner.draw()
            ge[x].fitness += 0.005

            inputs = (runner.get_distance(obstacles))
            outputs = nets[x].activate(inputs)

            if outputs[0] > 0.5:
                if not(runner.sliding):
                    runner.sliding = True

            elif outputs[1] > 0.5 and round(runner.y) == 313:
                if not(runner.jumping):
                    runner.jumping = True
            """
            if round(runner.y) == 313:
                runner.jumping = True
            """

        add_obstacle = False

        rem = []
        for obstacle in obstacles:
            for runner in runners:
                if obstacle.collide(runner.hitbox):
                    runner.falling = True
                    ge[runners.index(runner)].fitness -= 1
                    nets.pop(runners.index(runner))
                    ge.pop(runners.index(runner))
                    runners.pop(runners.index(runner))

                    """
                    if pause == 0:
                        pause = 1
                        fallSpeed = speed
                    """
            if obstacle.x < -64:
                obstacles.pop(obstacles.index(obstacle))
            else:
                obstacle.x -= 1.4
            if obstacle.x < runner.x and len(obstacles) == 1:
                score += 1
                add_obstacle = True
            if obstacle.x + obstacle.width < 0:
                rem.append(obstacle)


        if add_obstacle:
            increase_fitness = 5
            r = random.randrange(0,2)
            if r == 0:
                obstacles.append(saw(810, 310, 64, 64))
            else:
                obstacles.append(spike(810, 0, 48, 310))
            add_obstacle = False
            for g in ge:
                g.fitness += increase_fitness

        for r in rem:
            obstacles.remove(r)

        """
            if event.type == USEREVENT+1:
                speed += 1

            if event.type == USEREVENT+2:
                r = random.randrange(0,2)
                if r == 0:
                    obstacles.append(saw(810, 310, 64, 64))
                elif r == 1:
                    obstacles.append(spike(810, 0, 48, 310))

        if runner.falling == False:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not(runner.jumping):
                    runner.jumping = True

            if keys[pygame.K_DOWN]:
                if not(runner.sliding):
                    runner.sliding = True
        """

        redrawWindow(runners, obstacles, score)

def run(config_path):
    max_gen = 120
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
        neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run up for max_gen's values generations
    winner = p.run(main, max_gen)

if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NeatConfigSideScroller.txt")
    run(config_path)
