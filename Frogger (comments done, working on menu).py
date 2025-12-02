#Joseph Foti (JF), Kaila Brophy (KB)

import pygame
import random
#KB: improves readability in later code by assigning shorter names to two functions; random.randint generates a random integer in a given range and random.choice returns a random value from a provided sequence   
r = random.randint
c = random.choice

#################################### CLASSES ##################################

class player(): 
    def __init__(self): 
        self.x = 500
        self.y = 700
        self.w = 50
        self.h = 1
#KB: loads the image that will be used for the frog character and scales it to size
        self.img = pygame.image.load("frog (real main).png")
        self.img = pygame.transform.scale(self.img, (110,110))
    #JF: The draw method for the player sprite, (i was too lazy to center the sprite correctly so i manually adjusted it for when it rotates)
    def draw(self):
        extraY = -11
        extraX = 1.5
        #JF: The frogs list is initialized at the beginning of the loop and contains rotated player sprites by 0,90,180,and 270 degrees respectivley
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
            
#KB: draws image of self.img (frog character) onto a position determined by the value of self.img 
        screen.blit(self.img, (self.x-extraX,self.y-extraY))
    
    def move(self,up,down,left,right):
#KB: allows the variable pos to be modified and used on a global scope instead of exclusively in this function        
        global pos
#KB: relates to movement in the y-direction; will run the first statement intially and then the value of self.y will be modified and the next elif statement will be run
        #JF: This statement covers the case of the player being on the bottom lane and actually needing to move the sprite up as opposed to moving all other elements down
        #through the global pos variable           
        if self.y == 700 and up:
            self.y -= 100
            self.img = frogs[0]
        
        #JF: if the player "moves up" the height variable pos is increased to shift all other sprites down in the display
        elif up:
            pos += 100
            lanes.append(lane(-100 - pos))
            self.img = frogs[0]
        #JF: allows the player to move from the second form the bottom lane to the bottom lane, without shifting the screen so the player cannot backtrack
        elif down:
            self.y += 100
            self.img = frogs[2]
        
        #JF: These two checks allow the player to move left and right, changing the sprite accordingly
        if right and self.x < 900:
            self.x += 100
            self.img = frogs[3]
        
        elif left and self.x > 0:
            self.x -=100
            self.img = frogs[1]
#KB: creates a class relating to the movement and position of the lanes and cars that appear at various points throughout the game         
class lane():
    
    #JF: the lane takes in a y value to place it at for convenience while initializing
    def __init__(self,y):
        global wait
        global styles
        self.direction = "no"
    
        self.y = y
        self.speed = 0
    
        self.obstacles = []
#KB: If the wait is equal to False, the program uses a series of if statements to assign values to various varibles that will later be used to determine the material of the ground; 
# the use of exclusive if statements ensures that only one of these cases applies.
  
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
#KB: uses a for loop to decide the material on the ground and how many tiles the material extends for; the range of each variable will depend on the elif statements above
#which will result in a different combination of ground materials based on the player's position.                 
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
#KB: if wait is equal to True, the else portion of the if statement will be triggered and the value of wait would be set to False; this accounts for any cases where the value of
# not wait==False, meaning that wait==True                   
        else:
            wait = False
#KB: makes the starting ground material grass if the value of start is greater than zero then lowers the value of start by one; this will make the first
#three lanes of each game grass; if start is equal to any value that does not satisfy start > 0, a random ground material will be generated.     
        global start        
        if start > 0:
            self.type = "grass"
            start -= 1
            
        else:
            self.type = c(styles)
#KB: sets up the graphics and other components specific to each ground material and makes sure only the correct obstacles and components (like trees and lilypads) are being generated on their corresponding material            
        if self.type in "grass_trees":
            
            if self.type == "trees":
                for i in range(r(5,7)):
                    self.obstacles.append(obstacle(self))
                
                removeAll(styles,"trees")
                wait = True
                
            self.bg = (121+r(-10,10),201+r(-10,10),40+r(-10,10))

        #JF: if the lany type is road, it randomly assigns a speed, direction, and amount for the cars
        elif self.type == "road":
            self.direction = c(["l","r"])
            self.bg = (0,0,0)
            self.speed = r(3,6)
            for i in range(r(2,5)):
                #JF: the obstacle 
                self.obstacles.append(obstacle(self))
        
        else:
            #JF: this else contains all water lane types, and makes it so that you cannot have two of the same water lane in a row by removing it from the pool of styles availible
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
            #JF: speeds are default initialized for going left, so if the lane is moving right the speeds are reversed
            self.speed *= -1
              
    def draw(self):
        global pos
        #JF: The lanes draw themselves as just a screenwide rectangle at their initial y value plus the position vairable tht shifts the screen as the game progresses
        pygame.draw.rect(screen, self.bg, (0, self.y+pos, 1000, 100))
        
        if self.type == "road":
            for i in lanes:
                #JF: this is the dumbest thing i've ever coded
                #If two road lanes are side by side, the road lines betweeen them are yellow if going in opposite directions and white if they travel together
                if i.y == self.y - 100 and i.type == "road":
                    color = (255,255,255)
                    
                    if self.direction != i.direction:
                        color = (255,255,0)
                    
                    #JF: this draws in the road line rectangles 
                    for i in range(-40,1041,100):
                        pygame.draw.rect(screen,color,(i,self.y + pos - 10,80,20))
#KB: creates a class containing information concerning movement of obstacles                 
class obstacle():
#KB: loads and scales images of obstacles based on the terrain; for example, if the ground material type is "trees", a file containing a tree will be loaded and added at a position on the ground   
    def __init__(self,lane):
        self.y = lane.y
        self.img = pygame.image.load("scaled.png")
        #JF: Each obstacle also contains the information of the lane it's contained in to keep movement and direction consistent (and easy for me to code)
        self.lane = lane
        self.h = 100
        self.t = self.p = False
        
        #JF: the in operator is used here for ease of readability, to just know that it's one of two lane types with no need to worry about edge cases as there are only 5 lane types 
        if lane.type in "trees_w(pad)":
            if lane.type == "trees":
                #JF: if the lane is a "trees" lane, the obstacle present is trees. WOW !
                self.img = pygame.image.load("tc scaled.png")
                self.img = pygame.transform.scale(self.img, (100,100))
            
            else:
                #JF: if the lane type is w(water) with lily pads, the "obstacle" present is lilypads
                self.img = pygame.image.load("pad.png")
                self.img = pygame.transform.scale(self.img, (95,95))
            
            #JF: randomly assigns an x value to the tree or lily pad along the lane
            self.x = r(0,9)*100
            self.w = 100
#KB: sets up moving obstacles for when the ground is water with logs or road with cars and whales        
        else:
            self.w = 0
            avoid = 0
            
            if lane.type == "road":
                #JF: forces the cars to be spaced apart
                for i in lane.obstacles:
                    avoid += i.w + 30 + r(2,3)*100
                
                #JF: adds a fun easter egg of one in 30 cars being the hipster whale (the mascot of the crossy road devs)
                if r(1,30)==1:
                    self.img = pygame.image.load("goose_scaled.png")
                    self.img = pygame.transform.scale(self.img, (152,100))
                    self.w = 160
                    
                else:
                    #JF: randomly chooses between two car sprites
                    self.img = pygame.image.load(c(["tile049.png","tile048.png"]))
                    
                    #JF: randomly decides in two checks if the car is going to become a police car or tractor 
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
                #JF: initializes the sprites for logs
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
                
                
            
            #JF: ensures all obstacles are offset form eachother an loop well
            if lane.direction == "l":
                self.x = 1400 - avoid
                
            else:
                self.x = -400 + avoid
                
                #JF: flips car sprites if they are moving left
                if lane.type == "road":
                    self.img = pygame.transform.flip(self.img, True, False)
                
                else:
                    x = self.Limg
                    self.Limg = pygame.transform.flip(self.Rimg, True, False)
                    self.Rimg = pygame.transform.flip(x, True, False)
#KB: draws the frog character and accounts for scenarios where the frog is on a moving surface, like a moving log                      
    def draw(self):
        global pos
        
        #JF: for the log type of obstacle, it begins by displaying the leftmomst log sprite and shifting right
        if self.lane.type == "w(log)":
            screen.blit(self.Limg, (self.x,self.y + pos - 5))
            
            #JF: the length of the log is detirmined by its random width assigned earlier, the amount of midsections it has is the number of 100px tiles it takes up -2
            for i in range((self.w//100)-2):
                screen.blit(self.Mimg, (self.x+(100*(i+1)),self.y + pos - 5))
            #JF: this last line adds the rightmost tile of the log
            screen.blit(self.Rimg, (self.x+(self.w-100),self.y + pos - 5))
        #Self.t is just a check to see if the car is a tractor
        elif self.t:
            #JF: the speed at which the tractor cycles between its sprites depends on the speed of the lane it is in
            if self.lane.direction == "l":
                self.img = tractorR[(self.frame//(self.lane.speed*2))%3]
            else:
                self.img = tractorL[(self.frame//(self.lane.speed*2))%3]
                
            screen.blit(self.img, (self.x,self.y+pos))
            self.frame += 1
        
        #JF: the same logic for cycling the tractors animation is used on the cop cars too
        elif self.p:
            if self.lane.direction == "l":
                self.img = oppsR[(self.frame//(self.lane.speed*3))%2]
            else:
                self.img = oppsL[(self.frame//(self.lane.speed*3))%2]
                
            screen.blit(self.img, (self.x,self.y+pos))
            self.frame += 1
        #JF: if there is no animation, the car just displays its singular sprite
        else:
            screen.blit(self.img, (self.x,self.y+pos))
    
    #JF: every frame update, the cars' x value is summed with the cars' lane's speed (which is why it was handy to have each obstacle contain the information form its lane)
    def move(self):
        self.x += self.lane.speed

#KB: sets up a class containing the name and score of the player which will be needed for the leaderboard
class person():
    def __init__(self,name,score):
        self.name = name
        self.score = score
#################################### FUNCTIONS ################################
#KB: checks to see if multiple obstacles are being placed at the same position; if the position of two obstacles is the same,
#a different value for the position of the obstacle will be generated 
def obstaclePlacementReroll(lane1,lane2):

    done = False
    
    while not done:
        done = True
        
        for i in lane1.obstacles:
            for I in lane2.obstacles:
                if i.x == I.x:
                    I.x = r(0,9)*100
                    done = False

#JF: a simple function thats probably alrady built-in that removes all instances of an entry from a list
def removeAll(i,thing):

    for x in range(i.count(thing)):
        i.remove(thing)
        
#KB: draws the lanes and the score in the top lefthand corner of the game
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
    global check
    
    screen.fill((0, 0, 0))
    screen.blit(title, [0,-7])
 #KB:prints instructions for the player on the main menu screen    
    screen.blit(titleFont.render(("use arrow keys and press right to select"), False, (53,197,0)), [300,300])
    
    #JF:sets the defaul colour of the menu selection options as well as what it changes to iff it is hovered over
    tColor1 = tColor2 = tColor3 = tColor4 = tColor5 = (53,197,0)
    hover = (212, 217, 67)
      
    if spot == 0:
        tColor1 = hover
    elif spot == 1:
        tColor2 = hover
    elif spot == 2:
        tColor3 = hover
    elif spot == 3:
        tColor4 = hover
    elif spot == 4:
        tColor5 = hover
#KB: uses a series of if statements to establish what happens when the player clicks the right arrow at each different main menu spot; spot==0 means the player has
# selected to start the game which starts the game music and prompts the user to go to shell in spyder to enter their player name.           
    if right:
        if spot == 0:
            #JF: when start game is selected, the start game text flashes a few times before beginning the game
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
#KB: restricts the acceptable inputs the player can provide for their player name through an if statement; if the player's name is greater than 6 characters,
# or the player does not input a name, they will be prompted to enter a 1-6 character name.                 
            while True:
                name = input("Enter name here: ")
                if len(name) > 9 or len(name) == 0 or " " in name:
                    print('\nname must be 1-9 characters and NO SPACES PLEASE\n')
                else:
                    break
            
            pygame.mixer.music.load("bgMusic.wav")
            pygame.mixer.music.play(-1)
            
            state = 'game'
            
            #JF: runs the function that initializes the whole game
            init()
        
        elif spot == 1:
            x = leaderboard

            leaderboard = []
            #JF: reorders (sorts) the leaderboard list of player objects to be greatest score to least
            for i in x:
                a = True
                for I in range(len(leaderboard)):
                    if int(i.score) > int(leaderboard[I].score):
                        leaderboard.insert(I,i)
                        a = False
                        break
                if a:
                    leaderboard.append(i)
            
            leaderboard = leaderboard[:10]
            
            state = 'leaderboard'
        
        elif spot == 2:
            #JF: sends you to the instructions menu
            state = 'instructions'
        
        elif spot == 3:
            #Do smth to change the sprites
            check += 1
        
        elif spot == 4:
            #JF: if done is set to True then the pygame window will close
            done = True
            
        return
        
    screen.blit(titleFont2.render(("Start game"), False, tColor1), [420,410])
    screen.blit(titleFont2.render(("Leaderboard"), False, tColor2), [420,480])
    screen.blit(titleFont2.render(("Instructions"), False, tColor3), [420,550])
    
    screen.blit(titleFont2.render(("Alternate sprites"), False, tColor4), [420,620])
    pygame.draw.rect(screen, tColor4, (710, 620, 30, 30))
    pygame.draw.rect(screen, (0,0,0), (715, 625, 20, 20))
    
    if check % 2 == 1:
        pygame.draw.rect(screen, tColor4, (718, 628, 14, 14))
    
    screen.blit(titleFont2.render(("Quit"), False, tColor5), [420,690])
    
    screen.blit(select, [370,400+(spot*70)])
#KB: defines a new function that is triggered if the player clicks the right arrow when beside the "instructions" main menu option and formats the instruction text
# into multiple lines across the screen
def instructions(right):
    global state
    
    screen.fill((0, 0, 0))
    screen.blit(title, [0,-7])
    
    screen.blit(titleFont.render(("press right to return"), False, (53,197,0)), [400,300])
    
    screen.blit(titleFont2.render(("Your goal is to use the arrow keys to "), False, (53,197,0)), [200,400])
    screen.blit(titleFont2.render(("move the frog as far as you can to get "), False, (53,197,0)), [200,470])
    screen.blit(titleFont2.render((" a high score while crossing trees, "), False, (53,197,0)), [220,540])
    screen.blit(titleFont2.render(("jumping on logs, and avoiding cars"), False, (53,197,0)), [230,610])
#KB: allows the player to return to the main menu after viewing the instructions    
    if right:
        init()
        state = 'main'
#KB: defines a function triggered if the player clicks the right arrow while beside the "leaderboard" option on the main menu; 
# if the function is triggered, the player's entered name that was previously collected in spyder will be printed beside their recorded score 
def lb(right):
    global state
    
    screen.fill((0, 0, 0))
    screen.blit(title, [0,-7])
    
    screen.blit(titleFont.render(("press right to return"), False, (53,197,0)), [400,250])
    
    for i in range(10):
        screen.blit(titleFont2.render((((str(i+1)+". ").rjust(4)+leaderboard[i].name)), False, (53,197,0)), [340,300 + (i*50)])
        screen.blit(titleFont2.render(((str(leaderboard[i].score))), False, (53,197,0)), [570,300 + (i*50)])
        
        str(leaderboard[i].score)
    
    if right:
        init()
        state = 'main'
#KB: uses if statements to set up what happens in scenarios where the player dies in the game; generates different images and sounds
#depending on how the player dies           
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
 #KB: returns to main menu after the character death scene is played   
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
#KB: setting start = 3 relates to earlier established conditions that make the first lanes generated grass; from above, when start > 0 a lane of grass will be generated
#and then the value of start will be lowered by one, meaning three lanes of grass will always be generated at the beginning of the game   
    start = 3
    
    #JF: resets the player sprite and location to default
    p = player()
    
    #JF: multiple assignment !
    up = down = left = right = wait = above = below = lSide = rSide = onLog = done = noInput = False
    
    styles = ["grass","trees","road","w(log)","w(pad)"]
    
    #JF: creates the first 9 lanes (8 on screen and one off)
    lanes = []
    for i in range(9):
        lanes.append(lane(700-(i*100)))
#################################### GLOBAL VARIABLES #########################
#KB: sets up how the game is displayed and its dimensions and rotates the images used so that they are facing the correct direction during gameplay
pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Street legal frogger")

init()
spot = 0
check = 0
reload = True
state = 'main'

frogs = []
frog = pygame.transform.scale(pygame.image.load("frog (real main).png"),(110,110))
for i in range(4):
    frogs.append(pygame.transform.rotate(frog, (i*90)))

#JF: creates every animation loop list of sprites
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

oppsR = [pygame.transform.scale(pygame.image.load(("tile059.png")), (100,100)),\
         pygame.transform.flip(pygame.transform.scale(pygame.image.load(("tile059.png")), (100,100)), False, True)]

oppsL = [pygame.transform.flip(pygame.transform.scale(pygame.image.load("tile059.png"), (100,100)), True, False),\
         pygame.transform.flip(pygame.transform.scale(pygame.image.load("tile059.png"), (100,100)), True, True)]

#JF: starts the leaderboard off with 10 scores of 0
leaderboard = []

with open("scoreList.txt") as file:
    playerData = file.read().split(" ")

for i in range(0,len(playerData),2):
    leaderboard.append(person(playerData[i],playerData[i+1]))

for i in leaderboard:
    print(i.score)
#KB: sets the scale and position of the frog on the main menu screen
select = pygame.transform.scale(pygame.image.load('scaled.png'), (65,65))

#KB: assigns variables to the sounds and fonts used throughout the game for easy referencing in the rest of the code
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
#KB: uses a while loop and if statements to determine what occurs after the game has ended 
while True:
    # ============================== HANDLE EVENTS  ========================= #
    move = True
#KB: allows the player to exit the game by breaking the loop that returns the player to the main menu; without this the player would not be able to exit the game through in-game commands     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True
            break
        
        if event.type == pygame.KEYDOWN:
            
            #JF: the purpose of the move check is to only allow one input per frame, as after being registered, move goes to false
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
#KB: uses if statements to allow player movement and movement of the cars on road spaces; if the player is on a log, they will be moved in the direction that the log is moving  
    if state == 'game':
        
        
        if check % 2 == 1:
            
            print("sprite changed wow!")
            
            check += 1
        
        for i in lanes:
            for I in i.obstacles:
                I.move()
            
        p.move(up,down,left,right)
        up = down = left = right = above = below = lSide = rSide = False

        if onLog:
            #JF: if the player is on a log, the game preserves movement by shifting the player to the log's x value plus the distance to the contact point
            p.x = logOn.x + contact
            
        else:
            #JF: if the player is not on a log, they are snapped to the closest tile of 100px
            p.x = round(p.x/100)*100
    # ============================== COLLISION ============================== #
#KB: dictates what happens when the player collides with obstacles through if statements; in the case that the object is a tree, the player will not be able to move
# onto the same square as the obstacle, whereas moving onto a water square when the player is not on a log or colliding with a car will result in character death
# this will trigger the scenarios established above for each type of character death.   
    if state == 'game':
        
        if p.y == 700:
            below = True
            
        if not (-50 < p.x < 980):
            die("a")
            
        for i in lanes:
            #JF: if a lane has been moved off screen, it is removed forom the list of lanes to prevent a buildup of checks
            if i.y + pos >= 800:
                lanes.remove(i)
        
        for i in lanes:
            #JF: if there is a tree or lily pad lane at the top of the screen and also above it, the game will ensure that the trees and lily pads do not appear on the same x value
            if i.y + pos == 0 and i.type in "trees_w(pad)":
                for I in lanes:
                    if I.y + pos == -100 and I.type in "trees_w(pad)":
                        obstaclePlacementReroll(i,I)
            
            #JF: loops the logs around the screen when they proceed all the way to one side or the other (l and r are still backwards)
            if i.type in "road_w(log)":
                for I in i.obstacles:
                    if I.x > 1400 and i.direction == "l":
                        I.x = -400
                    elif I.x < -400 and i.direction == "r":
                        I.x = 1400
            
            #JF: if two log lanes are above eachother, they will have their speeds altered to not be the same to prevent any impossible situations
            if i.y + pos == 0 and i.type in "road_w(log)":
                for I in lanes:
                    if I.y + pos == -100 and I.type in "road_w(log)":
                        while i.speed == I.speed:
                            I.speed += r(-1,1)
            
            #JF: if the payer is not on a log lane, they will be marked and not being on a log
            if i.type != "w(log)" and i.y + pos == p.y:
                onLog = False
            
            #JF: prevents a player from walking into trees
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
            
            #JF: if the player is inside the hitbox of a given car, they die.
            elif i.type == "road" and i.y + pos == p.y:
                for I in i.obstacles:
                    if I.x + I.w > p.x + 25 and I.x < p.x + p.w + 25:
                        die("car")
                        break
            
            #JF: if the player is on a water lane, they are marked to die unless ontop of an obstacle
            elif i.type in "w(pad)_w(log)" and i.y + pos == p.y:
                onWater = True
                
                for I in i.obstacles:
                    #JF: if contact is made with an obstacle, the player is snapped to the closest tile on that obstacle and that contact point is stored
                    if I.x + I.w > p.x and I.x < p.x + p.w:
                        onWater = False
                        
                        if i.type == "w(log)" and not onLog:
                            contact = round((p.x - I.x)/100)*100
                            logOn = I
                            onLog = True
                #JF: if no contact with an obstacle is made, the player dies             
                if onWater:
                    onLog = False
                    die("drown")
                    
                
                else:
                    if i.type == "w(log)":
                        onLog = True
    # ============================== DRAW STUFF ============================= #
#KB: uses a series of if statements to set up the graphics and components of the game based on which screen is being displayed
#KB: when the game is started, the previously defined functions are called upon and the graphics are set up through the drawGame function    
    if state == 'game':
        screen.fill((0, 0, 0))
        
        drawGame()
#KB: allows the player to toggle between menu options by using the up and down arrows; if the up arrow is used, the spot number will lower by one, meaning the selected option will
# be one above the one previously selected; the opposite occurs if the down arrow is pressed.    
    elif state == 'main':
        if up:
            spot -= 1
        if down:
            spot += 1
        
        menu(spot%5,right)
        
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

with open("scoreList.txt","w") as file:
    out = []
    for i in leaderboard:
        out.append(i.name)
        out.append(str(i.score))
        
    file.write(" ".join(out))
    
