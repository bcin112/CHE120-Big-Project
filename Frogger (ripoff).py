#Joseph Foti

import pygame
import random
r = random.randint
c = random.choice

#################################### CLASSES ##################################

class player():
class player(): #Just a test comment to see if git works
    def __init__(self):
        self.x = 500
        self.y = 700
        self.w = 50
        self.h = 1
        self.img = pygame.image.load("tile000.png")
        self.img = pygame.transform.scale(self.img, (110,110))
    
    def draw(self):
        extraY = -11
        extraX = 1.5
        
        if self.img == frogs[0]:
            extraY = -11
            extraX = 1.5
        elif self.img == frogs[1]:
            extraY = 8
            extraX = -10
        elif self.img == frogs[2]:
            extraY = 20
            extraX = 7
        elif self.img == frogs[3]:
            extraY = 2
            extraX = 20
            
        screen.blit(self.img, (self.x-extraX,self.y-extraY))
    
    def move(self,up,down,left,right):
        global pos
        
        if self.y == 700 and up:
            self.y -= 100
            self.img = frogs[0]
        
        elif up:
            pos += 100
            lanes.append(lane(-100 - pos))
            self.img = frogs[0]
        
        elif down:
            self.y += 100
            self.img = frogs[2]
            
        if right and self.x < 900:
            self.x += 100
            self.img = frogs[3]
        
        elif left and self.x > 0:
            self.x -=100
            self.img = frogs[1]
        
class lane():
    
    def __init__(self,y):
        global wait
        global styles
        self.direction = "no"
    
        self.y = y
        self.speed = 0
    
        self.obstacles = []

        if not wait:
            if pos < 2500:
                g = 2
                t = 2
                R = 1
                l = 1
                p = 2
            
            elif pos < 5000:
                g = 1
                t = 2
                R = 2
                l = 2
                p = 2
            
            elif pos < 7500:
                g = 1
                t = 2
                R = 3
                l = 1
                p = 2
            
            elif pos < 10000:
                g = 1
                t = 2
                R = 3
                l = 3
                p = 3
                
            else:
                g = 1
                t = 3
                R = 4
                l = 3
                p = 2
                
            for i in range(g):
                styles.append("grass")
            for i in range(t):
                styles.append("trees")
            for i in range(R):
                styles.append("road")
            for i in range(l):
                styles.append("w(log)")
            for i in range(p):
                styles.append("w(pad)")
                
        else:
            wait = False
    
        global start
        if start > 0:
            self.type = "grass"
            start -= 1
            
        else:
            self.type = c(styles)
        
        if self.type in "grass_trees":
            
            if self.type == "trees":
                for i in range(r(5,7)):
                    self.obstacles.append(obstacle(self))
                
                removeAll(styles,"trees")
                wait = True
                
            self.bg = (121+r(-10,10),201+r(-10,10),40+r(-10,10))

        
        elif self.type == "road":
            self.direction = c(["l","r"])
            self.bg = (0,0,0)
            self.speed = r(3,6)
            for i in range(r(2,5)):
                self.obstacles.append(obstacle(self))
        
        else:
            if self.type == "w(pad)":
                for i in range(r(3,7)):
                    self.obstacles.append(obstacle(self))
                
                removeAll(styles,"w(pad)")
                wait = True
                
            else:
                self.direction = c(["l","r"])
                self.speed = r(2,5)
                for i in range(r(2,3)):
                    self.obstacles.append(obstacle(self))
                removeAll(styles,"trees")
                wait = True
                
            self.bg = (13+r(-10,10),76+r(-10,10),140+r(-10,10))
    
        if self.direction == "r":
            self.speed *= -1
            
    def draw(self):
        global pos
        pygame.draw.rect(screen, self.bg, (0, self.y+pos, 1000, 100))
        
        if self.type == "road":
            for i in lanes:
                if i.y == self.y - 100 and i.type == "road":
                    color = (255,255,255)
                    
                    if self.direction != i.direction:
                        color = (255,255,0)
                    
                    for i in range(-40,1041,100):
                        pygame.draw.rect(screen,color,(i,self.y + pos - 10,80,20))
                
class obstacle():
    
    def __init__(self,lane):
        self.y = lane.y
        self.img = pygame.image.load("tile004.png")
        self.lane = lane
        self.h = 100
        self.t = self.p = False
        
        if lane.type in "trees_w(pad)":
            if lane.type == "trees":
                self.img = pygame.image.load("treeSprite.png")
                self.img = pygame.transform.scale(self.img, (100,100))
            
            else:
                self.img = pygame.image.load("pad.png")
                self.img = pygame.transform.scale(self.img, (95,95))
                
            self.x = r(0,9)*100
            self.w = 100
        
        else:
            self.w = 0
            avoid = 0
            
            if lane.type == "road":
                for i in lane.obstacles:
                    avoid += i.w + 30 + r(2,3)*100
                
                if r(1,30)==1:
                    self.img = pygame.image.load("whale.png")
                    self.img = pygame.transform.scale(self.img, (152,100))
                    self.w = 160
                    
                else:
                    self.img = pygame.image.load(c(["tile049.png","tile048.png"]))
                    
                    if r(1,10) == 1 and lane.speed >= 5:
                        self.p = True
                        self.frame = r(0,1)
                        self.w = 120
                        
                    elif r(1,3) == 1:
                        self.t = True
                        self.frame = r(0,2)*5
                        self.w = 85
                        
                    else:
                        self.img = pygame.transform.scale(self.img, (95,95))
                        self.w = 85
                
                
            else:
                self.Limg = pygame.image.load("tile024.png")
                self.Mimg = pygame.image.load("tile025.png")
                self.Rimg = pygame.image.load("tile026.png")
                self.Limg = pygame.transform.scale(self.Limg, (100,100))
                self.Mimg = pygame.transform.scale(self.Mimg, (100,100))
                self.Rimg = pygame.transform.scale(self.Rimg, (100,100))
                if len(lane.obstacles) >= 2:
                    self.w = r(2,3)*100
                else:
                    self.w = r(2,4)*100
                
                for i in lane.obstacles:
                    avoid += i.w + r(1,2)*100 + 105
                
                
            
            
            if lane.direction == "l":
                self.x = 1400 - avoid
                
            else:
                self.x = -400 + avoid
            
                if lane.type == "road":
                    self.img = pygame.transform.flip(self.img, True, False)
                
                else:
                    x = self.Limg
                    self.Limg = pygame.transform.flip(self.Rimg, True, False)
                    self.Rimg = pygame.transform.flip(x, True, False)
                    
    def draw(self):
        global pos
        
        if self.lane.type == "w(log)":
            screen.blit(self.Limg, (self.x,self.y + pos - 5))
            for i in range((self.w//100)-2):
                screen.blit(self.Mimg, (self.x+(100*(i+1)),self.y + pos - 5))
            screen.blit(self.Rimg, (self.x+(self.w-100),self.y + pos - 5))

        elif self.t:
            if self.lane.direction == "l":
                self.img = tractorR[(self.frame//(self.lane.speed*2))%3]
            else:
                self.img = tractorL[(self.frame//(self.lane.speed*2))%3]
                
            screen.blit(self.img, (self.x,self.y+pos))
            self.frame += 1
        
        elif self.p:
            if self.lane.direction == "l":
                self.img = oppsR[(self.frame//(self.lane.speed*3))%2]
            else:
                self.img = oppsL[(self.frame//(self.lane.speed*3))%2]
                
            screen.blit(self.img, (self.x,self.y+pos))
            self.frame += 1

        else:
            screen.blit(self.img, (self.x,self.y+pos))
    
    def move(self):
        self.x += self.lane.speed


class person():
    def __init__(self,name,score):
        self.name = name
        self.score = score
#################################### FUNCTIONS ################################
def obstaclePlacementReroll(lane1,lane2):

    done = False
    
    while not done:
        done = True
        
        for i in lane1.obstacles:
            for I in lane2.obstacles:
                if i.x == I.x:
                    I.x = r(0,9)*100
                    done = False

def removeAll(i,thing):

    for x in range(i.count(thing)):
        i.remove(thing)

def drawGame():

    for i in lanes:
        i.draw()
        
        for I in i.obstacles: 
            I.draw()
        
    p.draw()
    
    screen.blit(scoreFont.render(("Score:" + str(pos)), False, (255,255,255)), [25,25])

def menu(spot,right):
    global state
    global done
    global name
    global leaderboard
    
    screen.fill((0, 0, 0))
    screen.blit(title, [0,-7])
    
    screen.blit(titleFont.render(("use arrow keys and press right to select"), False, (53,197,0)), [300,300])
    
    tColor1 = tColor2 = tColor3 = tColor4 = (53,197,0)
    hover = (212, 217, 67)
    
    if spot == 0:
        tColor1 = hover
    elif spot == 1:
        tColor2 = hover
    elif spot == 2:
        tColor3 = hover
    elif spot == 3:
        tColor4 = hover
        
    if right:
        if spot == 0:
            pygame.mixer.Sound.play(startSound)
            for i in range(5):
                screen.blit(titleFont2.render(("Start game"), False, tColor2), [420,430])
                
                pygame.display.flip()
                pygame.time.delay(100)
                
                screen.blit(titleFont2.render(("Start game"), False, hover), [420,430])
                
                pygame.display.flip()
                pygame.time.delay(100)
                
            screen.fill((0,0,0))
            screen.blit(titleFont2.render(("Go to shell"), False, (53,197,0)), [415,430])
            pygame.display.flip()
                
            while True:
                name = input("Enter name here: ")
                if len(name) > 6 or len(name) == 0:
                    print('\nname must be 1-6 characters\n')
                else:
                    break
            
            pygame.mixer.music.load("bgMusic.wav")
            pygame.mixer.music.play(-1)
            
            state = 'game'
            
            init()
        
        elif spot == 1:
            x = leaderboard

            leaderboard = []
            for i in x:
                a = True
                for I in range(len(leaderboard)):
                    if i.score > leaderboard[I].score:
                        leaderboard.insert(I,i)
                        a = False
                        break
                if a:
                    leaderboard.append(i)
                    
            state = 'leaderboard'
        
        elif spot == 2:                
            state = 'instructions'
        
        elif spot == 3:
            done = True
            
        return
        
    screen.blit(titleFont2.render(("Start game"), False, tColor1), [420,430])
    screen.blit(titleFont2.render(("Leaderboard"), False, tColor2), [420,500])
    screen.blit(titleFont2.render(("Instructions"), False, tColor3), [420,570])
    screen.blit(titleFont2.render(("Quit"), False, tColor4), [420,640])
    
    screen.blit(select, [370,420+(spot*70)])

def instructions(right):
    global state
    
    screen.fill((0, 0, 0))
    screen.blit(title, [0,-7])
    
    screen.blit(titleFont.render(("press right to return"), False, (53,197,0)), [400,300])
    
    screen.blit(titleFont2.render(("Your goal is to use the arrow keys to "), False, (53,197,0)), [200,400])
    screen.blit(titleFont2.render(("move the frog as far as you can to get "), False, (53,197,0)), [200,470])
    screen.blit(titleFont2.render((" a high score while crossing trees, "), False, (53,197,0)), [220,540])
    screen.blit(titleFont2.render(("jumping on logs, and avoiding cars"), False, (53,197,0)), [230,610])
    
    if right:
        init()
        state = 'main'

def lb(right):
    global state
    
    screen.fill((0, 0, 0))
    screen.blit(title, [0,-7])
    
    screen.blit(titleFont.render(("press right to return"), False, (53,197,0)), [400,250])
    
    for i in range(10):
        screen.blit(titleFont2.render((((str(i+1)+". ").rjust(4)+leaderboard[i].name.ljust(7)+str(leaderboard[i].score))), False, (53,197,0)), [420,300 + (i*50)])
    
    if right:
        init()
        state = 'main'
        
def die(x):
    global state
    global noInput
    global pos
    global name
    
    pygame.mixer.music.stop()
    
    if x == "drown":
        pygame.mixer.Sound.play(bubble)
        for i in range(6):
            p.img = drown[i]
            
            if i == 5:
                p.x += 10
                
            drawGame()
            
            pygame.display.flip()
            pygame.time.delay(200)
        pygame.time.delay(500)
    
    else:
        if x == "car":
            pygame.mixer.Sound.play(carHit)
        else:
            pygame.mixer.Sound.play(scream)
        p.img = drown[5]
        
        p.x += 10
        
        drawGame()
        
        pygame.display.flip()
        pygame.time.delay(2000)
    
    leaderboard.append(person(name,pos))
    
    state = 'main'
    init()
    noInput = True

def init():
    global up
    global down
    global left
    global right
    global above
    global below
    global lSide
    global rSide
    global wait
    global onLog
    global done
    global pos
    global contact
    global spot
    global styles
    global start
    global lanes
    global p
    
    pos = contact = 0

    start = 3

    p = player()
    
    up = down = left = right = wait = above = below = lSide = rSide = onLog = done = noInput = False
    
    styles = ["grass","trees","road","w(log)","w(pad)"]
    
    lanes = []
    for i in range(9):
        lanes.append(lane(700-(i*100)))
#################################### GLOBAL VARIABLES #########################
pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Street legal frogger")

init()
spot = 0
state = 'main'

frogs = []
frog = pygame.transform.scale(pygame.image.load("tile000.png"),(110,110))
for i in range(4):
    frogs.append(pygame.transform.rotate(frog, (i*90)))
    
drown = []
for i in range(1,6):
    drown.append(pygame.transform.scale(pygame.image.load(("b"+str(i)+".png")), (90,90)))
drown.append(pygame.transform.scale(pygame.image.load(("tile008.png")), (80,80)))

tractorR = []
for i in range(4,1,-1):
    tractorR.append(pygame.transform.scale(pygame.image.load(("tile05"+str(i)+".png")), (95,95)))

tractorL = []
for i in range(2,5):
    tractorL.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(("tile05"+str(i)+".png")), (95,95)), True, False))

oppsR = [pygame.transform.scale(pygame.image.load(("tile059.png")), (100,100)),pygame.transform.flip(pygame.transform.scale(pygame.image.load(("tile059.png")), (100,100)), False, True)]
oppsL = [pygame.transform.flip(pygame.transform.scale(pygame.image.load("tile059.png"), (100,100)), True, False),pygame.transform.flip(pygame.transform.scale(pygame.image.load("tile059.png"), (100,100)), True, True)]

leaderboard = []
for i in range(10):
    leaderboard.append(person('------',0))

select = pygame.transform.scale(pygame.image.load('tile004.png'), (40,40))

scoreFont = pygame.font.SysFont('playbill', 50)
titleFont = pygame.font.Font('Retro Gaming.ttf', 15)
titleFont2 = pygame.font.Font('Retro Gaming.ttf', 25)
title = pygame.image.load('mainmenu.png')

startSound = pygame.mixer.Sound("start.wav")
carHit = pygame.mixer.Sound("carHit.wav")
jump = pygame.mixer.Sound("jump.wav")
bubble = pygame.mixer.Sound("bubble.wav")
scream = pygame.mixer.Sound("scream.wav")
#################################### GAME LOOP ################################

while True:
    # ============================== HANDLE EVENTS  ========================= #
    move = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
            break
        
        if event.type == pygame.KEYDOWN:
            
            if move and not noInput:

                if event.key == pygame.K_UP and not above:      
                    up = True
                    onLog = False
                    move = False
                    pygame.mixer.Sound.play(jump)
                        
                if event.key == pygame.K_DOWN and not below:
                    down = True
                    onLog = False
                    move = False
                    pygame.mixer.Sound.play(jump)
                    
                if event.key == pygame.K_RIGHT and not rSide:      
                    right = True
                    move = False
                    if onLog:
                        contact += 100
                    pygame.mixer.Sound.play(jump)

                if event.key == pygame.K_LEFT and not lSide:      
                    left = True
                    move = False
                    if onLog:
                        contact -= 100
                    pygame.mixer.Sound.play(jump)
                    
    if done == True:
        break
    
    done = noInput = False

    # ============================== MOVE STUFF ============================= #
    if state == 'game':
        
        for i in lanes:
            for I in i.obstacles:
                I.move()
            
        p.move(up,down,left,right)
        up = down = left = right = above = below = lSide = rSide = False

        if onLog:

            p.x = logOn.x + contact
            
        else:
            p.x = round(p.x/100)*100
    # ============================== COLLISION ============================== #
    if state == 'game':

        if p.y == 700:
            below = True
            
        if not (-50 < p.x < 980):
            die("a")
            
        for i in lanes:
            if i.y + pos >= 800:
                lanes.remove(i)
        
        for i in lanes:
            if i.y + pos == 0 and i.type in "trees_w(pad)":
                for I in lanes:
                    if I.y + pos == -100 and I.type in "trees_w(pad)":
                        obstaclePlacementReroll(i,I)
            
            if i.type in "road_w(log)":
                for I in i.obstacles:
                    if I.x > 1400 and i.direction == "l":
                        I.x = -400
                    elif I.x < -400 and i.direction == "r":
                        I.x = 1400
            
            if i.y + pos == 0 and i.type in "road_w(log)":
                for I in lanes:
                    if I.y + pos == -100 and I.type in "road_w(log)":
                        while i.speed == I.speed:
                            I.speed += r(-1,1)
            
            if i.type != "w(log)" and i.y + pos == p.y:
                onLog = False
                
            if i.type == "trees":
                for I in i.obstacles:
                    
                    if I.x == p.x:
                        if I.y + pos == p.y - 100:
                            above = True
                        if I.y + pos == p.y + 100:
                            below = True
                    
                    if I.y + pos == p.y:
                        if I.x == p.x - 100:
                            lSide = True
                        if I.x == p.x + 100:
                            rSide = True

            elif i.type == "road" and i.y + pos == p.y:
                for I in i.obstacles:
                    if I.x + I.w > p.x + 25 and I.x < p.x + p.w + 25:
                        die("car")
                        break
            
            elif i.type in "w(pad)_w(log)" and i.y + pos == p.y:
                onWater = True
                
                for I in i.obstacles:

                    if I.x + I.w > p.x and I.x < p.x + p.w:
                        onWater = False
                        
                        if i.type == "w(log)" and not onLog:
                            contact = round((p.x - I.x)/100)*100
                            logOn = I
                            onLog = True
                             
                if onWater:
                    onLog = False
                    die("drown")
                    
                
                else:
                    if i.type == "w(log)":
                        onLog = True
    # ============================== DRAW STUFF ============================= #
    if state == 'game':
        screen.fill((0, 0, 0))
        
        drawGame()
    
    elif state == 'main':
        if up:
            spot -= 1
        if down:
            spot += 1
        
        menu(spot%4,right)
        
        up = down = right = False
    
    elif state == 'leaderboard':
        lb(right)
        
        right = False
        
    elif state == 'instructions':
        instructions(right)
        
        right = False

    # ============================== PYGAME STUFF (DO NOT EDIT) ============= #
    pygame.display.flip()
    pygame.time.delay(10)
pygame.quit()