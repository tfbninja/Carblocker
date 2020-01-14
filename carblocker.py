# The following 2 lines import modules.  Modules are collections of function definitions
# for you to use.  So the following two lines DEFINE a large number of useful functions.
# You can USE the functions in your code by prefixing the function name with the module
# name and a period.  So, in the code when I use pygame.display I am using the 
# function display defined in the pygame module.

import random, cmd, os
from pygame.locals import *
import pygame.font



# ------------------------------------------------------------------------------------
# This function may draw a blocker on the line that will make you crash.
# ------------------------------------------------------------------------------------
def genBlocker(screen, blockFreq, blockWidth, blockerList):

    # The random.random() function returns a random value from 0.0 to 1.0.  If this
    # value is less than the blockFreq, then we draw a block.  So, the smaller 
    # blockFreq, the less likely a blocker is drawn 
    if random.random() < blockFreq:     
        
        # Calculate the position of the blocker.  Again we use random to randomly
        # place the blocker in the window.
        pos = int(windowWidth * random.random()) - int(blockWidth / 2)
        blockerList.append([pos, windowHeight - 1])
        # Once we have the position of the blocker, draw pixels for the blocker
        #screen.fill(blockColor, [pos,windowHeight-2,blockWidth,2])
    return blockerList

def genPower(screen, powerFreq, powerColors, powerWidth, powerList):
    if random.random() < 0:#powerFreq * 50:     
        pos = int(windowWidth * random.random()) - int(powerWidth / 2)
        powerList.append([pos, windowHeight - 1, int(random.random() * len(powerColors))])
    return powerList
    
# ------------------------------------------------------------------------------------
# This function draws the car at position xpos
# ------------------------------------------------------------------------------------
def drawCar (screen, xpos, ypos, w, h, carColor, carCoordinates):
    screen.fill(carColor, [xpos - (w / 2), ypos - (h / 2), w, h])
    return [xpos - (w/2), ypos - (h / 2), xpos + w, ypos + h]

def drawBlockers(screen, blockerList, blockWidth, blockHeight):
    for blocker in blockerList:
        screen.fill(blockColor, [blocker[0],blocker[1],blockWidth,blockHeight])

def drawPowers(screen, powerList, powerWidth, powerHeight, powerColors):
    for power in powerList:
        screen.fill(powerColors[power[2]], [power[0], power[1], powerWidth, powerHeight])

def deleteBlockers(blockerList, blockHeight):
    newList = []
    for blocker in blockerList:
        if blocker[1] + blockHeight > 0:
            newList.append(blocker)
    return newList

def deletePowers(powerList, powerHeight):
    newList = []
    for power in powerList:
        if power[2] + powerHeight > 0:
            newList.append(power)
    return newList

# ----------------------------------------------------------------------------------
# This function moves the car based on the key pressed
# ----------------------------------------------------------------------------------
def moveCar (screen, carx, cary):
    
    #See if the left and right keys are down, from that move right or left
        keys=pygame.key.get_pressed()
        if keys[K_LEFT]:
                carx=carx-1
        if keys[K_RIGHT]:
                carx=carx+1
        if keys[K_UP]:
                cary=cary-1
        if keys[K_DOWN]:
                cary=cary+1

        #Make sure the car doesn't get outside of the window
        if carx<=1:
                carx=1
        if carx>=windowWidth:
                carx=windowWidth-1

        if cary<=1:
                cary=1
        if cary>=windowHeight:
                cary=windowHeight-1

        #Return the new x value
        return [carx, cary]

def moveBlockers(blockerList):
    newList = []
    for blocker in blockerList:
        newList.append([blocker[0], blocker[1] - 1])
    return newList

def movePowers(powerList):
    newList = []
    for power in powerList:
        newList.append([power[0], power[1] - 1, power[2]])
    return newList

def fadeToBlack(color, amt):
    newColor = []
    for num in color:
        if num >= amt:
            num -= amt
        else:
            num = 0
        newColor.append(int(num))
    return newColor

def fadeTransparent(color, amt):
    newColor = color
    newColor[len(newColor) - 1] -= amt
    if newColor[len(newColor) - 1] < 0:
        newColor[len(newColor) - 1] = 0
    return newColor

def isBoundedBy(point, bounds):
    if not isinstance(point, list):
        raise TypeError("'Point' must be a list with an x & y position. \"" + str(point) + "\"")
    elif not isinstance(bounds, list):
        raise TypeError("'Bounds' must be a list with two points.")
    elif not (isinstance(bounds[0], list) and isinstance(bounds[1], list)):
        raise TypeError("'Bounds' must be a list with two points as lists.")
    if point[0] > bounds[0][0] and point[1] > bounds[0][1] and point[0] < bounds[1][0] and point[1] < bounds[1][1]:
        return True
    elif point[0] > bounds[1][0] and point[1] > bounds[1][1] and point[0] < bounds[0][0] and point[1] < bounds[0][1]:
        return True
    return False

def detectCollision(carCoordinates, list, width, height):
    for item in list:
        bTopY = item[1]
        bBottomY = item[1] + blockHeight
        bLeftX = item[0]
        bRightX = item[0] + blockWidth
        cTopY = carCoordinates[1]
        cBottomY = carCoordinates[3]
        cLeftX = carCoordinates[0]
        cRightX = carCoordinates[2]
        
        if (bTopY < cBottomY and bBottomY > cTopY and bRightX > cLeftX and bLeftX < cRightX) or (isBoundedBy([cLeftX, cTopY],[[bLeftX, bTopY],[bRightX,bBottomY]])) or (isBoundedBy([cRightX, cBottomY],[[bLeftX, bTopY],[bRightX,bBottomY]])):
            if len(item) > 2:
                return item[2]
            else:
                return True
    return False

def drawScore(screen, score, font, color, carCoordinates, windowWidth, margin, y):
    # create a text suface object, 
    # on which text is drawn on it.
    txt = "Score: " + str(score)
    text = font.render(txt, True, color)
    text_width, text_height = text.get_width(), text.get_height()
    
    # create a rectangular object for the 
    # text surface object 
    x = margin

    if detectCollision(carCoordinates, [[x, y]], text_width, text_height):
        x = windowWidth - (text_width + margin)

    # copying the text surface object 
    # to the display surface object  
    # at the center coordinate. 
    screen.blit(text, [x, y])

def drawLives(screen, lives, font, color, windowWidth, windowHeight):
    # create a text suface object, 
    # on which text is drawn on it.
    txt = str(lives)
    text = font.render(txt, True, color)
    text_width, text_height = text.get_width(), text.get_height()
    
    # create a rectangular object for the 
    # text surface object 
    x = (windowWidth - text_width) / 2
    y = (windowHeight - text_height) / 2

    # copying the text surface object 
    # to the display surface object  
    # at the center coordinate.
    if (len(color) > 3):
        alpha_img = pygame.Surface(text.get_rect().size, pygame.SRCALPHA)
        alpha_img.fill((255, 255, 255, color[3] / 255 * 100))
        text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(text, [x, y]) 
    
    

#------------------------------------------------------------------------------------
# This is where the function definitions cease and the first bit of code begins
# executing
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# Initialize outer-level variables - These variables are used throughout the program and
# when they are defined here they are available in all functions and code.
#-------------------------------------------------------------------------------------

BLACK  = [0,   0,   0  ]
WHITE  = [255, 255, 255]
RED    = [255, 0,   0  ]
GREEN  = [0,   255, 0  ]
BLUE   = [0,   0,   255]
ORANGE = [252, 102, 3  ]
YELLOW = [252, 248, 3  ]
PURPLE = [248, 3,   252]
LIME   = [153, 255, 89 ]

screenBG = BLACK
livesColor = [0, 0, 0, 255]

windowWidth = 500     # The game window width
windowHeight = 800        # The game window height

pygame.font.init()
scoreFont = pygame.font.SysFont('dejavuserif', 32)
livesFont = pygame.font.SysFont('dejavusans', 64)
finalScoreFont = pygame.font.SysFont('impact', 45)

loopCount = 0   # The number of times the game's main loop has executed
secondsPassed = 0   # The seconds that have passed since the main loop started running
clockSpeed = 100    # Since this value is subject to change every level, we're making it a variable

blockWidth = 10                   # The width of the blockers
blockHeight = 2                   # The height of the blockers
blockColor = RED                  # The blocker color
blockFreq = 0.10                  # A blockers has a 10% chance of appearing every frame

powerWidth = 15                           # The width of the powerups
powerHeight = 15                          # The height of the powerups
powerColors = [LIME,PURPLE,ORANGE]  # Powerup colors by type
powerFreq = 0.0001                        # A powerup has a 0.1% chance of appearing every frame

carColor = BLUE # The car color

carStart = [windowWidth / 2, 75]
carx,cary = carStart   # Where is the car in the window
carw = 2
carh = 4
carCoordinates = [] # The actual screen positions of the top left,  bottom right corners of the car

lives = 3

blockerList = [] # list of blocker positions, [[blocker1_X, blocker1_Y], [blocker2_X, blocker2_Y]...]
powerList = [] # list of power-up positions and types, [[power1_type, power1_X, power1_Y], [power2_type, power2_X, power2_Y]...]

activePowerTimes = [0] * len(powerColors) # list of seconds left of each powerup type, 0 if not active

#Initialize pygame
pygame.init()
pygame.display.set_caption("Carblocker")
    
#Set the size of the window
size = [windowWidth,windowHeight]
screen = pygame.display.set_mode(size)
    
#Do not Display the mouse
pygame.mouse.set_visible(0)

#Seed the random number generator, this lets the game play differently every time you start it up
random.seed()

#Initialize the clock
clock = pygame.time.Clock()

#Keep going until I say I am done by clicking the close button or pressing the escape key
done = False

#Main Loop
while not done:
    loopCount += 1
    secondsPassed = loopCount / clockSpeed
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    #Slow down the game, so that this the frame updates only 100 times a second.  This
    #controls the speed of the game.  If you increase or decrease this value, you 
    #will speed up and slow down the game.  Also based on this value, you know how
    #many seconds you have been playing for.  If you incremented a counter every loop,
    #and divided that by the value passed to clock.tick (the number in parentheses),
	#you would know how many seconds you have been playing for. 
	#seconds playing=counter/clockSpeed
    clock.tick(clockSpeed)
    
    # Create a blocker
    blockerList = genBlocker(screen, blockFreq, blockWidth, blockerList)

    # Create a powerup
    powerList = genPower(screen, powerFreq, powerColors, powerWidth, powerList)

    # Move the current screen up by 1
    #screen.blit(screen, [0,0], [0,1,windowWidth,windowHeight-1])
    #..... no......
    
    # Clear everything to black so that the game can be re-drawn
    screen.fill(screenBG, [0,0,windowWidth,windowHeight])
    screenBG = fadeToBlack(screenBG, 2)
    livesColor = fadeTransparent(livesColor, 1)

    
    # Move and draw the car
    carx,cary = moveCar(screen, carx, cary)   

    # Draw the car in the new position
    carCoordinates = drawCar(screen, carx, cary, carw, carh, carColor, carCoordinates)

    # Draw the blockers
    drawBlockers(screen, blockerList, blockWidth, blockHeight)

    # Draw the score
    drawScore(screen, int(secondsPassed), scoreFont, GREEN, carCoordinates, windowWidth, 5, 3)

    # Draw the life count
    drawLives(screen, int(lives), livesFont, livesColor, windowWidth, windowHeight)

    # Draw the powerups
    drawPowers(screen, powerList, powerWidth, powerHeight, powerColors)

    blockerList = deleteBlockers(blockerList, blockHeight)
    blockerList = moveBlockers(blockerList)

    powerList = deletePowers(powerList, powerHeight)
    powerList = movePowers(powerList)

    if detectCollision(carCoordinates, blockerList, blockWidth, blockHeight) != False:
        lives -= 1
        blockerList.clear()
        screenBG = RED
        livesColor = [0, 0, 0, 255]
        carx,cary = carStart

        if lives < 1:
            screen.fill([110, 0, 0], [0,0,windowWidth, windowHeight])
            drawLives(screen, "FINAL SCORE: " + str(int(secondsPassed)), finalScoreFont, BLACK, windowWidth, windowHeight)
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit(0)
    
    powerBufferVar = detectCollision(carCoordinates, powerList, powerWidth, powerHeight)
    if powerBufferVar != False:
        activePowerTimes[powerBufferVar] += 15 * clockSpeed
        print(powerBufferVar)
    
    for i in range(len(activePowerTimes)):
        blockWidth = 10
        if activePowerTimes[i] > 0:
            activePowerTimes[i] -= 1
            if i == 0:
                newList = []
                for blocker in blockerList:
                    margin = 25
                    if not (blocker[0] + blockWidth > carx - margin and blocker[0] < carx + margin):
                        newList.append(blocker)
                blockerList = newList
            elif i == 1:
                secondsPassed += 15
            elif i == 2:
                blockWidth = 2


    #Display the new screen
    pygame.display.flip()

#Uninitialize and destroy the window
pygame.quit()