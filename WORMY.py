import pygame,random,sys #imports the pygame,random and sys module in our script
from pygame.locals import * #imports the pygame.locals module into our script which contains no function but simply all the keyboard constants

FPS = 15 # frame speed is set to 15 means 15 frames(images) will be drawn per second
WINDOWWIDTH = 640 #windowwidth is set to 640 pixels 
WINDOWHEIGHT = 480 #windowheight is set to 480 pixels
CELLSIZE = 20 #cellwidth and cellheight is 20 pixels
assert WINDOWWIDTH%CELLSIZE==0,"there should be an integral number of cells along the width" #there should be integral number of cells on the board
assert WINDOWHEIGHT%CELLSIZE==0,"there should be an integral number of cells along the height" 
CELLWIDTH = int(WINDOWWIDTH/CELLSIZE) #number of cells across the width
CELLHEIGHT = int(WINDOWHEIGHT/CELLSIZE) #number of cells across the height

WHITE=(255,255,255) #sets the rgb color code for white
BLACK=(0,0,0) #sets the rgb color code for black
RED=(255,0,0) #sets the rgb color code for red
GREEN=(0,255,0) #sets the rgb color code for green
DARKGREEN=(0,155,0) #sets the rgb color code for darkgreen
DARKGRAY=(40,40,40) #sets the rgb color code for darkgray
BGCOLOR=BLACK #sets the background color to black

UP="up" # variable storing the string up
DOWN="down"  # variable storing the string down
LEFT="left"  # variable storing the string left
RIGHT="right"  # variable storing the string right

HEAD=0 #keeps the track of the worm's head

def main(): #function main
    global FPSCLOCK,DISPLAYSURF,BASICFONT #global variables FPSCLOCK,DISPLAYSURF,BASICFONT which can be used in any function
    pygame.init() # initialising the pygame module to use it's functionality
    FPSCLOCK=pygame.time.Clock() #seting up the clock object whose's tick method controls the frame speed
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) #set's up a screen which is 640 pixels wide and 480 pixels tall
    BASICFONT=pygame.font.Font(None,18) #setting up the font object having a font styling of none and a font size of 18 pixels
    pygame.display.set_caption("WORMY") #sets the caption of pygame window
     
    showStartScreen() #begins the game with an animation (wormy animation)
    while True: #infinite loop
        runGame() #begins the game
        showGameOverScreen() #shows the animation indicating the end of game

'''there are 3 main functions of the game ,first is runGame for running the game,one is showStartScreen which shows the welcome animation and and showGameOverScreen which indicates the end of the game by showing an animation'''

def runGame(): ## function responsible for running the game
    startx = random.randint(5,CELLWIDTH-6) # selects a random cell not too close to the borders
    starty = random.randint(5,CELLHEIGHT-6)
    wormCoords=[{'x':startx,'y':starty},{'x':startx-1,'y':starty},{'x':startx-2,'y':starty}] # each segment of the snake is represented by a dictionary which further has 2 keys the x and y coordinate of that particular segment
    direction=RIGHT # starts moving in the right direction

    apple = getRandomLocation() #sets the random location for an apple

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==KEYDOWN:
                if (event.key==K_DOWN or event.key==K_s) and direction!=UP:
                    direction=DOWN
                elif (event.key==K_UP or event.key==K_w) and direction!=DOWN:
                    direction=UP
                elif (event.key==K_LEFT or event.key==K_a) and direction!=RIGHT:
                    direction=LEFT
                elif (event.key==K_RIGHT or event.key==K_d) and direction!=LEFT:
                    direction=RIGHT
                elif event.key==K_ESCAPE:
                    terminate()
            if wormCoords[HEAD]['x']==-1 or wormCoords[HEAD]['x']==CELLWIDTH or wormCoords[HEAD]['y']==-1 or wormCoords[HEAD]['y']==CELLHEIGHT:
                return
            for wormBody in wormCoords[1:]:
                if wormBody['x']==wormCoords[HEAD]['x'] and wormBody['y']==wormCoords[HEAD]['y']:
                    return
            ## if the coordinates of the body's head and the apple matches then we need to get a new random location of the apple and also don't interfere with size as we will add a new head which results in an increase in size.    
            if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
                apple = getRandomLocation()
            else:
                del wormCoords[-1] ## else reduce the size by one unit but size remains the same as a new head is added in the direction of movement
            if direction==UP:
                newHead = {'x':wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y']-1}
            elif direction==DOWN:
                newHead = {'x':wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y']+1}
            elif direction==LEFT:
                newHead = {'x':wormCoords[HEAD]['x']-1,'y':wormCoords[HEAD]['y']}
            else:
                newHead = {'x':wormCoords[HEAD]['x']+1,'y':wormCoords[HEAD]['y']}
            wormCoords.insert(0,newHead)
            ## fills the screen with black background color
            DISPLAYSURF.fill(BGCOLOR)
            ## draws the grid onto the screen
            drawGrid()
            ## draws the worm onto the screen
            drawWorm(wormCoords)
            ## draws the apple onto the screen
            drawApple(apple)
            ## draws the game score onto the screen
            drawScore(len(wormCoords)-3)
            ## updates the game state so that it also updates onto the screen
            pygame.display.update()
            ## controls the speed of the game
            FPSCLOCK.tick(FPS)
            
def drawPressKeyMsg():
    ## returns a new surface object
    pressKeySurf = BASICFONT.render('Press a key to play',True,DARKGRAY)
    ## returns the by default coordinates of this surface with topleft being 0,0
    pressKeyRect = pressKeySurf.get_rect()
    ## sets the topleft coordinates according to our need so that it can be easily blitted onto the the displaysurface at the bootom right coordinates
    pressKeyRect.topleft = (WINDOWWIDTH-200,WINDOWHEIGHT-30)
    ## pastes the surface onto the displaysurface
    DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT))>0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents)==0:
        return None
    if keyUpEvents[0].key==K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def terminate():
    pygame.quit()
    sys.exit()

def showStartScreen():
    ## creates a new font object which has a font style of freesansbold.ttf and a font size of 100pixels
    titleFont = pygame.font.Font('freesansbold.ttf',100)
    ## creates a surface object1
    titleSurf1 = titleFont.render('Wormy!',True,WHITE,DARKGREEN)
    ## creates a surface object 2
    titleSurf2 = titleFont.render('Wormy!',True,GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:## animation
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1=pygame.transform.rotate(titleSurf1,degrees1)
        rotatedRect1=rotatedSurf1.get_rect()
        rotatedRect1.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2)
        DISPLAYSURF.blit(rotatedSurf1,rotatedRect1)

        rotatedSurf2=pygame.transform.rotate(titleSurf2,degrees2)
        rotatedRect2=rotatedSurf2.get_rect()
        rotatedRect2.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2)
        DISPLAYSURF.blit(rotatedSurf2,rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return

        degrees1+=3
        degrees2+=7

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getRandomLocation():
    return {'x':random.randint(0,CELLWIDTH-1),'y':random.randint(0,CELLHEIGHT-1)}

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf',150)
    gameSurf = gameOverFont.render('Game',True,WHITE)
    overSurf = gameOverFont.render('Over',True,WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH/2,10)
    overRect.midtop = (WINDOWWIDTH/2,10+gameRect.height+25)
    DISPLAYSURF.blit(gameSurf,gameRect)
    DISPLAYSURF.blit(overSurf,overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(1000)
    checkForKeyPress()
    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def drawScore(score):
    scoreSurf=BASICFONT.render("Score : %s"%(score),True,WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH-120,10)
    DISPLAYSURF.blit(scoreSurf,scoreRect)

def drawGrid():
    for x in range(0,WINDOWWIDTH,CELLSIZE):
        pygame.draw.line(DISPLAYSURF,DARKGRAY,(x,0),(x,WINDOWHEIGHT))
    for y in range(0,WINDOWHEIGHT,CELLSIZE):
        pygame.draw.line(DISPLAYSURF,DARKGRAY,(0,y),(WINDOWWIDTH,y))

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x']*CELLSIZE
        y = coord['y']*CELLSIZE
        wormSegmentRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,DARKGREEN,wormSegmentRect)
        wormInnerSegmentRect=pygame.Rect(x+4,y+4,CELLSIZE-8,CELLSIZE-8)
        pygame.draw.rect(DISPLAYSURF,GREEN,wormInnerSegmentRect)

        
def drawApple(coord):
    x=coord['x']*CELLSIZE
    y=coord['y']*CELLSIZE
    appleRect=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(DISPLAYSURF,RED,appleRect)
    
main()

                
                
            
