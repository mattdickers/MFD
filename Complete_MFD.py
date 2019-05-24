import krpc
import math
import pygame
from pygame.locals import *
import sys
import time
import wernher
import numpy as np
from colorsList import c

pygame.init()

pygame.display.set_caption("MFD")
icon = pygame.image.load(r"pictures\icon.png")
pygame.display.set_icon(icon)

width  = 1204
height = 768
screen = pygame.display.set_mode((width, height),HWSURFACE|DOUBLEBUF|RESIZABLE)

scale            = 0.1
activeButton     = ""
activeScroll     = [0, 0]
selectScroll     = []
returned         = ""
screenShowing    = "home"
dialogueBox      = None
oldDialogueBox   = None
clicked          = None
click            = [0, 0, 0]
PI               = math.pi
TWOPI            = 2 * PI
HALFPI           = PI / 2
selected         = 0
conn             = None
buttonType       = 0
lineList         = []
powerRunOnce     = 0
runOnce          = 0
runOnce1         = 0
error            = ""
vesselSelect     = 0
vesselScroll     = 0
experimentSelect = 0
experimentScroll = 0
allowErrors      = False # true to allow errors, false to crash upon errors

# graph screen variables
completed        = 1
graphSettings    = []
xLimit           = 0
altList          = []
velList          = []
radAltList       = []
altLimit         = 0
velLimit         = 0
radAltLimit      = 0

touchScreen  = None
fullscreen   = None
sideButtons  = None
mainSettings = ["", "", ""]


extraScreens        = ["science", "maneuver", "graph", "engine"] # this is for the settings dialogue on the home screen
showBox             = "main"
screenShortcut      = ""
buttonToEdit        = ""
homeScreenFunctions = ["", "", ""]

times = []
transmit = False

planetColors = {"Sun":(255,240,0),"Kerbol":(255,240,0),"Moho":(95,76,65)
                 ,"Eve":(135,75,161),"Gilly":(116,102,91),"Kerbin":(30,60,200)
                 ,"Mun":(94,96,95),"Minmus":(97,147,128),"Duna":(111,47,27)
                 ,"Ike":(91,90,91),"Dres":(157,152,151),"Jool":(70,130,30)
                 ,"Laythe":(49,103,148),"Vall":(126,170,172),"Tylo":(167,157,143)
                 ,"Bop":(102,87,78),"Pol":(238,207,155),"Eeloo":(205,217,218)}


leftAlign = 90
topAlign = 0

buttonList = []
scrollButtonList = []

mousePos = (0, 0)

font      = pygame.font.SysFont("monospace", 20)
bigFont   = pygame.font.SysFont("monospace", 50)
smallFont = pygame.font.SysFont("monospace", 16)

logo = pygame.image.load(r"pictures\logo.bmp")

orbitButton    = pygame.image.load(r"pictures\orbit data button.bmp")
flightButton   = pygame.image.load(r"pictures\flight data button.bmp")
resourceButton = pygame.image.load(r"pictures\resources button.bmp")
genericButton  = pygame.image.load(r"pictures\generic button.bmp")
yesButton      = pygame.image.load(r"pictures\yes button.bmp")
noButton       = pygame.image.load(r"pictures\no button.bmp")
homeButton     = pygame.image.load(r"pictures\home button.bmp")
powerButton    = pygame.image.load(r"pictures\power button.bmp")

joystickButton1 = pygame.image.load(r"pictures\up button.bmp")
joystickButton2 = pygame.image.load(r"pictures\right button.bmp")
joystickButton3 = pygame.image.load(r"pictures\down button.bmp")
joystickButton4 = pygame.image.load(r"pictures\left button.bmp")

materialsBayImage      = pygame.image.load(r"pictures\materials bay.bmp")
mysteryGooImage        = pygame.image.load(r"pictures\mystery goo.bmp")
accelerometerImage     = pygame.image.load(r"pictures\accelerometer.bmp")
barometerImage         = pygame.image.load(r"pictures\barometer.bmp")
gravityDetectorImage   = pygame.image.load(r"pictures\gravity detector.bmp")
thermometerImage       = pygame.image.load(r"pictures\thermometer.bmp")
atmosphereSensorImage  = pygame.image.load(r"pictures\atmosphere sensor.bmp")
asteroidTelescopeImage = pygame.image.load(r"pictures\asteroid telescope.bmp")
moddedPartImage        = pygame.image.load(r"pictures\modded_part.bmp")
scrollUpImage          = pygame.image.load(r"pictures\scroll up.bmp")
scrollDownImage        = pygame.image.load(r"pictures\scroll down.bmp")
runExperimentImage     = pygame.image.load(r"pictures\run.bmp")
transmitData           = pygame.image.load(r"pictures\transmit.bmp")
recycleExperiment      = pygame.image.load(r"pictures\recycle experiment.bmp")
settingsIcon           = pygame.image.load(r"pictures\settings icon.bmp")

Ap_markerL             = pygame.image.load(r"pictures\Ap_markerL.png")
Pe_markerL             = pygame.image.load(r"pictures\Pe_markerL.png")
Ap_markerM             = pygame.image.load(r"pictures\Ap_markerM.png")
Pe_markerM             = pygame.image.load(r"pictures\Pe_markerM.png")
Ap_markerS             = pygame.image.load(r"pictures\Ap_markerS.png")
Pe_markerS             = pygame.image.load(r"pictures\Pe_markerS.png")

vesselManned           = pygame.image.load(r"pictures\vessel manned.bmp")
relayImage             = pygame.image.load(r"pictures\relay.bmp")
KSCimage               = pygame.image.load(r"pictures\KSC image.bmp")
noSignal               = pygame.image.load(r"pictures\no signal.bmp")



# draws rectangles planning on adding more
def rectFunc(pos, size, borderWidth, borderColor, innerColor, defPos = "topLeft") :
    rectPos = [0, 0]
    rectPos[0], rectPos[1] = pos[0], pos[1]

    if defPos == "centre" :
        rectPos[0] = pos[0] - size[0] / 2
        rectPos[1] = pos[1] - size[1] / 2

        rectPos[0] = int(rectPos[0])
        rectPos[1] = int(rectPos[1])

    area = pygame.Rect((rectPos[0], rectPos[1]), (size[0], size[1]))

    if innerColor is not None:
        pygame.draw.rect(screen, innerColor, area)

    pygame.draw.rect(screen, borderColor, area, 1)

    # if color2 is not None
    if innerColor is not None :
        if borderWidth != 1 :
            for i in range(0, borderWidth):
                area = pygame.Rect((rectPos[0] + (i - 1), rectPos[1] + (i - 1)),
                                   (size[0] - (2 * (i - 1)), size[1] - (2 * (i - 1))))
                pygame.draw.rect(screen, borderColor, area, 1)


def textFunc(text, textColor, pos, direc = "left", fontSize = 20) :
    textFont = pygame.font.SysFont("monospace", fontSize)

    if direc == "centre" :
        posX = (pos[0] - textFont.size(text)[0] / 2)
    elif direc == "right" :
        posX = (pos[0] - textFont.size(text)[0])
    elif direc == "." and "." in text :
        distToDec = len(text.split(".")[0]) * (textFont.size(text)[1] / 2)
        posX = (pos[0] - distToDec)
    else:
        posX = pos[0]
    # create text object
    textObject = textFont.render(text, False, textColor)
    # add/render the text to screen
    screen.blit(textObject, (posX, pos[1]))


def distBetween(point1, point2) :
    diffVec = [point2[0] - point1[0], point2[1] - point1[1]]
    diffVec[0] = abs(diffVec[0])
    diffVec[1] = abs(diffVec[1])

    diffMagOut = math.sqrt(diffVec[0] **2 + diffVec[1] **2)

    return diffMagOut


def angleBetween(point1, point2) :
    xDist = point2[1] - point1[1]
    yDist = point2[0] - point1[0]
    angle = 0

    try :
        angle = math.atan(xDist / yDist) / PI * 180
    except ZeroDivisionError :
        pass

    return angle


# converts seconds to formatted clock string
def timeConvert(seconds, value=None):
    m, s = divmod(seconds, 60)
    #return "%02d:%02d:%02d" % (h, m, s)
    if value == "m" :
        return "%02d:%02d" % (m, s)
    elif value == "h" :
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)
    elif value == "d" :
        h, m = divmod(m, 60)
        d, h = divmod(h, 6)
        return str(int(d)) + "d," + "%02d:%02d:%02d" % (h, m, s)
    elif value == "y" :
        h, m = divmod(m, 60)
        d, h = divmod(h, 6)
        y, d = divmod(d, 426)
        return str(int(y)) + "y," + str(int(d)) + "d," + "%02d:%02d:%02d" % (h, m, s)

    elif value == "smart" :
        # if less than a day (6 hours)
        if seconds < 21600 :
            h, m = divmod(m, 60)
            return "%02d:%02d:%02d" % (h, m, s)
        # if less than a year
        elif seconds < 9201600 :
            h, m = divmod(m, 60)
            d, h = divmod(h, 6)
            return str(int(d)) + "d," + "%02d:%02d:%02d" % (h, m, s)

        else :
            h, m = divmod(m, 60)
            d, h = divmod(h, 6)
            y, d = divmod(d, 426)
            return str(int(y)) + "y," + str(int(d)) + "d," + "%02d:%02d:%02d" % (h, m, s)

    elif value is None :
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)


def siFormat(num, sigFigs = 7) :
    #num = round(num)

    if num > 1000000000 :
        return str(int(num / 1000000000)) + "G"
    elif num > 1000000 :
        return str(int(num / 1000000)) + "M"
    elif num > 1000 :
        return str(int(num / 1000)) + "k"
    elif num < 1000 :
        return '%s' % float(str("%." + str(sigFigs) + "g") % num)
    elif num < 1 :
        return str(int(num / 1000)) + "m"
    elif num < 1 :
        return str(int(num / 1000000)) + "µ"
    elif num < 1 :
        return str(int(num / 1000000000)) + "n"

    #numRet = '%s' % float(str("%." + str(3) + "g") % num)


def hyperbola(hyperbolaPos, semiMaj, semiMin, soiRadius):
    xVal = math.sqrt((semiMin ** 2 * (soiRadius ** 2 * semiMin ** 2 + soiRadius ** 2 * semiMaj ** 2 + 2 * soiRadius *
                                      semiMaj ** 3 + 2 * soiRadius * semiMin ** 2 * semiMaj - semiMin ** 4 - semiMin ** 2 *
                                      semiMaj ** 2)) / (semiMin ** 4 + 2 * semiMin ** 2 * semiMaj ** 2 + semiMaj ** 4))

    detail      = 100 # number of steps
    step        = (xVal * 2.1) / detail # size of each step
    stepAcc     = -xVal - (xVal * 0.05) # start point

    # init
    points = []
    hyperbolaPosX = hyperbolaPos[0]
    hyperbolaPosY = hyperbolaPos[1]

    for i in range(detail):
        stepAcc += step
        point    = []

        # x values are linear
        hyperbolaX = stepAcc
        point.append(hyperbolaX)
        # y values follow rearranged hyperbola equation
        hyperbolaY = (semiMaj * math.sqrt((semiMin ** 2) + (hyperbolaX ** 2))) / semiMin
        point.append(hyperbolaY)

        # debugging aids
        #drawCross(c["green"], (point[0] + hyperbolaPosX, point[1] + hyperbolaPosY), 1)
        #if i == 49 :
        #    pygame.draw.line(screen, c["darkRed"], (0 + hyperbolaPosX, focusCentre + hyperbolaPosY), (point[0] + hyperbolaPosX, point[1] + hyperbolaPosY))
        #angle = angleBetween((0 + hyperbolaPosX, focusCentre + hyperbolaPosY), (point[0] + hyperbolaPosX, point[1] + hyperbolaPosY))
        #print(str(i) + " " + str(angle))

        point[0] += hyperbolaPosX
        point[1] += hyperbolaPosY

        points.append(point)

    return points


# cross drawing
def drawCross(givenColor, crossPos, size=5, width=1):
    pos = list(crossPos)

    pygame.draw.line(screen, givenColor, (pos[0] + size, pos[1] + size), (pos[0] - size, pos[1] - size), width)
    pygame.draw.line(screen, givenColor, (pos[0] - size, pos[1] + size), (pos[0] + size, pos[1] - size), width)


def rotatePolygon(polygon, theta, pos):
    # note : theta in degrees
    theta = math.radians(theta)
    output = []

    for point in polygon:
        output.append((point[0] * math.cos(theta) - point[1] * math.sin(theta) + pos[0],
                       point[0] * math.sin(theta) + point[1] * math.cos(theta) + pos[1]))

    return output


# translate points list by polar coodinates
def polarTranslate(pointsList, angle, radius) :
    # note: angle in degrees
    angle = math.radians(angle)
    newPointsList = []

    for point in pointsList :
        pointX, pointY = point[0], point[1]

        # adds x translation multiplied by distance
        pointX = pointX + (math.cos(angle) * radius)

        # adds y translation multiplied by distance
        pointY = pointY + (math.sin(angle) * radius)

        # sets output variables
        newPoint = [pointX, pointY]
        newPointsList.append(newPoint)

    return newPointsList


def translate(pointsList, pos) :
    pointsListNew = []

    for point in pointsList :
        #print(point)
        newPoint = [point[0], point[1]]
        newPoint[0] = point[0] + pos[0]
        newPoint[1] = point[1] + pos[1]

        pointsListNew.append(newPoint)

    return pointsListNew


# draw flat ellipses
def ellipse(ellipsePos, radius, height, cross) :
    crossPoint = [0, 0]
    
    detail = 100
    step = (2 * PI) / detail
    stepAcc = 0

    ellipsePosX = ellipsePos[0]
    ellipsePosY = ellipsePos[1]

    points = [0 for i in range(detail)]

    for i in range(0, detail):
        points[i] = ellipsePosX + radius * math.cos(stepAcc), ellipsePosY - height * radius * math.sin(stepAcc)
        stepAcc = stepAcc + step
    
    if cross[0]:
        crossPoint = [ellipsePosX + radius * math.cos(cross[1]), ellipsePosY - height * radius * math.sin(cross[1])]

        # the code doesnt draw a cross here because the crosspos is used to draw the moons

    return {"points":points, "crossPos":crossPoint}


# draws half ellipses
def halfEllipse(givenColor, ellipsePos, radius, height, width, startPoint, endPoint, angle):
    # number of points
    detail = 100
    # angle between each point
    step = endPoint / detail
    # accumulation of angle
    stepAcc = 0

    ellipsePosX = ellipsePos[0]
    ellipsePosY = ellipsePos[1]

    # initialise array with length detail
    points = [None] * detail

    for x in range(0, detail):
        points[x] = [width * radius * math.cos(stepAcc), height * radius * math.sin(stepAcc)]

        stepAcc = stepAcc + step

    rotatedLine = rotatePolygon(points, angle, (ellipsePosX, ellipsePosY))

    pygame.draw.lines(screen, givenColor, False, rotatedLine, 1)


# draws a nav-ball
def navBall(pos, roll, pitch, yaw, radius):
    # rollAngle  = roll
    # pitchAngle = pitch
    # yawAngle   = yaw

    # outer ring (the stationary border part)
    points = ellipse(pos, radius, 1, (False, 0, 0))["points"]
    pygame.draw.lines(screen, c["white"], True, points)

    pitchAngle = []
    yawAngle = []

    # if pitch > 90 and pitch < 270 :
    #    pitch = 90

    roll = math.radians(roll)
    pitch = math.radians(pitch)
    yaw = math.radians(yaw)

    # math.sin(pitch)

    pitchAngle.append(math.sin(-pitch))
    pitchAngle.append(math.sin(pitch + HALFPI))
    pitchAngle.append(math.sin(-pitch + PI))
    pitchAngle.append(math.sin(pitch + PI + HALFPI))

    yawAngle.append(math.sin(-yaw))
    yawAngle.append(math.sin(yaw + HALFPI))
    yawAngle.append(math.sin(-yaw + PI))
    yawAngle.append(math.sin(yaw + PI + HALFPI))

    if pitch < HALFPI or pitch > 1.5 * PI:
        halfEllipse(c["white"], (pos[0], pos[1]), radius, pitchAngle[0], 1, 0, PI, math.degrees(roll))

    if pitch < PI:
        halfEllipse(c["white"], (pos[0], pos[1]), radius, pitchAngle[1], 1, 0, PI, math.degrees(roll))

    if HALFPI < pitch < 1.5 * PI:
        halfEllipse(c["white"], (pos[0], pos[1]), radius, pitchAngle[2], 1, 0, PI, math.degrees(roll))

    if pitch > PI:
        halfEllipse(c["white"], (pos[0], pos[1]), radius, pitchAngle[3], 1, 0, PI, math.degrees(roll))

    # halfEllipse(c["white, (pos[0], pos[1]), 100, math.degrees(yaw), 1, 0, PI, math.degrees(roll +HALFPI))

    if yaw < HALFPI or yaw > 1.5 * PI:
        halfEllipse(c["white"], (pos[0], pos[1]), radius, yawAngle[0], 1, 0, PI, math.degrees(roll + HALFPI))

    if yaw < PI:
        halfEllipse(c["white"], (pos[0], pos[1]), radius, yawAngle[1], 1, 0, PI, math.degrees(roll + HALFPI))

    if HALFPI < yaw < 1.5 * PI:
        halfEllipse(c["white"], (pos[0], pos[1]), radius, yawAngle[2], 1, 0, PI, math.degrees(roll + HALFPI))

    if yaw > PI:
        halfEllipse(c["white"], (pos[0], pos[1]), radius, yawAngle[3], 1, 0, PI, math.degrees(roll + HALFPI))

    # halfEllipse(c["white, (pos[0], pos[1]), 100, pitch, 1, 0, PI, 0)
    # halfEllipse(c["white, (pos[0], pos[1]), 100, pitch - 1, 1, 0, PI, 0)


# makes a list of buttons
def newButton(pos, size, name, givenButtonType=0, regPos=(0, 0), title="", drawTime="front"):
    # regPos is for the scroll buttons

    # adds normal button
    if givenButtonType == 0:
        buttonList.append((pos, size, name, title, drawTime))
    # adds joystick-able button
    elif givenButtonType == 1:
        scrollButtonList.append((pos, size, name, regPos, title, drawTime))


# function to clear the buttons
def clearScrollButtons(buttonNames):
    global scrollButtonList

    if buttonNames is None :
        buttonNames = ["all"]
    
    if buttonNames[0] == "all":
        scrollButtonList = []
    else:
        for i in range(0, len(buttonNames)):
            for j in range(0, len(scrollButtonList)):
                if buttonNames[i] == scrollButtonList[j][2]:
                    del (scrollButtonList[j][2])


# function to clear the buttons
def clearButtons(buttonNames) :
    global buttonList

    if buttonNames[0] == "all" :
        if touchScreen :
            del (buttonList[14:])
        if not touchScreen :
            del (buttonList[18:])

    if buttonNames == "reset" :
        buttonList = []

    # runs through all button names given by function call
    for i in range(0, len(buttonNames)) :
        # runs through all buttons on screen
        for j in range(0, len(buttonList)) :
            # compares given names against buttons' names

            try :
                if buttonNames[i] == buttonList[j][2] :
                    del (buttonList[j])
            except IndexError :
                pass


# checks input co-ords against all button areas
def checkButtons(pos):
    # find number of buttons
    length = len(buttonList)

    # runs loop once for each button
    for x in range(0, length):

        # checks if mouse pos is higher than lowest button positions
        if pos[0] >= buttonList[x][0][0] and pos[1] >= buttonList[x][0][1]:

            # checks if mouse pos is below right and bottom of button
            if pos[0] <= buttonList[x][0][0] + buttonList[x][1][0] and pos[1] <= buttonList[x][0][1] + buttonList[x][1][
                1]:
                # return button name
                return buttonList[x][2]


def checkScrollButtons(selectedRegPos):
    length = len(scrollButtonList)

    # this bit checks the slected button against the list and returns the name of the currently selected one
    for x in range(0, length):

        # checks selected button (selectedregPos against the list items)
        if selectedRegPos[0] == scrollButtonList[x][3][0] and selectedRegPos[1] == scrollButtonList[x][3][1]:
            # return button name
            return scrollButtonList[x][2]


# checks that the highlighted button is within the button list
def selectScrollCheck(selectedRegPos):
    length = len(scrollButtonList)

    xList = []
    yList = []
    xMax = 0
    xMin = 0
    yMax = 0
    yMin = 0

    for i in range(0, length):
        xList.append(scrollButtonList[i][3][0])
        yList.append(scrollButtonList[i][3][1])

    if xList :
        xMax = max(xList)
        xMin = min(xList)

    if yList :
        yMax = max(yList)
        yMin = min(yList)

    if selectedRegPos[0] > xMax:
        selectedRegPos[0] = xMax
    if selectedRegPos[0] < xMin:
        selectedRegPos[0] = xMin

    if selectedRegPos[1] > yMax:
        selectedRegPos[1] = yMax
    if selectedRegPos[1] < yMin:
        selectedRegPos[1] = yMin

    return selectedRegPos


# draws the buttons
def drawButtons(buttonDrawTime="front"):
    # find number of buttons
    length = len(buttonList)
    # runs loop once for each button
    for x in range(0, length):
        area = pygame.Rect(buttonList[x][0][0], buttonList[x][0][1],
                           buttonList[x][1][0], buttonList[x][1][1])
        buttonPos = (area[0], area[1])
        buttonSize = (area[2], area[3])

        # puts correct buttons in correct places
        if buttonList[x][2] == "a0":
            screen.blit(orbitButton, buttonPos)
        elif buttonList[x][2] == "a1":
            screen.blit(flightButton, buttonPos)
        elif buttonList[x][2] == "a2":
            screen.blit(resourceButton, buttonPos)
        elif buttonList[x][2] == "a3":
            screen.blit(genericButton, buttonPos)
        elif buttonList[x][2] == "a4":
            screen.blit(yesButton, buttonPos)
        elif buttonList[x][2] == "a5":
            screen.blit(noButton, buttonPos)
        elif buttonList[x][2] == "a6":
            screen.blit(homeButton, buttonPos)
        elif buttonList[x][2] == "a7":
            screen.blit(powerButton, buttonPos)

        elif buttonList[x][2] == "b0":
            screen.blit(genericButton, buttonPos)
        elif buttonList[x][2] == "b1":
            screen.blit(genericButton, buttonPos)
        elif buttonList[x][2] == "b2":
            screen.blit(genericButton, buttonPos)
        elif buttonList[x][2] == "b3":
            screen.blit(genericButton, buttonPos)
        elif buttonList[x][2] == "b4":
            screen.blit(genericButton, buttonPos)
        elif buttonList[x][2] == "b5":
            screen.blit(genericButton, buttonPos)

        elif buttonList[x][2] == "j1":
            screen.blit(joystickButton1, buttonPos)
        elif buttonList[x][2] == "j2":
            screen.blit(joystickButton2, buttonPos)
        elif buttonList[x][2] == "j3":
            screen.blit(joystickButton3, buttonPos)
        elif buttonList[x][2] == "j4":
            screen.blit(joystickButton4, buttonPos)

        else :
            if buttonDrawTime == "front" :
                if buttonList[x][4] == "front" :
                    rectFunc(buttonPos, buttonSize, 2, c["white"], c["dialGrey"])

                    textPos = (buttonPos[0] + (buttonSize[0] / 2), buttonPos[1] + (buttonSize[1] / 2) - 10)
                    textFunc(str(buttonList[x][3]), c["white"], textPos, "centre")

            if buttonDrawTime == "back" :
                if buttonList[x][4] == "back" :
                    rectFunc(buttonPos, buttonSize, 2, c["white"], c["dialGrey"])

                    textPos = (buttonPos[0] + (buttonSize[0] / 2), buttonPos[1] + (buttonSize[1] / 2) - 10)
                    textFunc(str(buttonList[x][3]), c["white"], textPos, "centre")


# draws a rectangle with the button title centred in the rectangle
def drawScrollButtons(scrollButtonDrawTime="front"):
    # runs loop once for each button
    for x in range(0, len(scrollButtonList)):
        area = pygame.Rect(scrollButtonList[x][0][0], scrollButtonList[x][0][1],
                           scrollButtonList[x][1][0], scrollButtonList[x][1][1])
        buttonPos = (area[0], area[1])
        buttonSize = (area[2], area[3])

        # check which one of the functions is called (start or end of loop)
        if scrollButtonDrawTime == "front" :
            # check if button is supposed to be drawn then
            if scrollButtonList[x][5] == "front" :
                # draw button
                textPos = (buttonPos[0] + (buttonSize[0] / 2), buttonPos[1] + (buttonSize[1] / 2) - 10)

                rectFunc(buttonPos, buttonSize, 2, c["white"], c["dialGrey"])

                # makes selected button lighter
                if activeScroll[0] == scrollButtonList[x][3][0] and activeScroll[1] == scrollButtonList[x][3][1] :
                    rectFunc(buttonPos, buttonSize, 2, c["white"], c["grey"])

                textFunc(str(scrollButtonList[x][4]), c["white"], textPos, "centre")

        if scrollButtonDrawTime == "back" :
            if scrollButtonList[x][5] == "back" :
                textPos = (buttonPos[0] + (buttonSize[0] / 2), buttonPos[1] + (buttonSize[1] / 2) - 10)

                rectFunc(buttonPos, buttonSize, 2, c["white"], c["dialGrey"])

                # makes selected button lighter
                if activeScroll[0] == scrollButtonList[x][3][0] and activeScroll[1] == scrollButtonList[x][3][1] :
                    rectFunc(buttonPos, buttonSize, 2, c["white"], c["grey"])

                textFunc(str(scrollButtonList[x][4]), c["white"], textPos, "centre")


# value, x, y, length, vert, color, max, min
#     0, 1, 2,      3,    4,     5,   6,   7

# function that draws the progress bars
# returns the positions of the bars so stuff (eg text) can be aligned with the bar
# make sure that the vert is between 1 and 4
def bar(value, pos, length, vert, givenColor, maxVal, minVal):
    if value >= maxVal :
        value = maxVal

    # finds length of the display bar as percentage of (max - min) value
    barLength = value / (maxVal - minVal)
    barLength = barLength * length
    barLength = int(barLength)

    returnVal = [0, 0]

    posX, posY = pos
    xPos      = 0
    yPos      = 0
    barHeight = 0
    barWidth  = 0

    # up
    if vert == 1:
        # border
        pygame.draw.rect(screen, givenColor, pygame.Rect(posX - 2, posY - 2, 24, length + 4), 1)

        yPos = posY + (length - barLength)
        xPos = posX

        barHeight = barLength
        barWidth = 20

        returnVal = barLength

    # right
    if vert == 2:
        # border
        pygame.draw.rect(screen, givenColor, pygame.Rect(posX - 2, posY - 2, length + 4, 24), 1)

        yPos = posY
        xPos = posX

        barHeight = 20
        barWidth = barLength

        returnVal = barLength

    # down
    if vert == 3:
        # border
        pygame.draw.rect(screen, givenColor, pygame.Rect(posX - 2, posY - 2, 24, length + 4), 1)

        yPos = posY
        xPos = posX

        barHeight = barLength
        barWidth = 20

        returnVal = barLength

    # left
    if vert == 4:
        # border
        pygame.draw.rect(screen, givenColor, pygame.Rect(posX - 2, posY - 2, length + 4, 24), 1)

        yPos = posY
        xPos = posX + (length - barLength)

        barHeight = 20
        barWidth = barLength

        returnVal = barLength

    # bar
    # check value isn't 0 then draw the bar
    if 1 >= barLength >= 0.5:
        pygame.draw.rect(screen, givenColor, pygame.Rect(xPos, yPos, barWidth, barHeight))
        # print("dunne")
    if barLength > 1:
        pygame.draw.rect(screen, givenColor, pygame.Rect(xPos, yPos, barWidth, barHeight))

    return returnVal


def panelExposure():
    # get list of solar panels
    solarPanels = vessel.parts.solar_panels
    # number of solar panels in the list
    panelsAmount = len(solarPanels)

    panelsVal = 0
    panelsMean = 0

    if panelsAmount != 0:
        for i in range(0, panelsAmount):
            panelsVal = panelsVal + solarPanels[i].sun_exposure

        panelsMean = panelsVal / panelsAmount
    elif panelsAmount == 0:
        panelsMean = None

    return panelsMean


def elecGeneration() :
    # partType can be: panels, cells, generators or, alternators
    panels         = vessel.parts.solar_panels
    cells          = vessel.parts.with_title("Fuel Cell")
    cellArrays     = vessel.parts.with_title("Fuel Cell Array")
    generators     = vessel.parts.with_title("PB-NUK Radioisotope Thermoelectric Generator")
    allAlternators = vessel.parts.with_module("ModuleAlternator")
    alternators    = []
    other          = cells + cellArrays + generators

    panelGen      = 0
    otherGen      = 0
    alternatorGen = 0
    totalGen      = 0

    # filter out engines that arent in the current stage
    for alternator in allAlternators :
        currentStage = vessel.control.current_stage
        if alternator.stage == currentStage :
            alternators.append(alternator)

    # energy production panels
    for panel in panels :
        panelGen =+ panel.energy_flow

    # production from alternators
    #for alternator in alternators : #TODO temporaraly disabled as crashes if multiple engines
        #print("")
        #for module in alternator.modules :
        #    print(module.name)
        #print("------")
        #print(alternator.modules[4].fields)
        #print(alternator.modules[4].get_field("Alternator Output"))

        #alternatorGen =+ float(alternator.modules[4].get_field("Alternator Output")) #TODO temporaraly disabled as crashes if multiple engines

    for item in vessel.parts.with_module("ModuleGenerator") :
        #print(item.name)
        pass

    #for item in cells :
    #    for mod in item.modules :
    #        print(mod.fields)
    #        print(mod.get_field("Fuel Cell"))

    infoToReturn = {"panels": panelGen,
                    "other" : otherGen,
                    "alternators" : alternatorGen,
                    "total": totalGen}

    return infoToReturn


# gets engine data
def engineData():
    data = []
    thrust = 0
    availableThrust = 0
    totalThrust = 0
    totalAvailable = 0
    engines = vessel.parts.engines

    # returns none if there are no engines
    if len(engines) == 0:
        return None

    # adds the thrust from each engine to find total
    for i in range(len(engines)):
        thrust = thrust + engines[i].thrust
        availableThrust = availableThrust + engines[i].available_thrust
        totalThrust = thrust
        totalAvailable = availableThrust

    data.append(totalThrust)
    data.append(totalAvailable)

    return data


# finds flow rate using gradient equation
def flowRate(resource):
    a = vessel.resources.amount(resource)
    time.sleep(0.05)
    b = vessel.resources.amount(resource)

    flow = (a - b) / 0.05

    return flow


# draws a bar but without the bar and one side
def marker(value, maxVal, pos, height, color, label):
    posX = pos[0]
    posY = pos[1]

    # value as percent of maxVal
    markerHeight = value / maxVal
    markerHeight = markerHeight * height
    # reduce crap in the line drawing functions
    markerOffset = height - markerHeight

    # main line
    pygame.draw.line(screen, color, (posX + 3, posY), (posX + 3, posY + height))
    # top and bottom marker lines
    pygame.draw.line(screen, color, (posX + 3, posY), (posX - 3, posY))
    pygame.draw.line(screen, color, (posX + 3, posY + height), (posX - 3, posY + height))
    # marker lines
    pygame.draw.line(screen, c["red"], (posX + 2, posY + markerOffset), (posX - 3, (posY - 3) + markerOffset))
    pygame.draw.line(screen, c["red"], (posX + 2, posY + markerOffset), (posX - 3, (posY + 3) + markerOffset))

    # label maker
    textPosX = font.size(label)[0] / 2
    textPosY = font.size(label)[1]

    textFunc(label, c["white"], (posX - textPosX, posY - textPosY), "center")


# adds buttons to the list
def loadButtons():
    for x in range(0, 8):
        newButton((20, ((x + 1) * 90) - 49), (50, 50), "a" + str(x))

    for x in range(0, 6):
        newButton((1134, ((x + 1) * 90) - 49), (50, 50), "b" + str(x))

    if buttonType == 1 :
        newButton((1109, 591), (50, 30), "j1")
        newButton((1164, 626), (30, 50), "j2")
        newButton((1109, 681), (50, 30), "j3")
        newButton((1074, 626), (30, 50), "j4")

    length = len(buttonList)

    for x in range(0, length):
        for i in range(x + 1, length):
            if buttonList[x][2] == buttonList[i][2]:
                print("Error: two buttons have the same name")
                print(buttonList[x][2])  # don't remove these lines fucktard


# find vessels and remove debris from vessel list
def findVessels() :
    global vessel
    
    vesselsList  = conn.space_center.vessels
    debris       = vessel.type.debris.name
    debrisExists = True

    while debrisExists :
        # checks for debris in the list of vessels and removes it
        for craft in vesselsList :
            if craft.type.name == debris :
                vesselsList.remove(craft)

        # runs through the list again checking for debris that was missed out
        # when it finds more debris it exits the for loop and runs the previous one again
        for newCraft in vesselsList :
            if newCraft.type.name == debris :
                break
        else :
            # when there's no debris left in the list it exits the while loop
            debrisExists = False

    return vesselsList


# CHECK CONNECTION
def checkConnection() :
    global conn

    try :
        conn = krpc.connect(name="MFD")
    except ConnectionRefusedError :
        conn = None


# Writes data to given file file
def settingsWrite(filename,contents):
    file = open(filename,"w")
    for line in contents:
        file.write(line+"\n")
    file.close()


def settingsRead(fileName):
    file = open(fileName, "r")
    contents = file.readlines()
    for i in range(len(contents)):
        contents[i] = contents[i][:-1]
    return contents


#Draw Map And Orbit
def DrawMap(mapPos, body, mapType, level, prevOrbit, nextOrbit, givenColor, vessel):
    ksc          = conn.space_center
    deg          = math.pi/180
    imgSize      = 256
    levelsDict   = {0:[2,1,256,128,3,100,16],1:[4,2,512,256,5,200,30],2:[8,4,1024,512,7,450,45]}
    mapPosDict   = {0:0, 1:imgSize, 2: 3 * imgSize}
    latLonScales = {0:81.48733086,1:162.9746617,2:325.9493235}
    markerScales = {0:[Ap_markerS,Pe_markerS,11],1:[Ap_markerM,Pe_markerM,17],2:[Ap_markerL,Pe_markerL,23]}
    detail       = 200
    parent_body  = vessel.orbit.body

    mapImages = [r"pictures\\map_images\\"+str(body)+"\\"+str(mapType)+"\\"+str(level)+"\\"+str(column)+"_"+str(row)+".png"
                 for column in range(levelsDict[level][0]) for row in range(levelsDict[level][1])]
    for image in range(len(mapImages)):
        screen.blit(pygame.image.load(mapImages[image]),(mapPos[0]+(imgSize*int(mapImages[image][-7]))
                                                         ,mapPos[1]+mapPosDict[level]-(imgSize*int(mapImages[image][-5]))))

    Wbody = wernher.CelestialBody(
        name = parent_body.name,
        gravitational_parameter = parent_body.gravitational_parameter,
        equatorial_radius = parent_body.equatorial_radius,
        rotational_speed = parent_body.rotational_speed)

    try:
        orbit = wernher.Orbit.from_krpc(ksc,vessel.orbit)
    except wernher.locked_property.OverspecifiedError:
        textFunc("CHEATER",c["red"],(mapPos[0]+imgSize*(levelsDict[level][1]),mapPos[1]+imgSize*(levelsDict[level][0]/8)),"centre",levelsDict[level][5])
        textFunc("Soz the map doesn't like perfect orbits",c["red"],(mapPos[0]+imgSize*(levelsDict[level][1]),mapPos[1]+imgSize*(levelsDict[level][0]/3)),"centre",levelsDict[level][6])
        #what a good meme

    try:
        orbit = wernher.Orbit.from_krpc(ksc,vessel.orbit)

        # start in the past by 1/4 of the orbital period
        tmin = orbit.epoch - prevOrbit*orbit.period

        # plot 1.5 periods of ground track
        tmax = tmin + nextOrbit*orbit.period

        # array of times - evenly spaced
        tt = np.linspace(tmin,tmax,detail)

        # array of lattitude and longitudes, converted to degrees
        lat = orbit.latitude_at_time(tt)/deg
        lon = orbit.longitude_at_time(tt)/deg

        #Convert lat and lon from degrees to pixels
        for i in range(len(lat)):
            lat[i] = np.radians(-(lat[i]))*latLonScales[level]+mapPos[1]+levelsDict[level][3] #Made negative as for some reason it is inverted by default
            lon[i] = np.radians(lon[i])*latLonScales[level]+mapPos[0]+levelsDict[level][2]
        points = list(zip(lon,lat))

        # makes sure that the points lists go all the way to the edge of the map image
        #print(mapPos)
        #leftEdge, rightEdge = mapPos[0], mapPos[0] + 0

        for x in range(4) :
            pass

        #Plot orbit
        for i in range(len(points)):
            try:
                # this if statement might be needed but removing it fixed inclined geosynchronous orbit lines
                #if points[i+1][0]-points[i][0] > 0:
                pygame.draw.line(screen, givenColor, (points[i]), (points[i + 1]), level + 1)
            except IndexError:
                pass
                #pygame.draw.line(screen, c["pink"], (mapPos[0], points[i][1]), (points[i + 1]), level + 1)
                #print(points[i+1])
                #try :
                #    print(str(mapPos[0]) + "  " + str(points[i][1]))
                #    print(points[i+1])
                #    pygame.draw.line(screen, c["pink"], (mapPos[0], points[i][1]), (points[i+1]), level + 1)
                #    pygame.draw.line(screen, c["pink"], (mapPos[0] + levelsDict[level[0*imgSize]], points[i][1]), (points[i+1]), level + 1)
                #except IndexError :
                #    pass

        #Plot vessel
        vesselLat = orbit.latitude_at_epoch/deg
        vesselLon = orbit.longitude_at_epoch/deg

        vesselLat = np.radians(-(vesselLat))*latLonScales[level]+mapPos[1]+levelsDict[level][3]
        vesselLon = np.radians(vesselLon)*latLonScales[level]+mapPos[0]+levelsDict[level][2]

        #Plot Aposapsis and Periapsis
        apoLat = orbit.latitude_at_apoapsis()/deg
        apoLon = orbit.longitude_at_apoapsis()/deg

        periLat = orbit.latitude_at_periapsis()/deg
        periLon = orbit.longitude_at_periapsis()/deg

        apoLat = np.radians(-apoLat)*latLonScales[level]+mapPos[1]+levelsDict[level][3]
        apoLon = np.radians(apoLon)*latLonScales[level]+mapPos[0]+levelsDict[level][2]
        periLat = np.radians(-(periLat))*latLonScales[level]+mapPos[1]+levelsDict[level][3]
        periLon = np.radians(periLon)*latLonScales[level]+mapPos[0]+levelsDict[level][2]

        screen.blit(markerScales[level][0],(int(apoLon)-int(markerScales[level][2]/2),int(apoLat)-int(markerScales[level][2])))
        screen.blit(markerScales[level][1],(int(periLon)-int(markerScales[level][2]/2),int(periLat)-int(markerScales[level][2])))
    except (wernher.locked_property.OverspecifiedError,RuntimeError):
        pass

    vesselLat = vessel.flight().latitude
    vesselLon = vessel.flight().longitude

    vesselLat = np.radians(-vesselLat)*latLonScales[level] + mapPos[1] + levelsDict[level][3]
    vesselLon = np.radians(vesselLon)*latLonScales[level]+mapPos[0]+levelsDict[level][2]
    print(vesselLon, vesselLat)

    drawCross(c["black"],(vesselLon,vesselLat),levelsDict[level][4],level+1)


def ProgressBar(givenTransmitTime, transmitting, boxPos):
    global startTime
    if transmitting :
        if len(times) == 0:
            times.append(time.time())
            startTime = times[0]

        diff = 300 / givenTransmitTime
        progress = (time.time() - startTime) * diff

        rectFunc((boxPos[0] - 10, boxPos[1] - 40), (320, 130), 2, c["white"], c["dialGrey"])
        rectFunc(boxPos, (300, 50), 1, c["white"], c["dialGrey"])

        if progress < 300:
            textFunc("Transmitting", c["white"], (boxPos[0]+150, boxPos[1]-25), "centre")
            rectFunc(boxPos, (progress, 50), 0, c["white"], c["white"])
            rectFunc((boxPos[0], boxPos[1] + 55), (300, 25), 0, c["dialGrey"], c["dialGrey"])
            textFunc(str(round(round(progress, 0) / 3, 1)) + "%", c["white"], (boxPos[0]+150, boxPos[1]+55), "centre")

        elif progress > 300:
            rectFunc((boxPos[0],boxPos[1]-25), (300, 100), 0, c["dialGrey"], c["dialGrey"])
            textFunc("Transmit Complete", c["white"], (boxPos[0]+150, boxPos[1]-25), "centre")
            rectFunc(boxPos, (300, 50), 0, c["white"], c["white"])
            textFunc(str(100) + "%", c["white"], (boxPos[0]+150, boxPos[1]+55), "centre")
            if (time.time() - startTime) > givenTransmitTime + 1:
                transmitting = False

    if not transmitting :
        try:
            times.pop(0)
        except IndexError:
            pass

    return transmitting


def toggleIndicator(pos, state) :
    toggPos   = 4
    toggColor = c["red"]

    rectFunc(pos, (40, 20), 1, c["white"], c["dialGrey"])

    if state :
        toggPos   = 24
        toggColor = c["green"]

    rectFunc((toggPos + pos[0], 4 + pos[1]), (12, 12), 2, toggColor, c["white"])


def drawOrbit(orbitingVessel, givenColor, pos) :

    # orbit variables
    # peri. and apo. are from centre of mass
    semiMajor        = orbitingVessel.orbit.semi_major_axis
    semiMinor        = orbitingVessel.orbit.semi_minor_axis
    timeToApo        = orbitingVessel.orbit.time_to_apoapsis
    eccentricity     = orbitingVessel.orbit.eccentricity
    eccentricAnomaly = orbitingVessel.orbit.eccentric_anomaly
    trueAnomaly      = orbitingVessel.orbit.true_anomaly
    longAscending    = orbitingVessel.orbit.longitude_of_ascending_node
    arguPeriapsis    = orbitingVessel.orbit.argument_of_periapsis
    longPeriapsis    = longAscending + arguPeriapsis
    apoapsis         = orbitingVessel.orbit.apoapsis
    soiRadius        = orbitingVessel.orbit.body.sphere_of_influence
    focusCentre      = math.sqrt(((semiMajor / scale) / 2) ** 2 - ((semiMinor / scale) / 2) ** 2)
    longPeriapsis    = -longPeriapsis
    situation        = ""

    try :
        situation = str(orbitingVessel.situation)[16:]
    except AttributeError :
        try :
            situation = str(orbitingVessel.orbit.situation)[16:]
        except AttributeError :
            pass

    xPos, yPos = pos[0], pos[1]

    closed = True

    orbit = ellipse((0 + focusCentre, 0), (semiMajor / scale) / 2, ((semiMinor / scale) / 2) / ((semiMajor / scale) / 2),
                    (True, eccentricAnomaly + PI))

    # rotate to make the periapsis upwards
    orbitPoints = rotatePolygon(orbit["points"], 90, (0, 0))
    orbitCross = rotatePolygon((orbit["crossPos"], [0, 0]), 90, (0, 0))
    # rotate to align with the prime meridian
    orbitPoints = rotatePolygon(orbitPoints, math.degrees(longPeriapsis), (0, 0))
    orbitCross = rotatePolygon(orbitCross, math.degrees(longPeriapsis), (0, 0))
    # translate to planet
    orbitPoints = translate(orbitPoints, (xPos, yPos))
    orbitCross = translate(orbitCross, (xPos, yPos))

    # escapes
    if "escaping" in situation or apoapsis > soiRadius :
        closed = False

        # elliptical escape
        if semiMajor > 0 :
            # remove points outside the soi
            toDelete = []
            for i, point in enumerate(orbitPoints) :
                if distBetween(point, (xPos, yPos)) > (soiRadius / scale) / 2 :
                    toDelete.append(point)
            for i in toDelete :
                orbitPoints.remove(i)

        # hyperbolic orbits
        elif timeToApo != float :
            # hyperbolic escapes
            semiMinor = math.sqrt((eccentricity ** 2) - 1) * semiMajor
            semiMajor = semiMajor * -1
            semiMinor = semiMinor * -1
            focusCentre = (math.sqrt((semiMajor ** 2) + (semiMinor ** 2)) + semiMajor) / scale / 2

            orbit = hyperbola((0, 0 - focusCentre), semiMajor / scale, semiMinor / scale, (soiRadius / scale) / 2)

            # rotate to align with prime meridian
            orbitPoints = rotatePolygon(orbit, math.degrees(longPeriapsis), (0, 0))
            # translate to orbit position
            orbitPoints = translate(orbitPoints, (xPos, yPos))

            # remove points outside the soi
            toDelete = []
            for i, point in enumerate(orbitPoints) :
                pass
                if distBetween(point, (xPos, yPos)) > soiRadius / scale :
                    toDelete.append(point)
                    # print(point)
            for i in toDelete :
                orbitPoints.remove(i)

    try :
        # draw the lines
        pygame.draw.lines(screen, givenColor, closed, orbitPoints)
    except ValueError :
        pass
    except TypeError :
        pass
    finally :
        try :
            drawCross(c["lightGrey"], orbitCross[0], 5)
        except TypeError :
            pass

    # debug aid
    """
    ###########################################
    for i, point in enumerate(orbitPoints) :
        # drawCross(c["red"], (point[0], point[1]), 2)
        # if i == 49 :
        #    pygame.draw.line(screen, c["darkRed"], (xPos, yPos), (point[0], point[1]))
        pass

    linePoints = ((0, 0), (0, -200))
    linePoints = rotatePolygon(linePoints, math.degrees(longPeriapsis), (0, 0))
    linePoints = translate(linePoints, (leftAlign + 300, topAlign + 500))
    pygame.draw.lines(screen, givenColor, False, linePoints, 1)

    linePoints = ((0, 0), (0, -1000))
    print(orbitingVessel.name)
    print(math.degrees(-trueAnomaly))
    linePoints = rotatePolygon(linePoints, math.degrees(-trueAnomaly + longPeriapsis), (0, 0))
    linePoints = translate(linePoints, (leftAlign + 300, topAlign + 500))
    pygame.draw.lines(screen, givenColor, False, linePoints, 1)
    ###########################################
    """


def graphLine(rawValues, yMultiplier, timeMultplier, graphWidth, graphHeight) :
    pointslist = []
    time = conn.space_center.ut

    # maps points
    for point in rawValues :
        if point[0] != 0 :
            mappedPoint = point[:]
            mappedPoint[0] = (point[0] - time) / -timeMultplier
            mappedPoint[1] = point[1] / -yMultiplier

            # only append point when it is within graphs edges
            if mappedPoint[0] < graphWidth and mappedPoint[1] > -graphHeight :
                pointslist.append(mappedPoint)

    return pointslist



# ORBIT DATA SCREEN
###########################################################################################################################
def orbitDataScreen() :
    global scale

    ##### Orbit data #####
    ######################

    # orbit variables
    # peri. and apo. are from centre of mass
    semiMajor        = vessel.orbit.semi_major_axis
    semiMinor        = vessel.orbit.semi_minor_axis
    period           = vessel.orbit.period
    apoapsis         = vessel.orbit.apoapsis_altitude
    periapsis        = vessel.orbit.periapsis_altitude
    timeToApo        = vessel.orbit.time_to_apoapsis
    timeToPeri       = vessel.orbit.time_to_periapsis
    inclination      = vessel.orbit.inclination
    eccentricity     = vessel.orbit.eccentricity
    eccentricAnomaly = vessel.orbit.eccentric_anomaly
    longAscending    = vessel.orbit.longitude_of_ascending_node
    arguPeriapsis    = vessel.orbit.argument_of_periapsis
    longPeriapsis    = longAscending + arguPeriapsis
    situation        = str(vessel.situation)[16:]
    soiRadius        = vessel.orbit.body.sphere_of_influence
    focusCentre      = 0
    vesselBody       = vessel.orbit.body

    mainBody = 0

    ##### maneuver data #####
    #########################

    maneuverApoapsis         = 0
    maneuverPeriapsis        = 0
    maneuverInclination      = 0
    maneuverEccentricity     = 0
    maneuverEccentricAnomaly = 0
    maneuverTimeTo           = 0
    maneuverBurnTime         = 0
    maneuverTimeToBurn       = 0
    maneuverDV               = 0
    maneuverSemiMajor        = 0
    maneuverSemiMinor        = 0
    maneuverLongAscending    = 0
    maneuverArguPeriapsis    = 0
    maneuverLongPeriapsis    = 0
    maneuverFocusCentre      = 0
    maneuverSituation        = ""
    maneuverSoiRadius        = 0
    maneuverNode             = 0
    maneuverBody             = 0

    # if there is no maneuver there would be an error upon running these
    try :
        maneuver = True

        maneuverNode = vessel.control.nodes[0]

        maneuverSemiMajor        = vessel.control.nodes[0].orbit.semi_major_axis
        maneuverSemiMinor        = vessel.control.nodes[0].orbit.semi_minor_axis
        maneuverApoapsis         = vessel.control.nodes[0].orbit.apoapsis_altitude
        maneuverPeriapsis        = vessel.control.nodes[0].orbit.periapsis_altitude
        maneuverInclination      = vessel.control.nodes[0].orbit.inclination
        maneuverEccentricity     = vessel.control.nodes[0].orbit.eccentricity
        maneuverEccentricAnomaly = vessel.control.nodes[0].orbit.eccentric_anomaly
        maneuverLongAscending    = vessel.control.nodes[0].orbit.longitude_of_ascending_node
        maneuverArguPeriapsis    = vessel.control.nodes[0].orbit.argument_of_periapsis
        maneuverLongPeriapsis    = maneuverLongAscending + maneuverArguPeriapsis
        maneuverTimeTo           = vessel.control.nodes[0].time_to
        maneuverDV               = vessel.control.nodes[0].remaining_delta_v
        maneuverSoiRadius        = vessel.control.nodes[0].orbit.body.sphere_of_influence
        maneuverBody             = vessel.control.nodes[0].orbit.body

        # calculate burn time
        try:
            force                = vessel.available_thrust
            isp                  = vessel.specific_impulse * 9.82
            m0                   = vessel.mass
            m1                   = m0 / math.exp(vessel.control.nodes[0].remaining_delta_v / isp)
            flowRate             = force / isp
            maneuverBurnTime     = (m0 - m1) / flowRate
        except ZeroDivisionError:
            maneuverBurnTime     = "<NaN>"

        try:
            maneuverTimeToBurn   = maneuverTimeTo - (maneuverBurnTime / 2)
        except TypeError:
            maneuverTimeToBurn   = "<NaN>"

        if maneuverEccentricity > 1 :
            maneuverSituation    = "escaping"
        else :
            maneuverSituation    = "orbiting"

        try :
            # distance from focus to center
            maneuverFocusCentre  = math.sqrt(math.pow((maneuverSemiMajor / scale) / 2, 2) - math.pow((maneuverSemiMinor / scale) / 2, 2))
        except ValueError :
            maneuverFocusCentre  = 0

    except (IndexError, RuntimeError) :
        maneuver = False

    ##### target data #####
    #######################

    targSemiMajor             = 0
    targSemiMinor             = 0
    targPeriod                = 0
    targApoapsis              = 0
    targPeriapsis             = 0
    targTimeToApo             = 0
    targTimeToPeri            = 0
    targInclination           = 0
    targEccentricity          = 0
    targEccentricAnomaly      = 0
    targLongAscending         = 0
    targArguPeriapsis         = 0
    targLongPeriapsis         = 0
    targFocusCentre           = 0
    targAltitude              = 0
    targAngleToApo            = 0
    targDistance              = 0
    targRelativeInclination   = 0
    targTimeToClosestApproach = 0
    targetName                = ""
    targSituation             = ""
    targSoiRadius             = 0
    targeting                 = False
    target                    = 0
    targetBody                = 0


    try :
        target = conn.space_center.target_vessel
        if target is None :
            target = conn.space_center.target_body
            if target is None :
                targetName = "No Target"

        targeting               = True

        targSemiMajor           = target.orbit.semi_major_axis
        targSemiMinor           = target.orbit.semi_minor_axis
        targPeriod              = target.orbit.period
        targApoapsis            = target.orbit.apoapsis_altitude
        targPeriapsis           = target.orbit.periapsis_altitude
        targTimeToApo           = target.orbit.time_to_apoapsis
        targTimeToPeri          = target.orbit.time_to_periapsis
        targInclination         = target.orbit.inclination
        targEccentricity        = target.orbit.eccentricity
        targEccentricAnomaly    = target.orbit.eccentric_anomaly
        targLongAscending       = target.orbit.longitude_of_ascending_node
        targArguPeriapsis       = target.orbit.argument_of_periapsis
        targLongPeriapsis       = targLongAscending + targArguPeriapsis
        targAngleToApo          = (targTimeToApo / targPeriod) * (2 * math.pi)
        targetBody              = target.orbit.body

        # targTimeToClosestApproach = timeConvert(vessel.orbit.time_of_closest_approach(target) - conn.space_center.ut,"h")
        # print(targTimeToClosestApproach) #FINISH
        # VERY BROKEN # TODO
        targetName              = target.name
        targSoiRadius           = target.orbit.body.sphere_of_influence
        # \/ this moved to end because these lines cause exception when targeting body
        targRelativeInclination = vessel.orbit.relative_inclination(target.orbit)
        targDistance            = vessel.orbit.distance_at_closest_approach(target.orbit)
        targSituation           = str(target.situation)[16 :]

        try :
            # distance from focus to center
            targFocusCentre = math.sqrt(math.pow((targSemiMajor / scale) / 2, 2) - math.pow((targSemiMinor / scale) / 2, 2))
        except ValueError :
            targFocusCentre = 0

    except AttributeError :
        targeting = False
    except TypeError :
        pass

    try :
        mainBody = vesselBody.orbit.body
        if mainBody.name == "Sun" :
            mainBody = vesselBody
        if targeting or maneuver :
            if targetBody == vesselBody or maneuverBody == vesselBody :
                mainBody = vesselBody
    except AttributeError :
        mainBody = vesselBody

    ##### drawing inclination indicator #####
    #########################################

    # inclination indicator position
    inclPosX = 800 + leftAlign
    inclPosY = 450 + topAlign

    # the array that are rotated to draw the orbits' inclinations
    baseLine = ((-50, 0), (50, 0))
    longLine = ((-55, 0), (55, 0))

    # indicator outline
    pygame.draw.circle(screen, c["lightGrey"], (inclPosX, inclPosY), 50, 1)
    # indicator: 0 degree marker
    pygame.draw.line(screen, c["lightGrey"], (-60 + inclPosX, inclPosY), (60 + inclPosX, inclPosY), 1)

    # target
    if targeting :
        line = rotatePolygon(longLine, math.degrees(targInclination), (inclPosX, inclPosY))
        pygame.draw.line(screen, c["targetYellow"], line[0], line[1], 1)

    # maneuver
    if maneuver :
        line = rotatePolygon(longLine, math.degrees(maneuverInclination), (inclPosX, inclPosY))
        pygame.draw.line(screen, c["maneuverOrange"], line[0], line[1], 1)

    # orbit line
    line = rotatePolygon(baseLine, math.degrees(inclination), (inclPosX, inclPosY))
    pygame.draw.line(screen, c["guiBlue"], line[0], line[1], 1)


    ##### ORBITS #####
    ##################

    # the size (diameter) that the orbit is displayed on the screen
    orbitSize = 300

    # centre pos of the orbit:
    orbitPosX, orbitPosY = leftAlign + 300, topAlign + 500

    bodyList = (vesselBody, targetBody, maneuverBody)
    vesselSituations = (situation, targSituation, maneuverSituation)

    # if any craft are orbiting the main body
    if mainBody in bodyList :
        semiMajors  = [semiMajor, maneuverSemiMajor, targSemiMajor]
        largestAxis = max(semiMajors)
        scale       = (largestAxis / orbitSize)
        # if any of these craft are escaping main body's SOI
        if "escaping" in vesselSituations :
            soiRadii   = [soiRadius, maneuverSoiRadius, targSoiRadius]
            largestSoi = max(soiRadii)
            scale      = (largestSoi / (orbitSize * 1.4))
    # if
    for i, body in enumerate(bodyList) :
        if mainBody != body and body != 0 :

            if i == 0 :
                semiMajors = [semiMajor, maneuverSemiMajor, targSemiMajor, vesselBody.orbit.semi_major_axis]
                largestAxis = max(semiMajors)
                scale = (largestAxis / (orbitSize * 1.3))
            if i == 1 :
                semiMajors = [semiMajor, maneuverSemiMajor, targSemiMajor, targetBody.orbit.semi_major_axis]
                largestAxis = max(semiMajors)
                scale = (largestAxis / (orbitSize * 1.3))
            if i == 2 :
                semiMajors = [semiMajor, maneuverSemiMajor, targSemiMajor, maneuverBody.orbit.semi_major_axis]
                largestAxis = max(semiMajors)
                scale = (largestAxis / (orbitSize * 1.3))


    ##### moons n stuff #####

    satellites = mainBody.satellites

    bodyPositions = {}
    if satellites :
        for satellite in satellites :
            # drawing orbits
            sateSemiMajor        = satellite.orbit.semi_major_axis
            sateSemiMinor        = satellite.orbit.semi_minor_axis
            sateEccentricAnomaly = satellite.orbit.eccentric_anomaly
            radius               = satellite.equatorial_radius
            bodyColor            = planetColors[str(satellite.name)]
            sateLongAscending    = satellite.orbit.longitude_of_ascending_node
            sateArguPeriapsis    = satellite.orbit.argument_of_periapsis
            sateLongPeriapsis    = sateLongAscending + sateArguPeriapsis
            sateName             = satellite.name

            radius = radius / (scale * 2)
            if radius < 1 :
                radius = 1

            try :
                # distance from focus to center
                sateFocusCentre = math.sqrt(math.pow((sateSemiMajor / scale) / 2, 2) -
                                            math.pow((sateSemiMinor / scale) / 2, 2))
            except ValueError :
                sateFocusCentre = 0

            sateOrbit = ellipse((0 + sateFocusCentre, 0), (sateSemiMajor / scale) / 2, ((sateSemiMinor / scale) / 2) / ((sateSemiMajor / scale) / 2),
                                (True, sateEccentricAnomaly + PI))
            # rotate to make the periapsis upwards
            sateOrbitCross = rotatePolygon((sateOrbit["crossPos"], [0, 0]), 90, (0, 0))
            # rotate to align with the prime meridian
            sateOrbitCross = rotatePolygon(sateOrbitCross, math.degrees(-sateLongPeriapsis), (0, 0))
            # translate to planet
            sateOrbitCross = translate(sateOrbitCross, (orbitPosX, orbitPosY))
            # draw the lines
            drawOrbit(satellite, c["darkGrey"], (orbitPosX, orbitPosY))
            drawCross(bodyColor, sateOrbitCross[0], 5)

            bodyPositions.update({sateName : sateOrbitCross[0]})

            # body
            pygame.draw.circle(screen, bodyColor, (int(sateOrbitCross[0][0]), int(sateOrbitCross[0][1])), int(radius), 1)

            if satellite.has_atmosphere :
                atmosAlt = satellite.atmosphere_depth

                if atmosAlt < 1 :
                    atmosAlt = 0

                pygame.draw.circle(screen, c["lightGrey"], (orbitPosX, orbitPosY), int(atmosAlt + radius), 1)

    ##### vessels orbits #####

    vesselOrbitPos = (orbitPosX, orbitPosY)
    if vesselBody != mainBody :
        vesselOrbitPos = bodyPositions[vesselBody.name]
    drawOrbit(vessel, c["guiBlue"], vesselOrbitPos)

    if targeting :

        targetPos = (orbitPosX, orbitPosY)
        if targetBody != vesselBody :
            if targetBody != mainBody :
                targetPos = bodyPositions[targetBody.name]
        drawOrbit(target, c["targetYellow"], targetPos)

    if maneuver :
        drawOrbit(maneuverNode, c["maneuverOrange"], (orbitPosX, orbitPosY))

    ##### body #####

    radius    = mainBody.equatorial_radius
    bodyColor = planetColors[str(mainBody.name)]

    radius = radius / (scale * 2)

    if radius < 1 :
        radius = 1
        drawCross(bodyColor, (orbitPosX, orbitPosY))

    # atmosphere
    if mainBody.has_atmosphere and mainBody.name != "Sun" :
        atmosAlt = mainBody.atmosphere_depth
        atmosAlt = atmosAlt / (scale * 2)

        if atmosAlt < 1 :
            atmosAlt = 0

        pygame.draw.circle(screen, c["lightGrey"], (orbitPosX, orbitPosY), int(atmosAlt + radius), 1)

    # body
    pygame.draw.circle(screen, bodyColor, (orbitPosX, orbitPosY), int(radius), 1)

    ##### writing and extra stuff #####
    ###################################
    titleColor = c["grey"]
    infoColor = c["white"]

    # text
    textPosX = 0 + leftAlign
    textPosY = 0 + topAlign

    # Apoapsis
    try :
        timeToApoText  = str(timeConvert(timeToApo, "smart"))
    except ValueError :
        timeToApoText  = "NaN"

    # Periapsis
    try :
        timeToPeriText = str(timeConvert(timeToPeri, "smart"))
    except ValueError :
        timeToPeriText = "NaN"

    # period
    try :
        periodText     = str(timeConvert(period, "smart"))
    except ValueError :
        periodText     = "NaN"

    # apsides
    textFunc("ApA: ", titleColor, (20 + textPosX, 0 + textPosY), "left")
    textFunc("PeA: ", titleColor, (20 + textPosX, 20 + textPosY), "left")
    textFunc(str("{:,}".format(int(apoapsis))) + "m", infoColor, (235 + textPosX, 0 + textPosY), "right")
    textFunc(str("{:,}".format(int(periapsis))) + "m", infoColor, (235 + textPosX, 20 + textPosY), "right")
    # timeto
    textFunc("ApT: ", titleColor, (260 + textPosX, textPosY + 0), "left")
    textFunc("PeT: ", titleColor, (260 + textPosX, textPosY + 20), "left")
    textFunc("OrP: ", titleColor, (260 + textPosX, textPosY + 50), "left")
    textFunc(timeToApoText , infoColor, (530 + textPosX, textPosY + 0), "right")
    textFunc(timeToPeriText, infoColor, (530 + textPosX, textPosY + 20), "right")
    textFunc(periodText    , infoColor, (530 + textPosX, textPosY + 50), "right")
    # extra data
    textFunc("Inc: ", titleColor, (20 + textPosX, textPosY + 50), "left")
    textFunc("Ecc: ", titleColor, (20 + textPosX, textPosY + 70), "left")
    textFunc(str(round(math.degrees(inclination), 4)) + "°", infoColor, (148 + textPosX, textPosY + 50), ".")
    textFunc(str(round(eccentricity, 5))                   , infoColor, (148 + textPosX, textPosY + 70), ".")
    # seperator line
    # vert
    pygame.draw.line(screen, c["grey"], (240 + textPosX, 5 + textPosY), (240 + textPosX, 90 + textPosY), 1)
    pygame.draw.line(screen, c["white"], (540 + textPosX, 5 + textPosY), (540 + textPosX, 90 + textPosY), 1)
    # horz
    pygame.draw.line(screen, c["white"], (5 + textPosX, 95 + textPosY), (235 + textPosX, 95 + textPosY), 1)
    pygame.draw.line(screen, c["white"], (245 + textPosX, 95 + textPosY), (535 + textPosX, 95 + textPosY), 1)

    ##### maneuver text #####
    #########################

    # text
    textPosX = 0 + leftAlign
    textPosY = 95 + topAlign
    # title
    textFunc("Maneuver:", infoColor, (20 + textPosX, 0 + textPosY))

    if not maneuver :
        textFunc("No Maneuver", infoColor, (20 + textPosX, 20 + textPosY))

    if maneuver :
        if maneuverTimeTo < 0 :
            maneuverTimeToText = "<Beyond Node>"
            maneuverTimeToBurnText = "<Beyond Node>"
        else :
            maneuverTimeToText = str(timeConvert(maneuverTimeTo))
            try :
                maneuverTimeToBurnText = str(timeConvert(maneuverTimeToBurn))
            except TypeError :
                maneuverTimeToBurnText = "<NaN>"

        # apsides
        textFunc("ApA: ", titleColor, (20 + textPosX, 30 + textPosY))
        textFunc("PeA: ", titleColor, (20 + textPosX, 50 + textPosY))
        textFunc(str("{:,}".format(int(maneuverApoapsis))) + "m", infoColor, (220 + textPosX, 30 + textPosY), "right")
        textFunc(str("{:,}".format(int(maneuverPeriapsis))) + "m", infoColor, (220 + textPosX, 50 + textPosY), "right")
        # extra data
        textFunc("Inc:  ", titleColor, (20 + textPosX, 80 + textPosY))
        textFunc("Ecc: ", titleColor, (20 + textPosX, 100 + textPosY))
        textFunc(str(round(math.degrees(maneuverInclination), 4)) + "°", infoColor, (148 + textPosX, 80 + textPosY), ".")
        textFunc(str(round(maneuverEccentricity, 5)), infoColor, (148 + textPosX, 100 + textPosY), ".")
        # time data and DV
        textFunc("T to Node:  ", titleColor, (260 + textPosX, 30 + textPosY))
        textFunc("T to Burn:  ", titleColor, (260 + textPosX, 50 + textPosY))
        textFunc("Burn DV: ", titleColor, (260 + textPosX, 70 + textPosY))
        textFunc("Burn Time: ", titleColor,(260 + textPosX, 90 + textPosY))
        textFunc(maneuverTimeToText, infoColor, (400 + textPosX, 30 + textPosY))
        textFunc(maneuverTimeToBurnText, infoColor, (400 + textPosX, 50 + textPosY))
        textFunc(str(int(maneuverDV)) + "m/s", infoColor, (400 + textPosX, 70 + textPosY))
        try:
            textFunc(str(timeConvert(int(maneuverBurnTime))),infoColor, (400 + textPosX, 90 + textPosY))
        except ValueError:
            textFunc(maneuverBurnTime, infoColor, (400 + textPosX, 90 + textPosY))
    # seperator lines
    # vert
    pygame.draw.line(screen, c["grey"], (240 + textPosX, 5 + textPosY), (240 + textPosX, 120 + textPosY), 1)
    pygame.draw.line(screen, c["white"], (540 + textPosX, 5 + textPosY), (540 + textPosX, 120 + textPosY), 1)
    # horz
    pygame.draw.line(screen, c["white"], (5 + textPosX, 125 + textPosY), (235 + textPosX, 125 + textPosY), 1)
    pygame.draw.line(screen, c["white"], (245 + textPosX, 125 + textPosY), (535 + textPosX, 125 + textPosY), 1)

    ##### target text #####
    #######################

    # text
    textPosX = 540 + leftAlign
    textPosY = 0 + topAlign

    # titles
    textFunc("Target:", infoColor, (20 + textPosX, 0 + textPosY), "left")
    textFunc(targetName, infoColor, (20 + textPosX, 20 + textPosY), "left")

    if targeting :
        # Apoapsis
        try :
            targTimeToApoText = str(timeConvert(targTimeToApo, "smart"))
        except ValueError :
            targTimeToApoText = "NaN"

        # Periapsis
        try :
            targTimeToPeriText = str(timeConvert(targTimeToPeri, "smart"))
        except ValueError :
            targTimeToPeriText = "NaN"

        # period
        try :
            targPeriodText = str(timeConvert(targPeriod, "smart"))
        except ValueError :
            targPeriodText = "NaN"

        # apsides
        textFunc("ApA: ", titleColor, (20 + textPosX, 50 + textPosY), "left")
        textFunc("PeA: ", titleColor, (20 + textPosX, 70 + textPosY), "left")
        textFunc(str("{:,}".format(int(targApoapsis))) + "m", infoColor, (220 + textPosX, 50 + textPosY), "right")
        textFunc(str("{:,}".format(int(targPeriapsis))) + "m", infoColor, (220 + textPosX, 70 + textPosY), "right")
        # extra data
        textFunc("Inc:  ", titleColor, (20 + textPosX, 100 + textPosY), "left")
        textFunc("Ecc: ", titleColor, (20 + textPosX, 120 + textPosY), "left")
        #print(math.degrees(targInclination))
        textFunc(str(round(math.degrees(targInclination), 4)) + "°", infoColor, (148 + textPosX, 100 + textPosY), ".")
        textFunc(str(round(targEccentricity, 5)), infoColor, (148 + textPosX, 120 + textPosY), ".")
        # time data
        textFunc("ApT: ", titleColor, (240 + textPosX, 50 + textPosY), "left")
        textFunc("PeT: ", titleColor, (240 + textPosX, 70 + textPosY), "left")
        textFunc("OrP: ", titleColor, (240 + textPosX, 100 + textPosY), "left")
        textFunc(targTimeToApoText , infoColor, (440 + textPosX, 50 + textPosY), "right")
        textFunc(targTimeToPeriText, infoColor, (440 + textPosX, 70 + textPosY), "right")
        textFunc(targPeriodText    , infoColor, (440 + textPosX, 100 + textPosY), "right")
        # target data
        textFunc("Cl Appr: ", titleColor, (20 + textPosX, 150 + textPosY), "left")
        textFunc("Cl Dist: ", titleColor, (20 + textPosX, 170 + textPosY), "left")
        textFunc("Rel Inc: ", titleColor, (20 + textPosX, 190 + textPosY), "left")
        textFunc("BROKEN", c["white"], (280 + textPosX, 150 + textPosY), "right")
        textFunc(str("{:,}".format(int(targDistance))) + "m", infoColor, (280 + textPosX, 170 + textPosY), "right")
        textFunc(str(round(math.degrees(targRelativeInclination))) + "°", infoColor, (280 + textPosX, 190 + textPosY), "right")
    # seperators
    # horz
    pygame.draw.line(screen, c["grey"], (5 + textPosX, 145 + textPosY), (225 + textPosX, 145 + textPosY), 1)
    pygame.draw.line(screen, c["grey"], (235 + textPosX, 145 + textPosY), (479 + textPosX, 145 + textPosY), 1)
    pygame.draw.line(screen, c["white"], (5 + textPosX, 220 + textPosY), (479 + textPosX, 220 + textPosY), 1)
    # vert
    pygame.draw.line(screen, c["grey"], (230 + textPosX, 50 + textPosY), (230 + textPosX, 140 + textPosY), 1)


# FLIGHT DATA SCREEN
###########################################################################################################################
def flightDataScreen() :
    global vessel

    ##### nav-ball section #####
    ############################
    pitch = vessel.flight().pitch * -1
    roll = vessel.flight().roll * -1
    yaw = vessel.flight().heading

    pitch = pitch + 90
    roll = roll + 180
    yaw = yaw

    navBall((512 + leftAlign, 384 + topAlign), pitch=pitch, roll=roll, yaw=yaw, radius=200)

    textFunc("NOT WORKING", c["red"], (512 + leftAlign, 384 + topAlign), "centre", 30)

    # text for the nav-ball
    # boxes for the text
    rectFunc((667 + leftAlign, 372 + topAlign), (90, 23), 1, c["white"], (40, 40, 40))
    rectFunc((267 + leftAlign, 372 + topAlign), (90, 23), 1, c["white"], (40, 40, 40))
    rectFunc((467 + leftAlign, 184 + topAlign), (90, 23), 1, c["white"], (40, 40, 40))
    # pitch and roll
    textFunc("P:" + str(round(pitch, 1)), c["white"], (712 + leftAlign, 372 + topAlign), "centre")
    textFunc("R:" + str(round(roll, 1)), c["white"], (312 + leftAlign, 372 + topAlign), "centre")
    textFunc("Y:" + str(round(yaw, 1)), c["white"], (512 + leftAlign, 184 + topAlign), "centre")


    ##### heading incicator #####
    #############################
    headPosX, headPosY = 512 + leftAlign, 130 + topAlign
    width, height = 432, 50

    heading = vessel.flight().heading

    # borders
    pygame.draw.line(screen, c["white"], (-(width / 2) + headPosX, 50 + headPosY), ((width / 2) + headPosX, 50 + headPosY), 1)
    pygame.draw.line(screen, c["white"], (-(width / 2) + headPosX, 0 + headPosY), ((width / 2) + headPosX, 0 + headPosY), 1)
    pygame.draw.line(screen, c["white"], (-(width / 2) + headPosX, 0 + headPosY), (-(width / 2) + headPosX, 50 + headPosY), 1)
    pygame.draw.line(screen, c["white"], ((width / 2) + headPosX, 0 + headPosY), ((width / 2) + headPosX, 50 + headPosY), 1)

    # drawing
    # list of angles where a line will be shown
    anglesList = [0, 22.5, 30, 45, 60, 67.5, 90, 112.5, 120, 135, 150, 157.5, 180, 202.5, 210, 225, 240, 247.5, 270, 292.5, 300, 315, 330, 337.5, 360]
    yOffset = 0
    cardDirec = 0
    cardDirecLabel = ""

    for i in range(0, len(anglesList)) :

        # work out the x position of each indicator line (times by negative to switch the side that it moves to)
        xPos = (anglesList[i] + heading) * -2.4

        # makes the lines loop back to start if they go too far left
        if xPos + headPosX < headPosX - 432 :
            xPos = xPos + 864
            if xPos + headPosX < headPosX - 432 :
                xPos = xPos + 864

        # give the lines different lengths so they can be differentiated
        if anglesList[i] % 22.5 == 0 :
            yOffset = 10
        elif anglesList[i] % 30 == 0 :
            yOffset = 20
        if anglesList[i] % 90 == 0 :
            yOffset = 0
            # finds out which of the cardinal directions the indicator line is associated with
            cardDirec = anglesList[i] / 90
            # gives the line a label
            if cardDirec == 0 :
                cardDirecLabel = "N"
            elif cardDirec == 1 :
                cardDirecLabel = "E"
            elif cardDirec == 2 :
                cardDirecLabel = "S"
            elif cardDirec == 3 :
                cardDirecLabel = "W"
            else :
                cardDirecLabel = ""

        if headPosX - width/2 < xPos + headPosX < headPosX + width/2 :
            pygame.draw.line(screen, c["yellow"], (xPos + headPosX, headPosY + yOffset),
                                                  (xPos + headPosX, (headPosY + height) - yOffset))
            if anglesList[i] % 90 == 0 :
                textFunc(cardDirecLabel, c["white"], (xPos + headPosX, headPosY + 10), "centre", 30)


    ##### altitude section #####
    ############################
    altiPosX, altiPosY = 0 + leftAlign, 10 + topAlign

    # borders
    pygame.draw.line(screen, c["white"], (5 + altiPosX, 330 + altiPosY), (245 + altiPosX, 330 + altiPosY), 1)
    pygame.draw.line(screen, c["white"], (250 + altiPosX, 5 + altiPosY), (250 + altiPosX, 325 + altiPosY), 1)

    altitude = vessel.flight().mean_altitude
    terrainHeight = vessel.flight().mean_altitude - vessel.flight().surface_altitude

    #                 value,          x,             y, length, dir, color, max, min
    altitudeBar = [altitude, 80 + altiPosX, 80 + altiPosY, 200, 1, c["guiBlue"], 70000, 0]
    terrainBar = [terrainHeight, 160 + altiPosX, 80 + altiPosY, 200, 1, c["guiBlue"], altitude, 0]

    # checks altitude is below 70000 to stop the bar going too high
    if altitude > altitudeBar[6]:
        altitudeBar[0] = altitudeBar[6]

    # draw the bars
    barsPosX, barsPosY = 30 + altiPosX, 80 + altiPosY

    altitudeBarLength = bar(altitude, (0 + barsPosX, 0 + barsPosY), 200, 1, c["guiBlue"], 70000, 0)
    terrainBarLength = bar(terrainHeight, (92 + barsPosX, 0 + barsPosY), 200, 1, c["guiBlue"], altitude, 0)

    altitudeBarPoint = [     barsPosX, barsPosY + 200 - altitudeBarLength]
    terrainBarPoint  = [80 + barsPosX, barsPosY + 200 - terrainBarLength]

    # sets points for the connector line
    pointsBar = [(altitudeBarPoint[0] + 24, altitudeBarPoint[1]), (altitudeBarPoint[0] + 29, altitudeBarPoint[1]),
                 (terrainBar[1] - 49, terrainBar[2]), (terrainBar[1] - 44, terrainBar[2])]

    pointsPer = [(altitudeBarPoint[0] + 24, altitudeBarPoint[1]), (altitudeBarPoint[0] + 29, altitudeBarPoint[1]),
                 (93 + altiPosX, 315 + altiPosY), (98 + altiPosX, 315 + altiPosY)]

    pointsVal = [(altitudeBarPoint[0] + 24, altitudeBarPoint[1]), (altitudeBarPoint[0] + 29, altitudeBarPoint[1]),
                 (93 + altiPosX, 295 + altiPosY), (98 + altiPosX, 295 + altiPosY)]

    # draws the connector line between altitude bars
    pygame.draw.lines(screen, c["grey"], False, pointsBar, 1)
    pygame.draw.lines(screen, c["grey"], False, pointsPer, 1)
    pygame.draw.lines(screen, c["grey"], False, pointsVal, 1)

    roundedAltitude = round(altitude)
    atmosPercent = round((altitude / 70000) * 100)
    radarAltitude = altitude - terrainHeight
    roundRadarAlt = 0

    if atmosPercent > 100:
        atmosPercent = ">100"

    # text
    textFunc("Altitude", c["white"], (2 + altiPosX, 0 + altiPosY), "left", 22)
    # bar labels
    textFunc("True", c["white"], (40 + altiPosX, 25 + altiPosY), "centre")
    textFunc("Radar", c["white"], (130 + altiPosX, 25 + altiPosY), "centre")
    # text for the altitude bar
    textFunc("70KM", c["white"], (40 + altiPosX, 50 + altiPosY), "centre")
    textFunc("0KM", c["white"], (40 + altiPosX, 288 + altiPosY), "centre")
    # moving altitude
    textFunc(str("{:,}".format(roundedAltitude)) + "M", c["guiBlue"], (100 + altiPosX, 285 + altiPosY), "left")
    # atmospheric percentage
    textFunc(str(atmosPercent) + "%", c["guiBlue"], (100 + altiPosX, 305 + altiPosY), "left")
    # moving terrain height
    textFunc(str(siFormat(terrainHeight)) + "M", c["guiBlue"], (terrainBarPoint[0] + 35, terrainBarPoint[1] - 10), "left")
    # radar altitude
    textFunc(str(siFormat(radarAltitude)) + "M", c["guiBlue"], (130 + altiPosX, 50 + altiPosY), "centre")

    ##### pressure section #####
    ############################
    presPosX, presPosY = 0 + leftAlign, 340 + topAlign

    # borders
    pygame.draw.line(screen, c["white"], (5 + presPosX, 100 + presPosY), (245 + presPosX, 100 + presPosY), 1)
    pygame.draw.line(screen, c["white"], (250 + presPosX, 5 + presPosY), (250 + presPosX, 95 + presPosY), 1)

    atmosPressure = vessel.flight().static_pressure
    dynPressure = vessel.flight().dynamic_pressure
    atmosPresPercent = (atmosPressure / 101325) * 100

    # pressure
    textFunc("Pressure:", c["white"], (10 + presPosX, 5 + presPosY), "left")
    textFunc("Static:  " + str(round(atmosPressure)) + " Pa", c["guiBlue"],  (30 + presPosX, 35 + presPosY), "left")
    textFunc("Dynamic: " + str(round(dynPressure)) + " Pa", c["guiBlue"],    (30 + presPosX, 55 + presPosY), "left")
    textFunc("Percent: " + str(round(atmosPresPercent)) + "%", c["guiBlue"], (30 + presPosX, 75 + presPosY), "left")


    ##### velocity section #####
    ############################
    veloPosX, veloPosY = 740 + leftAlign, 0 + topAlign

    # borders
    pygame.draw.line(screen, c["white"], (0 + veloPosX, 5 + veloPosY), (0 + veloPosX, 255 + veloPosY), 1)
    pygame.draw.line(screen, c["white"], (5 + veloPosX, 260 + veloPosY), (279 + veloPosX, 260 + veloPosY), 1)

    surfaFrame = vessel.orbit.body.reference_frame
    
    speed = vessel.flight(surfaFrame).speed
    horiV = vessel.flight(surfaFrame).horizontal_speed
    vertV = vessel.flight(surfaFrame).vertical_speed
    
    try :
        angle = math.atan(round(vertV, 3) / round(horiV, 3))
        angle = math.degrees(angle) * -1
    except ZeroDivisionError :
        angle = 0

    linePoints = [[0, 0], [100, 0]]
    linePoints = rotatePolygon(linePoints, angle, (20 + veloPosX, 150 + veloPosY))
    
    # lines
    pygame.draw.lines(screen, c["red"], False, linePoints)
    pygame.draw.lines(screen, c["white"], False, (( 20 + veloPosX,  50 + veloPosY), ( 20 + veloPosX,  70 + veloPosY)))
    pygame.draw.lines(screen, c["white"], False, ((100 + veloPosX, 150 + veloPosY), (120 + veloPosX, 150 + veloPosY)))
    pygame.draw.lines(screen, c["white"], False, (( 20 + veloPosX, 230 + veloPosY), ( 20 + veloPosX, 250 + veloPosY)))

    for i in range(0, 18) :
        line = [[0, 95], [0, 100]]
        if i % 3 == 0  :
            line[0][1] = 88

        linePoints = rotatePolygon(line, 10 * -i, (20 + veloPosX, 150 + veloPosY))
        pygame.draw.lines(screen, c["white"], False, linePoints)

    
    # text
    # velocity labels
    textFunc("V: " + str(round(vertV, 2)) + "m/s", c["white"], ( 15 + veloPosX, 28 + veloPosY), "left")
    textFunc("H: " + str(round(horiV, 2)) + "m/s", c["white"], (125 + veloPosX, 140 + veloPosY), "left")
    textFunc(str(round(speed, 2)) + "m/s", c["red"],           (100 + veloPosX, 65 + veloPosY), "left")
    # angle label
    textFunc(str(round(angle * -1, 1)) + "°", c["red"], (140 + veloPosX, 100 + veloPosY), "left")


    ##### thrust section #####
    ##########################
    thrustPosX, thrustPosY = 0 + leftAlign, 598 + topAlign

    # borders
    pygame.draw.line(screen, c["white"], (  5 + thrustPosX, 0 + thrustPosY), (295 + thrustPosX, 0 + thrustPosY), 1)
    pygame.draw.line(screen, c["white"], (300 + thrustPosX, 5 + thrustPosY), (300 + thrustPosX, 164 + thrustPosY), 1)

    enginesData = engineData()
    throttle = vessel.control.throttle
    mass = vessel.mass

    ThrustValueBarPos = (140 + thrustPosX, 25 + thrustPosY)

    if enginesData is None :
        enginesData = [0.0001, 0.0001]
        thrustPercent = 0
        TWR = 0
        thrustBarLength = bar(0, ThrustValueBarPos, 100, 1, c["red"], 1, 0)
        textFunc("No Engine", c["white"], (10 + ThrustValueBarPos[0], 35 + ThrustValueBarPos[1]), "centre")
    else :
        try :
            thrustPercent = (enginesData[0] / enginesData[1]) * 100
            thrustBarLength = bar(enginesData[0], ThrustValueBarPos, 100, 1, c["red"], enginesData[1], 0)
        except ZeroDivisionError :
            thrustPercent = 0
            thrustBarLength = bar(0, ThrustValueBarPos, 100, 1, c["red"], 1, 0)

        TWR = (enginesData[0] / 10) / mass

    thrustBarPos = [140 + thrustPosX, 100 + 25 + thrustPosY - thrustBarLength]

    throttleBarLength = bar(throttle, (50 + thrustPosX, 25 + thrustPosY), 100, 1, c["red"], 1, 0)
    throttleBarPos = [50 + thrustPosX, 100 + 25 + thrustPosY - throttleBarLength]

    # text
    # bar labels
    textFunc("Thrtl", c["white"], (60 + thrustPosX, 0 + thrustPosY), "centre")
    textFunc("Thrust", c["white"], (150 + thrustPosX, 0 + thrustPosY), "centre")
    # throttle label box
    rectFunc((throttleBarPos[0] - 15, throttleBarPos[1] + 1), (49, 20), 1, c["white"], None)
    # throttle percent label
    textFunc(str(round(throttle * 100)) + "%", c["white"], (throttleBarPos[0] + 10, throttleBarPos[1]), "centre")
    # thrust data numbers
    textFunc(str(siFormat(round(enginesData[0], 1))) + "N", c["red"], (200 + thrustPosX, 83 + thrustPosY), "left")
    textFunc(str(round(thrustPercent)) + "%", c["red"], (200 + thrustPosX, 105 + thrustPosY), "left")
    # thrust weight ratio
    textFunc("TWR: " + str(round(TWR, 4)), c["red"], (140 + thrustPosX, 140 + thrustPosY), "left")

    # lines (from the bar to the numbers)
    # points for the lines
    pointsForce   = [[thrustBarPos[0] + 23, thrustBarPos[1]], [thrustBarPos[0] + 28, thrustBarPos[1]],
                     [193 + thrustPosX, 93 + thrustPosY], [198 + thrustPosX, 93 + thrustPosY]]
    pointsPercent = [[thrustBarPos[0] + 23, thrustBarPos[1]], [thrustBarPos[0] + 28, thrustBarPos[1]],
                     [193 + thrustPosX, 115 + thrustPosY], [198 + thrustPosX, 115 + thrustPosY]]
    # lines
    pygame.draw.lines(screen, c["grey"], False, pointsForce)
    pygame.draw.lines(screen, c["grey"], False, pointsPercent)


    ##### temperature section #####
    ###############################
    parts = vessel.parts.all

    tempPosX, tempPosY = 600 + leftAlign, 600 + topAlign

    # borders
    pygame.draw.line(screen, c["white"], (5 + tempPosX, 0 + tempPosY), (419 + tempPosX, 0 + tempPosY), 1)
    pygame.draw.line(screen, c["white"], (tempPosX, 5 + tempPosY), (tempPosX, 164 + tempPosY), 1)
    pygame.draw.line(screen, c["white"], (214.5 + tempPosX, 5 + tempPosY), (214.5 + tempPosX, 164 + tempPosY), 1)

    # titles
    textFunc("Root Part:",c["white"],(107.25 + tempPosX,tempPosY + 5),"centre")
    textFunc("Hottest Part:", c["white"], (321.75 + tempPosX, tempPosY + 5), "centre")

    try:
        # get temps
        #temps = [parts[i].temperature for i in range(len(parts))] #not needed now
        skinTemps = [parts[i].skin_temperature for i in range(len(parts))]
        #hottest = temps.index(max(temps)) #not needed now
        hottestSkin = skinTemps.index(max(skinTemps))
        #root = parts[0].temperature #not needed now
        rootSkin = parts[0].skin_temperature

        # part names
        textFunc(parts[0].title,c["white"],(107.25 + tempPosX,tempPosY + 35),"centre")
        textFunc(parts[hottestSkin].title, c["white"], (321.75 + tempPosX, tempPosY + 35), "centre")

        # temp text
        textFunc(str(round(rootSkin,1))+"K / "+str(int(parts[0].max_skin_temperature))+"K",c["white"],(107.25 + tempPosX,tempPosY + 95),"centre")
        textFunc(str(round(skinTemps[hottestSkin],1)) + "K / " + str(int(parts[hottestSkin].max_skin_temperature)) + "K", c["white"],(321.75 + tempPosX, tempPosY + 95), "centre")

        # temp bars
        bar(rootSkin,(107.25 + tempPosX - 60,tempPosY + 65),120,2,c["red"],parts[0].max_skin_temperature,0)
        bar(skinTemps[hottestSkin], (321.75 + tempPosX - 60, tempPosY + 65), 120, 2, c["red"], parts[hottestSkin].max_skin_temperature, 0)

        # calculate percentages
        rootPercentage = str(int(rootSkin / parts[0].max_skin_temperature *100))
        hottestPercentage = str(int(skinTemps[hottestSkin] / parts[hottestSkin].max_skin_temperature *100))

        # percentage/overheat
        if int(rootPercentage) >= 70:
            textFunc("OVERHEAT",c["red"],(107.25 + tempPosX,tempPosY + 140),"centre")
            textFunc(rootPercentage + "%", c["white"], (107.25 + tempPosX, tempPosY + 120), "centre")
        else:
            textFunc(rootPercentage + "%", c["white"], (107.25 + tempPosX, tempPosY + 120), "centre")
            textFunc("TEMPERATURE GOOD", c["grey"], (107.25 + tempPosX, tempPosY + 140), "centre")

        if int(hottestPercentage) >= 70:
            textFunc("OVERHEAT", c["red"], (321.75 + tempPosX, tempPosY + 140), "centre")
            textFunc(hottestPercentage + "%", c["white"], (321.75 + tempPosX, tempPosY + 120), "centre")
        else:
            textFunc(hottestPercentage+"%", c["white"], (321.75 + tempPosX, tempPosY + 120), "centre")
            textFunc("TEMPERATURE GOOD", c["grey"], (321.75 + tempPosX, tempPosY + 140), "centre")
    except krpc.error.RPCError:
        pass


# RESOURCE SCREEN
###########################################################################################################################
def resourceScreen() :
    maxFuel = vessel.resources.max("LiquidFuel")
    maxOxid = vessel.resources.max("Oxidizer")
    maxMono = vessel.resources.max("MonoPropellant")
    maxChar = vessel.resources.max("ElectricCharge")
    maxSoli = vessel.resources.max("SolidFuel")
    currentFuel = vessel.resources.amount("LiquidFuel")
    currentOxid = vessel.resources.amount("Oxidizer")
    currentMono = vessel.resources.amount("MonoPropellant")
    currentChar = vessel.resources.amount("ElectricCharge")
    currentSoli = vessel.resources.amount("SolidFuel")
    currentAbla = vessel.resources.amount("Ablator")

    densityFuel = vessel.resources.density("LiquidFuel")
    densityOxid = vessel.resources.density("Oxidizer")
    densityMono = vessel.resources.density("MonoPropellant")
    densitySoli = vessel.resources.density("SolidFuel")

    currentStage = vessel.control.current_stage
    maxStageFuel = vessel.resources_in_decouple_stage(currentStage - 1, False).max("LiquidFuel")
    maxStageOxid = vessel.resources_in_decouple_stage(currentStage - 1, False).max("Oxidizer")
    stageFuel = vessel.resources_in_decouple_stage(currentStage - 1, False).amount("LiquidFuel")
    stageOxid = vessel.resources_in_decouple_stage(currentStage - 1, False).amount("Oxidizer")

    panelsExpos = panelExposure()

    # checks if the resources aren't present so it sets vals so bar function doesn't divide by 0
    if not vessel.resources.has_resource("LiquidFuel"):
        maxFuel = 100
        currentFuel = 0

    if not vessel.resources.has_resource("Oxidizer"):
        maxOxid = 100
        currentOxid = 0

    if not vessel.resources_in_decouple_stage(currentStage - 1, False).has_resource("LiquidFuel"):
        maxStageFuel = 100
        stageFuel = 0

    if not vessel.resources_in_decouple_stage(currentStage - 1, False).has_resource("Oxidizer"):
        maxStageOxid = 100
        stageOxid = 0

    if not vessel.resources.has_resource("MonoPropellant"):
        maxMono = 100
        currentMono = 0

    if not vessel.resources.has_resource("ElectricCharge"):
        maxChar = 100
        currentChar = 0

    if not vessel.resources.has_resource("SolidFuel"):
        maxSoli = 100
        currentSoli = 0

    # find fuel flow for resources
    #fuelFlow = flowRate("LiquidFuel")
    #oxidFlow = flowRate("Oxidizer")
    #monoFlow = flowRate("MonoPropellant")
    #charFlow = flowRate("ElectricCharge")
    #soliFlow = flowRate("SolidFuel")
    fuelFlow = 1
    oxidFlow = 1
    monoFlow = 1
    soliFlow = 1

    ###### FUEL ######
    ##################

    fuelPosX, fuelPosY = 0 +leftAlign, 0 +topAlign

    # border lines
    pygame.draw.line(screen, c["white"], (200 + fuelPosX, 10 + fuelPosY), (200 + fuelPosX, 295 + fuelPosY))
    pygame.draw.line(screen, c["white"], (5 + fuelPosX, 300 + fuelPosY), (195 + fuelPosX, 300 + fuelPosY))

    # titles
    textFunc("Liquid Fuel", c["white"], (100 + fuelPosX, fuelPosY), "centre")

    textFunc("Stage", c["white"], (40 + fuelPosX, 20 + fuelPosY), "centre")
    textFunc("Total", c["white"], (140 + fuelPosX, 20 + fuelPosY), "centre")

    # draw progress bars
    bar(stageFuel, (30 + fuelPosX, 50 + fuelPosY), 200, 1, c["green"], maxStageFuel, 0)

    bar(currentFuel, (130 + fuelPosX, 50 + fuelPosY), 200, 1, c["green"], maxFuel, 0)

    # marker for the flow rate
    #        value, maxVal, pos,                           length, color, label
    marker(fuelFlow, 100, (90 + fuelPosX, 70 + fuelPosY), 150, c["white"], "Flow")

    # data labels
    roundedFuelStage = round(stageFuel, 1)
    roundedFuelCurrent = round(currentFuel, 1)
    roundedFuelMass = round(currentFuel * densityFuel, 1)
    #textSizeStage = font.size(str(roundedFuelStage))[0]
    #textSizeCurrent = font.size(str(roundedFuelCurrent))[0]
    #textSizeMass = font.size("Mass:" + str(roundedFuelMass))[0]

    textFunc(str(roundedFuelStage),                  c["green"], (40  + fuelPosX, 250 + fuelPosY), "centre")
    textFunc(str(roundedFuelCurrent),                c["green"], (140 + fuelPosX, 250 + fuelPosY), "centre")
    textFunc("Mass:" + str(roundedFuelMass) + " kg", c["green"], (100 + fuelPosX, 275 + fuelPosY), "centre")


    ###### Oxidiser ######
    ######################

    oxidPosX, oxidPosY = 200 + leftAlign, 0 + topAlign

    # border line
    pygame.draw.line(screen, c["white"], (200 + oxidPosX, 10 + oxidPosY), (200 + oxidPosX, 295 + oxidPosY))
    pygame.draw.line(screen, c["white"], (5 + oxidPosX, 300 + oxidPosY), (195 + oxidPosX, 300 + oxidPosY))

    # titles
    textFunc("Oxidiser", c["white"], (100 + oxidPosX, 0 + oxidPosY), "centre")

    textFunc("Stage", c["white"], (40 + oxidPosX, 20 + oxidPosY), "centre")
    textFunc("Total", c["white"], (140 + oxidPosX, 20 + oxidPosY), "centre")

    # draw prgress bars
    bar(stageOxid, (30 + oxidPosX, 50 + oxidPosY), 200, 1, c["green"], maxStageOxid, 0)
    bar(currentOxid, (130 + oxidPosX, 50 + oxidPosY), 200, 1, c["green"], maxOxid, 0)

    # marker for the flow rate
    #        value, maxVal, pos, length, color, label
    marker(oxidFlow, 100, (90 + oxidPosX, 70 + oxidPosY), 150, c["white"], "Flow")

    # data labels
    roundedOxidStage = round(stageOxid, 1)
    roundedOxidCurrent = round(currentOxid, 1)
    roundedOxidMass = round(currentOxid * densityOxid, 1)

    textFunc(str(roundedOxidStage),                  c["green"], (40  + oxidPosX, 250 + oxidPosY), "centre")
    textFunc(str(roundedOxidCurrent),                c["green"], (140 + oxidPosX, 250 + oxidPosY), "centre")
    textFunc("Mass:" + str(roundedOxidMass) + " kg", c["green"], (100 + oxidPosX, 275 + oxidPosY), "centre")


    ###### Monoprop ######
    ######################

    monoPosX, monoPosY = 400 + leftAlign, 0 + topAlign

    # border line
    pygame.draw.line(screen, c["white"], (200 + monoPosX, 10 + monoPosY), (200 + monoPosX, 295 + monoPosY))
    pygame.draw.line(screen, c["white"], (5 + monoPosX, 300 + monoPosY), (195 + monoPosX, 300 + monoPosY))

    # titles
    textFunc("Monoprop.", c["white"], (100 + monoPosX, 0 + monoPosY), "centre")

    textFunc("Total", c["white"], (40 + monoPosX, 20 + monoPosY), "centre")

    # textFunc("Stage", c["white, (410, 30))
    # textFunc("Total", c["white, (510, 30))

    # draw prgress bars
    bar(currentMono, (30 + monoPosX, 50 + topAlign), 200, 1, c["green"], maxMono, 0)

    # marker for the flow rate
    #        value, maxVal, pos, length, color, label
    marker(monoFlow, 100, (90 + monoPosX, 70 + monoPosY), 150, c["white"], "Flow")

    # data labels
    roundedMonoCurrent = round(currentMono, 1)
    roundedMonoMass = round(currentMono * densityMono, 1)

    textFunc(str(roundedMonoCurrent),                c["green"], (40 + monoPosX, 250 + monoPosY), "centre")
    textFunc("Mass:" + str(roundedMonoMass) + " kg", c["green"], (100 + monoPosX, 275 + monoPosY), "centre")


    ###### Solid fuel ######
    ########################

    soliPosX, soliPosY = 600 + leftAlign, 0 + topAlign

    # border line
    pygame.draw.line(screen, c["white"], (200 + soliPosX, 10 + soliPosY), (200 + soliPosX, 295 + soliPosY))
    pygame.draw.line(screen, c["white"], (5 + soliPosX, 300 + soliPosY), (195 + soliPosX, 300 + soliPosY))

    # titles
    textFunc("SolidFuel", c["white"], (100 + soliPosX, 0 + soliPosY), "centre")

    textFunc("Total", c["white"], (40 + soliPosX, 20 + soliPosY), "centre")

    # draw prgress bars
    bar(currentSoli, (30 + soliPosX, 50 + topAlign), 200, 1, c["green"], maxSoli, 0)

    # marker for the flow rate
    #        value, maxVal, pos, length, color, label
    marker(soliFlow, 100, (90 + soliPosX, 70 + soliPosY), 150, c["white"], "Flow")

    # data labels
    roundedSoliCurrent = round(currentSoli, 1)
    roundedSoliMass = round(currentSoli * densitySoli, 1)

    textFunc(str(roundedSoliCurrent),                c["green"], (40  + soliPosX, 250 + soliPosY), "centre")
    textFunc("Mass:" + str(roundedSoliMass) + " kg", c["green"], (100 + soliPosX, 275 + soliPosY), "centre")


    ##### Electricity #####
    #######################
    charPosX, charPosY = 0 + leftAlign, 300 + topAlign

    # borders
    pygame.draw.line(screen, c["white"], (400 + charPosX, 5 + charPosY), (400 + charPosX, 195 + charPosY), 1)
    pygame.draw.line(screen, c["white"], (5 + charPosX, 200 + charPosY), (395 + charPosX, 200 + charPosY), 1)

    # titles
    #titlePos = 100 - (font.size("Charge")[0] / 2) + charPosX
    textFunc("Charge", c["white"], (20 + charPosX, 20 + charPosY), "left")

    textFunc("Panel Exposure", c["white"], (20 + charPosX, 95 + charPosY))

    # draw progress bars
    #                  value,   pos,  length, vert, color, maxVal, minVal
    charPos = bar(currentChar, (30 + charPosX, 50 + charPosY), 200, 2, c["guiBlue"], maxChar, 0) # total

    #alteGen = elecGeneration("panels")
    #cellGen = elecGeneration("panels")
    #geneGen = elecGeneration("panels")
    panels     = elecGeneration()["panels"]
    paneGen    = 0

    #bar(paneGen,     (30 + charPosX, 150 + charPosY), 200, 2, c["guiBlue"], 1, 0) # panels
    if panelsExpos is None :
        panelsExpos = 0
        textFunc("No Panels", c["white"], (130 + charPosX, 120 + charPosY), "centre")

    bar(panelsExpos, (30 + charPosX, 120 + charPosY), 200, 2, c["guiBlue"], 1, 0) # panel exposure

    # data labels
    roundedCurrentChar = round(currentChar, 1)
    roundedMaxChar = round(maxChar, 1)
    textSizeCurrent = font.size(str(roundedCurrentChar))[0]
    textPosCurrent = charPos - (textSizeCurrent / 2)

    textFunc(str(roundedCurrentChar), c["guiBlue"], (textPosCurrent + 30 + charPosX, 72 + charPosY))
    textFunc(str(roundedMaxChar), c["guiBlue"], (235 + charPosX, 50 + charPosY))


    ###### ablator ######
    #####################
    ablaPosX, ablaPosY = 0 + leftAlign, 500 + topAlign

    # borders
    pygame.draw.line(screen, c["white"], (5 + ablaPosX, 75 + ablaPosY), (395 + ablaPosX, 75 + ablaPosY), 1)
    pygame.draw.line(screen, c["white"], (400 + ablaPosX, 5 + ablaPosY), (400 + ablaPosX, 70 + ablaPosY), 1)

    # titles
    #titlePos = 100 - (font.size("Ablator")[0] / 2) + ablaPosX
    textFunc("Ablator", c["white"], (10 + ablaPosX, 5 + ablaPosY))

    # draw progress bars
    #          value,   pos,  length, vert, color, maxVal, minVal
    bar(currentAbla, (30 + ablaPosX, 30 + ablaPosY), 200, 2, c["red"], 800, 0)

    # data labels
    roundedCurrentAbla = round(currentAbla, 1)

    textFunc(str(roundedCurrentAbla), c["red"], (235 + ablaPosX, 30 + ablaPosY))


    ##### engine data #####
    #######################
    enginePosX, enginePosY = 400 + leftAlign, 300 + topAlign
    spacing = 110

    # borders
    pygame.draw.line(screen, c["white"], (enginePosX, enginePosY + 280), (enginePosX, enginePosY + 462), 1)
    pygame.draw.line(screen, c["white"], (enginePosX + 405, enginePosY), (enginePosX + 619, enginePosY), 1)

    # title
    textFunc("Engine Data", c["white"], (enginePosX + 5, enginePosY + 10))

    # Note: engines only display when they are active (in the current stage)

    engines = vessel.parts.engines
    loop    = True

    #removes all engines not in current stage
    while loop :
        for engine in engines :
            if engine.part.stage !=  vessel.control.current_stage :
                engines.remove(engine)

        for engine in engines :
            if engine.part.stage != vessel.control.current_stage :
                break

        else :
            loop = False

    temps = [engines[i].part.temperature for i in range(len(engines))]
    maxTemps = [engines[i].part.max_temperature for i in range(len(engines))]

    # loop that draws boxes
    for i, engine in enumerate(engines) :
        engineIsActive  = engine.active
        engineThrust    = engine.thrust
        engineMaxThrust = engine.available_thrust
        engineFuelLeft  = engine.has_fuel
        engineProps     = engine.propellants
        engineName      = engine.part.title
        engineNameShort = ""
        engineThrottle  = engine.throttle
        props           = [False, False, False, False]

        # shortening the name
        if "\"" in engineName :
            engineNameShort = engineName.split("\"")[1]
        elif engineName == "CR-7 R.A.P.I.E.R. Engine" :
            engineNameShort = "RAPIER"

        inactiveReason = ""
        engineIsActiveText = ""

        # finds out why an engine isnt running
        # throttled down
        if engineThrottle == 0 :
            inactiveReason = "throttle down"

        # out of a propellant
        for prop in engineProps :
            # creates list propellants that are used
            if prop.name == "LiquidFuel" :
                props[0] = True
            if prop.name == "Oxidizer" :
                props[1] = True
            if prop.name == "IntakeAir" :
                props[2] = True
            if prop.name == "SolidFuel" :
                props[3] = True

            if prop.is_deprived :
                inactiveReason = "no " + prop.name
                engineFuelLeft = False

        if not engineFuelLeft :
            inactiveReason = "No Fuel"

        if engineIsActive :
            engineIsActiveText = "Active"
        if not engineIsActive or not engineFuelLeft or engineThrottle == 0 :
            engineIsActiveText = "Inactive"

        if engineMaxThrust == 0 :
            engineMaxThrust = 1
            engineThrust    = 0

        # box edges
        thisEngineBoxPosX = i * spacing + enginePosX
        thisEngineBoxPosY = enginePosY + 40

        if i >= 5 :
            thisEngineBoxPosX = i * spacing + enginePosX - (5 * spacing)
            thisEngineBoxPosY = thisEngineBoxPosY + 180

        # vert
        pygame.draw.line(screen, c["white"], (thisEngineBoxPosX + 110, thisEngineBoxPosY +   5),
                                             (thisEngineBoxPosX + 110, thisEngineBoxPosY + 175), 1)
        # horz
        pygame.draw.line(screen, c["white"], (thisEngineBoxPosX +   5, thisEngineBoxPosY +   0),
                                             (thisEngineBoxPosX + 105, thisEngineBoxPosY +   0), 1)
        pygame.draw.line(screen, c["white"], (thisEngineBoxPosX +   5, thisEngineBoxPosY + 180),
                                             (thisEngineBoxPosX + 105, thisEngineBoxPosY + 180), 1)

        # drawing the engine icons
        iconPosX, iconPosY = thisEngineBoxPosX + 10, thisEngineBoxPosY + 30

        pygame.draw.lines(screen, c["white"], False, (
                         (iconPosX +  5, iconPosY +  0),
                         (iconPosX +  0, iconPosY + 10),
                         (iconPosX + 40, iconPosY + 10),
                         (iconPosX + 35, iconPosY +  0)), 1)

        # resource icons
        resIconsPosX, resIconsPosY = thisEngineBoxPosX + 70, thisEngineBoxPosY + 42

        if props[0] :  # liquid fuel
            textFunc("L", c["yellow"],  (resIconsPosX +  0, resIconsPosY +  0), fontSize = 12)
        if props[1] :  # oxidiser
            textFunc("O", c["green"],   (resIconsPosX + 10, resIconsPosY +  0), fontSize = 12)
        if props[2] :  # intake air
            textFunc("A", c["guiBlue"], (resIconsPosX +  0, resIconsPosY + 10), fontSize = 12)
        if props[3] :  # solid fuel
            textFunc("S", c["red"],     (resIconsPosX + 10, resIconsPosY + 10), fontSize = 12)

        # thrust bar
        bar(vessel.control.throttle, (thisEngineBoxPosX + 21, thisEngineBoxPosY + 48), 80, 3, c["darkGrey"], 1, 0)
        barPos = bar(engineThrust, (thisEngineBoxPosX + 21, thisEngineBoxPosY + 48), 80, 3, c["red"], engineMaxThrust, 0)

        thrustPosX = thisEngineBoxPosX + 45
        thrustPosY = thisEngineBoxPosY + (barPos * 0.85) + 48

        thrustPercent = (engineThrust / engineMaxThrust) * 100

        textFunc(str(round(thrustPercent, 1)), c["red"], (thrustPosX, thrustPosY), fontSize = 14)

        # text info
        textFunc(engineNameShort,    c["white"], (thisEngineBoxPosX + 55, thisEngineBoxPosY +   5), "centre", 18)
        textFunc(engineIsActiveText, c["white"], (thisEngineBoxPosX + 55, thisEngineBoxPosY + 135), "centre", 16)
        textFunc(inactiveReason,     c["white"], (thisEngineBoxPosX + 55, thisEngineBoxPosY + 155), "centre", 14)

        # engine temperature
        if (temps[i]/maxTemps[i])*100 >= 70:
            for letter in range(len("OVERHEAT")):
                textFunc("OVERHEAT"[letter], c["orange"], (thisEngineBoxPosX + 100, thisEngineBoxPosY + 42 + (12 * (letter + 1))), "centre", 12)


# HOME SCREEN
###########################################################################################################################
def homeScreen() :
    global dialogueBox
    global selected
    global homeScreenFunctions
    global screenShowing
    global vesselSelect
    global vesselScroll

    spacing = 100

    vessels = findVessels()
    fullVesselList = vessels[:]

    print(vesselSelect)
    print(vesselScroll)
    print()

    # makes sure the list doesn't go off screen
    if len(fullVesselList) > 6 :
        del vessels[vesselScroll + 6:]
        del vessels[:vesselScroll]

        #if len(fullVesselList) > 6 :
        if len(vessels) == 6 :
            # down arrow
            pygame.draw.lines(screen, c["pink"], False, ((220 + leftAlign, 710 + topAlign),
                                                     (230 + leftAlign, 720 + topAlign),
                                                     (240 + leftAlign, 710 + topAlign)), 3)
        if len(vessels) <= 6 and vesselScroll != 0 :
            # up arrow
            pygame.draw.lines(screen, c["red"], False, ((220 + leftAlign, 80 + topAlign),
                                                     (230 + leftAlign, 70 + topAlign),
                                                     (240 + leftAlign, 80 + topAlign)), 3)

    # function that runs different screens when the function buttons are pressed
    def homeScreenSelect(index) :
        global screenShowing

        if homeScreenFunctions[index] == "science" :
            screenShowing = "science"
        if homeScreenFunctions[index] == "maneuver" :
            screenShowing = "maneuver"
        if homeScreenFunctions[index] == "graph" :
            screenShowing = "graph"
        if homeScreenFunctions[index] == "engine" :
            screenShowing = "engine"

    # scroll is what is selected from whole list
    # select is what is selected from the list on screen

    if activeButton == "b0" :
        # within first six vessels
        if vesselScroll == 0 :
            # selcted vessel isn't 0
            if vesselSelect != 0:
                vesselSelect -= 1
        # beyond first six vessels
        if vesselScroll != 0 :
            print("1")
            # first vessel is selected
            if vesselSelect == 0 :
                print("2")
                vesselScroll -= 6
                vesselSelect += 6
            # first vessel is not selected
            if vesselSelect != 0 :
                vesselSelect -= 1

    elif activeButton == "b1" :
        # stops you scrolling off the top of the list     NOTE: top refers to largest index number i.e. the bottom of the displayed (on screen) list
        if vesselSelect < len(fullVesselList) - 1 - vesselScroll :
            vesselSelect += 1
        # changes whole list when scrolling off top of list
        if vesselSelect == len(vessels) :
            if vesselSelect + vesselScroll < len(fullVesselList) - 1 :
                vesselScroll = vesselScroll + 6
                vesselSelect = 0

    elif activeButton == "b2" :
        homeScreenSelect(0)
    elif activeButton == "b3" :
        homeScreenSelect(1)
    elif activeButton == "b4" :
        homeScreenSelect(2)
    elif activeButton == "b5" :
        dialogueBox = "settings"

    screen.blit(scrollUpImage, (1075, 58))
    screen.blit(scrollDownImage, (1075, 149))
    screen.blit(settingsIcon, (1085, 507))

    textFunc("1", c["white"], (1085, 235), "left")
    textFunc("2", c["white"], (1085, 325), "left")
    textFunc("3", c["white"], (1085, 415), "left")

    # titles
    textFunc("Home Screen", c["white"], (2 +leftAlign, 0 +topAlign), "left", 36)
    textFunc("Game Time: " + gameTimeText, c["white"], (300 +leftAlign, 12 +topAlign), "left", 20)

    # boxes

    for i, Vessel in enumerate(vessels) :
        # ensures the selected box is correct color
        boxColor = c["dialGrey"]

        if i == vesselSelect :
            boxColor = c["grey"]

            # Active Vessel Marker

            # connection info box
            # box
            rectFunc((600 + leftAlign, 60 + topAlign), (375, 200), 2, c["white"], c["dialGrey"])
            # connecting lines
            pygame.draw.line(screen, c["grey"], (460 +leftAlign, 100 + (i*spacing) +topAlign), (598 + leftAlign, 60 + topAlign))
            pygame.draw.line(screen, c["grey"], (460 + leftAlign, 185 + (i * spacing) + topAlign), (598 + leftAlign, 260 + topAlign))

            # Draw Map
            body = Vessel.orbit.body.name

            DrawMap((470 + leftAlign, 400 + topAlign), body, "sat", 0, 2, 3, c["red"], Vessel)

            # Connection Bars
            if round(Vessel.comms.signal_strength,2)*100 > 75:
                barColourDict = {0:c["green"],1:c["green"],2:c["green"],3:c["green"]}
            elif round(Vessel.comms.signal_strength,2)*100 > 50:
                barColourDict = {0:c["yellow"],1:c["yellow"],2:c["yellow"],3:c["darkGrey"]}
            elif round(Vessel.comms.signal_strength,2)*100 > 25:
                barColourDict = {0:c["orange"],1:c["orange"],2:c["darkGrey"],3:c["darkGrey"]}
            elif round(Vessel.comms.signal_strength,2)*100 > 0:
                barColourDict = {0:c["red"],1:c["darkGrey"],2:c["darkGrey"],3:c["darkGrey"]}
            else:
                barColourDict = {0:c["darkGrey"],1:c["darkGrey"],2:c["darkGrey"],3:c["darkGrey"]}

            rectFunc((800+leftAlign,80+topAlign),(5,5),0,barColourDict[0],barColourDict[0])
            rectFunc((806+leftAlign,75+topAlign),(5,10),0,barColourDict[1],barColourDict[1])
            rectFunc((812+leftAlign,70+topAlign),(5,15),0,barColourDict[2],barColourDict[2])
            rectFunc((818+leftAlign,65+topAlign),(5,20),0,barColourDict[3],barColourDict[3])


            # text
            # titles:
            textFunc("Connection Info:", c["white"], (602 + leftAlign, 65 + topAlign), "left")
            #textFunc("not connected fuck you", red, (602 + leftAlign, 120 + topAlign), "left", 30)
            #signalStrength = str(round(Vessel.comms.signal_strength,2)*100)[:-2]+str("%") #OLD, keeping for testing
            signalStrength=str(round(Vessel.comms.signal_strength*100,0))[:-2]+str("%")
            textFunc("Signal Strength: "+signalStrength,c["white"],(602+leftAlign,95+topAlign),"left")
            if Vessel.comms.signal_strength == 0 or Vessel.comms.can_communicate == False:
                canCommunicate = "False"
            else:
                canCommunicate = "True"
            textFunc("Can Communicate with KSC: "+canCommunicate,c["white"],(602+leftAlign,125+topAlign),"left")
            textFunc("Can Transmit Science: "+str(Vessel.comms.can_transmit_science),c["white"],(602+leftAlign,155+topAlign),"left")
            #textFunc("Total Antenna Power:"+str(siFormat(vessel.comms.power)),c["white,(602+leftAlign,185+topAlign),"left") #broken #fix this

            #Network Path
            screen.blit(vesselManned,(620+leftAlign,200+topAlign))
            screen.blit(KSCimage,(920+leftAlign,200+topAlign))
            #print(vessel.comms.control_path[0].type)
##            for i,Ctype in enumerate(vessel.comms.control_path):
##                print(Ctype.type)
            try:
                if str(Vessel.comms.control_path[0].type) == "CommLinkType.relay":
                    relayNumber = len(Vessel.comms.control_path)
                    rectFunc((655+leftAlign,217+topAlign),(173+leftAlign,0),1,c["green"],c["green"])
                    screen.blit(relayImage,(770+leftAlign,200+topAlign))
                    textFunc("Connected Via x" + str(relayNumber - 1) + " Relay",c["white"],(787+leftAlign,235+topAlign),"centre",12)
                elif Vessel.comms.signal_strength == 0 or Vessel.comms.can_communicate == False:
                    rectFunc((655+leftAlign,217+topAlign),(173+leftAlign,0),1,c["red"],c["red"])
                    screen.blit(noSignal,(770+leftAlign,200+topAlign))
                    textFunc("No Connection",c["white"],(787+leftAlign,235+topAlign),"centre",12)
                else:
                    rectFunc((655+leftAlign,217+topAlign),(173+leftAlign,0),1,c["green"],c["green"])
                    textFunc("Direct Connection to KSC",c["white"],(787+leftAlign,235+topAlign),"centre",12)
            except IndexError:
                rectFunc((655+leftAlign,217+topAlign),(173+leftAlign,0),1,c["red"],c["red"])
                screen.blit(noSignal,(770+leftAlign,200+topAlign))
                textFunc("No Connection",c["white"],(787+leftAlign,235+topAlign),"centre",12)


        met = Vessel.met
        timeText = str(timeConvert(met, "smart"))

        line1 = str(Vessel.name) + ": " + str(Vessel.type)[11:].title()
        situationDict = {"pre_launch" : "Pre-Launch at KSC", "landed" : str(Vessel.situation)[16 :].title() + " on " + str(Vessel.orbit.body.name) + " in " + Vessel.biome
            , "splashed" : str(Vessel.situation)[16 :].title() + " on " + str(Vessel.orbit.body.name) + " in " + Vessel.biome
            , "orbiting" : str(Vessel.situation)[16 :].title() + " " + str(Vessel.orbit.body.name) + " over " + Vessel.biome
            , "flying" : str(Vessel.situation)[16 :].title() + " above " + str(Vessel.orbit.body.name) + " over " + Vessel.biome
            , "escaping" : str(Vessel.situation)[16 :].title() + " " + str(Vessel.orbit.body.name) + " over " + Vessel.biome
            , "sub_orbital" : str(Vessel.situation)[16 :].title().replace("_","-") + " above " + str(Vessel.orbit.body.name) + " over " + Vessel.biome}

        #print(str(Vessel.situation)[16:])
        #line2 = str(Vessel.situation)[16:].title() + " on " + str(Vessel.orbit.body.name) + " over " + Vessel.biome
        line2 = situationDict[str(Vessel.situation)[16:]]
        line3 = "Crew: " + str(Vessel.crew_count) + "/" + str(Vessel.crew_capacity)
        #print(Vessel.crew_capacity)
        line4 = "Recoverable: " + str(Vessel.recoverable) #Error due to loop, check
        line5 = "Mission Time: " + timeText

        #rectangle
        rectFunc((10 +leftAlign, 100 + (i*spacing) +topAlign), (450, 85), 1, c["white"], boxColor)
        #text
        textFunc(line1, c["white"], (15  +leftAlign, 100 + (i * spacing) + topAlign), "left")
        textFunc(line2, c["white"], (15  +leftAlign, 120 + (i * spacing) + topAlign), "left")
        textFunc(line3, c["white"], (15  +leftAlign, 140 + (i * spacing) + topAlign), "left", 16)
        textFunc(line4, c["white"], (200 +leftAlign, 140 + (i * spacing) + topAlign), "left", 16)
        textFunc(line5, c["white"], (15  +leftAlign, 160 + (i * spacing) + topAlign), "left", 16)

        if vessels[i] == vessel:
            textFunc("Active Vessel",c["green"],(450+leftAlign,160+(100*i)+topAlign),"right",16)


# SCIENCE SCREEN
###########################################################################################################################
def scienceScreen() :
    global vessel
    global selected
    global experimentSelect
    global experimentScroll
    global transmit
    global dialogueBox
    global transmitCost
    global transmitTime
    global allowTransmit
    global biome

    experimentImages = {"science.module" : materialsBayImage, "GooExperiment" : mysteryGooImage,
                        "sensorAccelerometer" : accelerometerImage,
                        "sensorBarometer" : barometerImage, "sensorGravimeter" : gravityDetectorImage,
                        "sensorThermometer" : thermometerImage,
                        "sensorAtmosphere" : atmosphereSensorImage, "InfraredTelescope" : asteroidTelescopeImage}
    firstPos = [100, 100]
    experiments = vessel.parts.experiments
    sensors = vessel.parts.sensors
    fullExperimentsList = experiments[:]

    if len(experiments) > 7 :
        del experiments[experimentScroll + 6:]
        del experiments[:experimentScroll]

        if len(fullExperimentsList) > 6 :
            if len(experiments) == 6 :
                pygame.draw.lines(screen, c["white"], False, ((220 + leftAlign, 710 + topAlign),
                                                         (230 + leftAlign, 720 + topAlign),
                                                         (240 + leftAlign, 710 + topAlign)), 3)
            if len(experiments) <= 6 and vesselScroll != 0 :
                pygame.draw.lines(screen, c["white"], False, ((220 + leftAlign, 80 + topAlign),
                                                         (230 + leftAlign, 70 + topAlign),
                                                         (240 + leftAlign, 80 + topAlign)), 3)

    if activeButton == "b0":
        # within first six vessels
        if experimentScroll == 0:
            # selcted vessel isn't 0
            if experimentSelect != 0:
                experimentSelect -= 1
                selected -= 1
        # beyond first six vessels
        if experimentScroll != 0:
            # first vessel is selected
            if experimentSelect == 0:
                experimentScroll -= 6
                experimentSelect += 6
            # first vessel is not selected
            if experimentSelect != 0:
                experimentSelect -= 1
                selected -= 1
    elif activeButton == "b1" :
        if experimentSelect < len(fullExperimentsList) - 1 - experimentScroll:
            experimentSelect += 1
            selected += 1
        # changes whole list when scrolling off top of list (bottom of screen)
        if experimentSelect == len(experiments):
            if experimentSelect + experimentScroll < len(fullExperimentsList) - 1:
                experimentScroll = experimentScroll + 6
                experimentSelect = 0

    elif activeButton == "b2" :
        try:
            experiments[experimentSelect].run()
        except RuntimeError:
            pass
    elif activeButton == "b3" :
        try:
            if len(experiments[experimentSelect].data) != 0:
                if experiments[experimentSelect].rerunnable is True:
                    if vessel.resources.amount("ElectricCharge") >= transmitCost:
                        experiments[experimentSelect].transmit()
                        transmit = True
                    else:
                        dialogueBox = "transmitPower"
                else:
                    dialogueBox = "inoperableDialogue"
        except NameError:
            pass
    elif activeButton == "b4" :
        try:
            experiments[experimentSelect].reset()
        except RuntimeError:
            pass
    elif activeButton == "b5":
        if experiments[experimentSelect].rerunnable is False:
            dialogueBox = "inoperableDialogue"

    # Position Data
    textFunc("Current Body: "+str(vessel.orbit.body.name), c["white"], (450, 20))
    try:
        if experiments[0].biome != "":
            textFunc("Current Biome: "+str(experiments[0].biome),c["white"],(750,20))
        else:
            textFunc("Current Biome: " + "N/A", c["white"], (750, 20))
    except IndexError:
        if vessel.biome != "":
            textFunc("Current Biome: "+str(vessel.biome),c["white"],(750,20))
        else:
            textFunc("Current Biome: " + "N/A", c["white"], (750, 20))
    textFunc("Current Situation: "+str(vessel.situation)[16:].title().replace("_","-"), c["white"], (600, 60))
    allExperimentScience = []
    for num in range(len(experiments)) :
        try :
            allExperimentScience.append(experiments[num].data[0].science_value)
        except IndexError :
            allExperimentScience.append(0)

    if len(fullExperimentsList) == 0:
        textFunc("No Experiments on Vessel",c["white"],(602,384),"centre",25)
        textFunc("No Experiments", c["white"], (100, 20), "left")
        textFunc("Total Science: 0 Science", c["white"], (100, 60))

    for num, Experiment in enumerate(experiments):
        # Defines fonts and experiment boxes
        experimentStatus = {True : "Deployed", False : "Available"}
        textFunc("Experiment: "+str(selected + 1) + " of " + str(len(fullExperimentsList)), c["white"], (100, 20), "left")
        totalScience = round(sum(allExperimentScience), 2)
        textFunc("Total Science: "+str(round(sum(allExperimentScience), 2))+" Science", c["white"], (100, 60))
        if num == experimentSelect :
            rectFunc((firstPos[0], firstPos[1] * (num + 1)), (450, 75), 1, c["white"], c["grey"])
        else :
            rectFunc((firstPos[0], firstPos[1] * (num + 1)), (450, 75), 1, c["white"], c["dialGrey"])
        
        # Button Labels
        screen.blit(scrollUpImage, (1075, 57.5)) # half a pixel? ok then
        screen.blit(scrollDownImage, (1075, 148.5))
        screen.blit(runExperimentImage, (1074.5, 234))
        screen.blit(transmitData, (1075, 324))
        screen.blit(recycleExperiment, (1075, 413.5))

        # Gets user friendly experiment title
        title = Experiment.part.title
        textFunc(title,c["white"],(firstPos[0] + 10, firstPos[1] * (num + 1) + 10))

        # Displays experiment status; Available, Deployed or Inoprable
        if Experiment.inoperable is True :
            status = "Status:Inoperable"
        elif Experiment.available is True :
            status = "Status:" + experimentStatus[Experiment.has_data]
        else :
            status = "Status:Unavailable"
        textFunc(status,c["white"],(firstPos[0] + 10, firstPos[1] * (num + 1) + 40),fontSize=16)
        
        # Gets the amount of science held in each experiment
        try :
            science = "Science:" + str(round(Experiment.data[0].science_value, 2))
        except IndexError :
            science = "Science:0.0"
        textFunc(science,c["white"],(firstPos[0] + 225, firstPos[1] * (num + 1) + 40),fontSize=16)
        
        # Draws the Data Box and Lines
        if num == experimentSelect :
            rectFunc((600, 125), (450, 425), 1, c["white"], c["dialGrey"])
            pygame.draw.lines(screen, c["grey"], False, ((firstPos[0] + 450, firstPos[1] * (num + 1)), (599, 125)))
            pygame.draw.lines(screen, c["grey"], False,
                              ((firstPos[0] + 450, firstPos[1] * (num + 1) + 75), (599, 125 + 425)))
        
            # Adds Data to Data Box:
            # Data Box Title
            boxTitle = experiments[experimentSelect].part.title
            textFunc(boxTitle, c["white"], (825, 130), "centre")

            # Data Box Status
            if experiments[experimentSelect].inoperable is True :
                boxStatus = "Status:Inoperable"
            elif experiments[experimentSelect].available is True :
                boxStatus = "Status:" + experimentStatus[experiments[experimentSelect].has_data]
            else :
                boxStatus = "Status:Unavailable"
            textFunc(boxStatus,c["white"],(712.5,160),"centre",fontSize=16)

            # Data Box Re-runable
            if experiments[experimentSelect].rerunnable is True :
                rerun = "Can be Re-run"
            else :
                rerun = "Cannot be Re-run"
            textFunc(rerun,c["white"],(937.5,160),"centre",fontSize=16)

            # Data Box Data Title)
            textFunc("Data:",c["white"],(610, 200))
            if experiments[experimentSelect].has_data is True :
                # Data Box Science Title
                try:
                    textFunc(experiments[experimentSelect].science_subject.title+str(" (BROKEN)"),c["red"],(825,225),"centre",fontSize=16) #TODO fix with .dll file
                except krpc.error.RPCError:
                    print("Experiment is not good in this situation, will be fixed with .dll file") #TODO fix with .dll file

                # Data Box Planet
                #textFunc("Planet:" + str(vessel.orbit.body.name),c["white"],(712.5,260),"centre",fontSize=16) TODO fix this with .dll file
                textFunc("Planet: BROKEN", c["red"], (712.5, 260), "centre", fontSize=16)

                # Data Box Biome
                if experiments[experimentSelect].biome == "":
                    biome = "N/A"
                else:
                    biome = str(experiments[experimentSelect].biome)
                #textFunc("Biome:" + biome,c["white"],(937.5,260),"centre",fontSize=16) TODO fix this with .dll file
                textFunc("Biome: BROKEN", c["red"], (937.5, 260), "centre", fontSize=16)

                # Data Box Amount
                textFunc("Data Size:" + str(experiments[experimentSelect].data[0].data_amount) + str(" Mits"),c["white"],(610,300),fontSize=16)

                # Data Box Science
                textFunc("Science:" + str(round(experiments[experimentSelect].data[0].science_value, 2)) + str(" Science"),c["white"],(610,340),fontSize=16)

                # Data Box TransmitValue
                textFunc("Transmit Science:" + str(round(experiments[experimentSelect].data[0].transmit_value, 2)) + str(" Science"),c["white"],(610,380),fontSize=16)

                # Part Image
                try :
                    screen.blit(experimentImages[experiments[experimentSelect].part.name], (632.5, 425))
                except KeyError :
                    screen.blit(moddedPartImage, (632.5, 425))

                # Live Data
                liveValue = "No Data"
                for i in range(len(sensors)) :
                    if sensors[i].part.name == experiments[experimentSelect].part.name :
                        if sensors[i].active is True :
                            liveValue = sensors[i].value
                        else :
                            sensors[i].active = True
                            liveValue = sensors[i].value
                textFunc("Live Data:" + str(liveValue),c["white"],(745, 445),fontSize=16)

                # Transmit Info
                # Find best antenna
                antennas = vessel.parts.antennas
                packetRates = [int(antennas[i].packet_size / antennas[i].packet_interval) for i in range(len(antennas))]
                bestAntenna = [i for i, j in enumerate(packetRates) if j == max(packetRates)][0] #TODO add exception for kerbals (no antenna)

                packetSize = vessel.parts.antennas[bestAntenna].packet_size
                packetInterval = vessel.parts.antennas[bestAntenna].packet_interval
                packetNum = experiments[experimentSelect].data[0].data_amount / packetSize
                if packetNum.is_integer() is False:
                    packetNum = round(packetNum, 0) + 1
                transmitTime = packetNum * packetInterval
                transmitCost = int(vessel.parts.antennas[bestAntenna].packet_resource_cost * packetNum)

                textFunc("Estimated Transmit Time:" + str(timeConvert(transmitTime, "m")),c["white"],(745, 465),fontSize=16)

                textFunc("Transmit Cost:",c["white"],(745, 485),fontSize=16)
                if transmitCost > vessel.resources.amount("ElectricCharge"):
                    textFunc(str(transmitCost),c["red"],(885, 485),fontSize=16)
                else:
                    textFunc(str(transmitCost), c["green"], (885, 485), fontSize=16)

            else:
                textFunc("NO DATA",c["white"],(783,360))

        try:
            if allowTransmit is True:
                if vessel.resources.amount("ElectricCharge") >= transmitCost:
                    experiments[experimentSelect].transmit()
                    transmit = True
                    allowTransmit = False
                else:
                    dialogueBox = "transmitPower"
                    allowTransmit = False
        except NameError:
            pass

        #Transmit Progress Bar
        try:
            transmit = ProgressBar(transmitTime, transmit, (442, 319))
        except (UnboundLocalError, NameError):
            pass

        # Map
        #DrawMap((575,510),vessel.orbit.body.name,"biome",0,0.25,1.5,c["red"],vessel)

        #Test Data Packet Stuff
        #print(vessel.parts.antennas[1].part.antenna.packet_size)

    return experimentSelect


# MANEUVER SCREEN
###########################################################################################################################
def maneuverScreen():
    print("working")


# GRAPH SCREEN
###########################################################################################################################
def graphScreen():
    global completed
    global graphSettings
    global dialogueBox
    global altList
    global velList
    global radAltList
    global xLimit
    global altLimit
    global velLimit
    global radAltLimit

    #position variables
    graphPosX, graphPosY    = 50 + leftAlign, 50 + topAlign
    graphWidth, graphHeight = 600, 500

    textFunc("Graph Screen", c["white"], (2 + leftAlign, 0 + topAlign), "left", 25)
    screen.blit(settingsIcon, (995 + leftAlign, 57))
    rectFunc((graphPosX - 1, graphPosY - 1), (graphWidth + 2, graphHeight + 2), 1, c["white"], c["backGrey"])

    # runs once :
    if completed == 1 :
        altList = [[0, 0]]
        velList = [[0, 0]]
        radAltList = [[0, 0]]
        xLimit       = int(graphSettings[0])
        altLimit     = int(graphSettings[1])
        velLimit     = int(graphSettings[2])
        radAltLimit  = altLimit

        completed = 2

    xMultiplier      = xLimit / graphWidth
    altMultiplier    = altLimit / graphHeight
    velMultiplier    = velLimit / graphHeight
    radAltMultiplier = altMultiplier

    #collect data
    xVal     = conn.space_center.ut
    altitude = vessel.flight().mean_altitude
    velocity = vessel.flight(vessel.orbit.body.reference_frame).speed
    radAlt   = vessel.flight().surface_altitude

    altList.append([xVal, altitude])
    velList.append([xVal, velocity])
    radAltList.append([xVal, radAlt])

    altPointslist    = graphLine(altList, altMultiplier, xMultiplier, graphWidth, graphHeight)
    velPointslist    = graphLine(velList, velMultiplier, xMultiplier, graphWidth, graphHeight)
    radAltPointslist = graphLine(radAltList, radAltMultiplier, xMultiplier, graphWidth, graphHeight)

    # move line to correct position
    altPointslist    = translate(altPointslist, (graphPosX, graphPosY + graphHeight))
    velPointslist    = translate(velPointslist, (graphPosX, graphPosY + graphHeight))
    radAltPointslist = translate(radAltPointslist, (graphPosX, graphPosY + graphHeight))

    # always crashes on first attempt because it only has one point
    try :
        pygame.draw.lines(screen, c["guiBlue"], False, altPointslist, 1)
        pygame.draw.lines(screen, c["red"], False, velPointslist, 1)
        pygame.draw.lines(screen, c["yellow"], False, radAltPointslist, 1)
    except ValueError :
        pass

    rectFunc((graphPosX + graphWidth + 20, 50), (20, 20), 1, c["black"], c["red"])
    textFunc("Velocity", c["white"], (graphPosX + graphWidth + 50, 50))
    rectFunc((graphPosX + graphWidth + 20, 80), (20, 20), 1, c["black"], c["guiBlue"])
    textFunc("Sea Level Altitude", c["white"], (graphPosX + graphWidth + 50, 80))
    rectFunc((graphPosX + graphWidth + 20, 110), (20, 20), 1, c["black"], c["yellow"])
    textFunc("Radar Altitude", c["white"], (graphPosX + graphWidth + 50, 110))

    ##### DIALOGUE BOX BUTTON CODE #####
    ####################################
    # takes the limit value and spits out edited version based on the name of the button being pushed
    # (buttons are named in graph settings dialogue function)
    def editVal(val) : # eg: val = altLimit
        if activeButton[3] == "1" :
            val = val - int(activeButton[4:])
        if activeButton[3] == "2" :
            val = val - int(activeButton[4:])
        if activeButton[3] == "3" :
            val = val - int(activeButton[4:])
        if activeButton[3] == "4" :
            val = val + int(activeButton[4:])
        if activeButton[3] == "5" :
            val = val + int(activeButton[4:])
        if activeButton[3] == "6" :
            val = val + int(activeButton[4:])

        return val

    if activeButton == "b0" :
        dialogueBox = "graphSettings"

    if not touchScreen :
        if activeButton == "b0" :
            dialogueBox = "graphSettings"
        if selectScroll[0] == "reset" :
            if selectScroll[1] :
                altList = [[0, 0]]
                velList = [[0, 0]]
                radAltList = [[0, 0]]

    if touchScreen :
        if  activeButton == "b0" :
            dialogueBox = "graphSettings"
        if activeButton == "reset" :
            altList = [[0, 0]]
            velList = [[0, 0]]
            radAltList = [[0, 0]]
        #try :
        if activeButton is not None :
            if "x" in activeButton :
                xLimit = editVal(xLimit)

                #if "+60" in activeButton :
                #    xLimit = xLimit + 60
                #elif "+10" in activeButton :
                #    xLimit = xLimit + 10
                #elif "+1" in activeButton :
                #    xLimit = xLimit + 1
                #elif "-60" in activeButton :
                #    xLimit = xLimit - 60
                #elif "-10" in activeButton :
                #    xLimit = xLimit - 10
                #elif "-1" in activeButton :
                #    xLimit = xLimit - 1
            if "alt" in activeButton :
                altLimit = editVal(altLimit)
            if "vel" in activeButton :
                velLimit = editVal(velLimit)
        #except TypeError :
        #    pass

    if xLimit <= 0 :
        xLimit = 1
    if altLimit == 0 :
        altLimit = 10
    if velLimit <= 0 :
        velLimit = 10

    graphSettings = [str(xLimit), str(altLimit), str(velLimit)]


# ENGINE SCREEN
###########################################################################################################################
def engineScreen() :
    # titles
    textFunc("Engine Data", c["white"], (2 +leftAlign, 0 +topAlign), "left", 36)
    textFunc("Game Time: " + gameTimeText, c["white"], (300 +leftAlign, 12 +topAlign), "left", 20)

    enginePosX, enginePosY = 0 + leftAlign, 50 + topAlign
    spacing = 110

    # borders
    #pygame.draw.line(screen, c["white"], (enginePosX, enginePosY + 85), (enginePosX, enginePosY + 195), 1)

    # Note: engines only display when they are active (in the current stage)

    engines = vessel.parts.engines
    loop = True

    # removes all engiones not in current stage
    while loop :
        for engine in engines :
            if engine.part.stage != vessel.control.current_stage :
                engines.remove(engine)

        for engine in engines :
            if engine.part.stage != vessel.control.current_stage :
                break

        else :
            loop = False

    # loop that draws boxes
    for i, engine in enumerate(engines) :
        engineIsActive = engine.active
        engineThrust = engine.thrust
        engineMaxThrust = engine.available_thrust
        engineFuelLeft = engine.has_fuel
        engineProps = engine.propellants
        engineName = engine.part.title
        engineNameShort = ""
        engineThrottle = engine.throttle
        props = [False, False, False, False]

        # shortening the name
        if "\"" in engineName :
            engineNameShort = engineName.split("\"")[1]
        elif engineName == "CR-7 R.A.P.I.E.R. Engine" :
            engineNameShort = "RAPIER"

        inactiveReason = ""
        engineIsActiveText = ""

        # finds out why an engine isnt running
        # throttled down
        if engineThrottle == 0 :
            inactiveReason = "throttle down"

        # out of a propellant
        for prop in engineProps :
            # creates list propellants that are used
            if prop.name == "LiquidFuel" :
                props[0] = True
            if prop.name == "Oxidizer" :
                props[1] = True
            if prop.name == "IntakeAir" :
                props[2] = True
            if prop.name == "SolidFuel" :
                props[3] = True

            if prop.is_deprived :
                inactiveReason = "no " + prop.name
                engineFuelLeft = False

        if engineIsActive :
            engineIsActiveText = "Active"
        if not engineIsActive or not engineFuelLeft or engineThrottle == 0 :
            engineIsActiveText = "Inactive"

        if engineMaxThrust == 0 :
            engineMaxThrust = 1
            engineThrust = 0

        # box edges
        # vert
        pygame.draw.line(screen, c["white"], (i * spacing + 110 + enginePosX, 5 + enginePosY),
                         (i * spacing + 110 + enginePosX, 195 + enginePosY), 1)
        # horz
        pygame.draw.line(screen, c["white"], (i * spacing + 5 + enginePosX, 200 + enginePosY),
                         (i * spacing + 105 + enginePosX, 200 + enginePosY), 1)

        # drawing the engine icons
        iconPosX, iconPosY = 10, 50

        pygame.draw.lines(screen, c["white"], False, (
            (i * spacing + iconPosX + 5 + enginePosX, iconPosY + 0 + enginePosY),
            (i * spacing + iconPosX + 0 + enginePosX, iconPosY + 10 + enginePosY),
            (i * spacing + iconPosX + 40 + enginePosX, iconPosY + 10 + enginePosY),
            (i * spacing + iconPosX + 35 + enginePosX, iconPosY + 0 + enginePosY)), 1)

        # resource icons
        resIconsPosX, resIconsPosY = 70 + i * spacing + enginePosX, 42 + enginePosY

        if props[0] :  # liquid fuel
            textFunc("L", c["yellow"], (resIconsPosX + 0, resIconsPosY + 0), fontSize = 12)
        if props[1] :  # oxidiser
            textFunc("O", c["green"], (resIconsPosX + 10, resIconsPosY + 0), fontSize = 12)
        if props[2] :  # intake air
            textFunc("A", c["guiBlue"], (resIconsPosX + 0, resIconsPosY + 10), fontSize = 12)
        if props[3] :  # solid fuel
            textFunc("S", c["red"], (resIconsPosX + 10, resIconsPosY + 10), fontSize = 12)

        # thrust bar
        bar(vessel.control.throttle, (i * spacing + 21 + enginePosX, 68 + enginePosY), 80, 3, c["darkGrey"], 1, 0)
        barPos = bar(engineThrust, (i * spacing + 21 + enginePosX, 68 + enginePosY), 80, 3, c["red"], engineMaxThrust, 0)

        thrustPosX = i * spacing + 45 + enginePosX
        thrustPosY = (barPos * 0.85) + 68 + enginePosY

        thrustPercent = (engineThrust / engineMaxThrust) * 100

        textFunc(str(round(thrustPercent, 1)), c["red"], (thrustPosX, thrustPosY), fontSize = 14)

        # text info
        textFunc(engineNameShort, c["white"], (i * spacing + 55 + enginePosX, 25 + enginePosY), "centre", 18)
        textFunc(engineIsActiveText, c["white"], (i * spacing + 55 + enginePosX, 155 + enginePosY), "centre", 16)
        textFunc(inactiveReason, c["white"], (i * spacing + 55 + enginePosX, 175 + enginePosY), "centre", 14)


# ROVER SCREEN
###########################################################################################################################
def roverScreen() :
    rover = vessel


# SETTING SCREEN
###########################################################################################################################
def settingScreen() :
    global dialogueBox

    dialogueBox = "settingScreen"


# ERROR SCREEN
###########################################################################################################################
def errorScreen() :
    textFunc("Error: " + str(error), c["white"], (20 + leftAlign, 20 + topAlign), "left", 30)
    print("error screen open")


# STARTUP SCREEN
###########################################################################################################################
def startupScreen() :
    global homeScreenFunctions
    global mainSettings
    global graphSettings
    global touchScreen
    global buttonType
    global sideButtons
    global fullscreen
    global vessel
    global gameTimeText
    global gameTime

    screen.fill((10, 10, 10))

    versionText = "Alpha Version 1.0.0"
    titleText = "Multi Functional Display"
    textFunc(versionText, c["white"], (512 + leftAlign, 576), "centre")
    textFunc(titleText, c["white"], (512 + leftAlign, 610), "centre")

    screen.blit(logo, (302, 184))

    pygame.display.update()

    homeScreenFunctions = settingsRead(r"settings\home screen shortcut settings.txt")
    mainSettings        = settingsRead(r"settings\main settings.txt")
    graphSettings       = settingsRead(r"settings\graph settings.txt")

    if mainSettings[0] == "True" :
        fullscreen = True
    elif mainSettings[0] == "False" :
        fullscreen = False

    if mainSettings[1] == "True" :
        sideButtons = True
    elif mainSettings[1] == "False" :
        sideButtons = False

    if mainSettings[2] == "True" :
        touchScreen = True
        buttonType = 0
    elif mainSettings[2] == "False" :
        touchScreen = False
        buttonType = 1

    loadButtons()
    checkConnection()

    if allowErrors :
        try :
            vessel = conn.space_center.active_vessel
            gameTime = conn.space_center.ut
            gameTimeText = timeConvert(gameTime, "smart")
        except krpc.error.RPCError :
            textFunc("Load a vessel then open a screen", c["white"], (601, 100), "centre")
        except AttributeError :
            textFunc("Cannot Connect", c["white"], (601, 100), "centre")
            checkConnection()
    else :
        vessel = conn.space_center.active_vessel
        gameTime = conn.space_center.ut
        gameTimeText = timeConvert(gameTime, "smart")


# SHUTDOWN SCREEN
###########################################################################################################################
def shutdownScreen() :
    screen.fill((10, 10, 10))
    time.sleep(0.2)
    pygame.display.update()

    screen.blit(logo, (302, 184))
    textFunc("Shutting Down", c["white"], (512 + leftAlign, 600 + topAlign), "centre", 50)
    pygame.display.update()

    settingsWrite(r"settings\home screen shortcut settings.txt", homeScreenFunctions)
    settingsWrite(r"settings\main settings.txt", mainSettings)
    settingsWrite(r"settings\graph settings.txt", graphSettings)

    for i in range(0, 5) :
        rectFunc((500 + leftAlign, 650 + topAlign), (20, 20), 0, (10, 10, 10), (10, 10, 10))
        textFunc(str((i * -1) + 5), c["white"], (512 + leftAlign, 650 + topAlign), "centre")
        pygame.display.update()
        time.sleep(0.2)

    pygame.quit()
    sys.exit()


# POWER DIALOGUE
def powerDialogue() :
    global selectScroll
    global dialogueBox
    global buttonType
    global selected
    global runOnce
    global screenShowing

    # the dialogue box border
    rectFunc((431, 256), (341, 256), 2, c["white"], (30, 30, 30))

    if runOnce == 0 :
        newButton((481, 380), (80, 25), "no", buttonType, (0, 0), "No")
        newButton((642, 380), (80, 25), "yes", buttonType, (1, 0), "Yes")

        runOnce = 1

    textFunc("Power Off?", c["white"], (602, 284), "centre")

    if buttonType == 1 :
        # checks for either yes or no button (it has to do this so the box doesn't close immediately after opening)
        if selectScroll[1] is not None :
            # checks for 'yes' button (the green one)
            if selectScroll[1] :
                # checks dialogue box button was 'yes' or 'no' (the one actually in the dialogue box)
                if selectScroll[0] == "yes" :
                    screenShowing = "shutdown"
                if selectScroll[0] == "no" :
                    dialogueBox = None
            # checks for 'no' button (the red one)
            elif not selectScroll[1] :
                dialogueBox = None
                clearScrollButtons(["all"])

    if buttonType == 0 :
        if activeButton == "yes" :
            screenShowing = "shutdown"
        elif activeButton == "no" :
            dialogueBox = None
            clearButtons(["yes", "no"])
        elif activeButton == "a5" :
            dialogueBox = None
            clearButtons(["yes", "no"])


# EXTRA DIALOGUE
def extraDialogue() :
    global screenShowing
    global dialogueBox
    global runOnce

    rectFunc((20 + leftAlign, 20 + topAlign), (200, 400), 2, c["white"], c["dialGrey"])

    if runOnce == 0 :
        newButton((30 + leftAlign, 30 + topAlign),  (180, 20), "setting", buttonType, (0, 0), "Settings")
        newButton((30 + leftAlign, 60 + topAlign),  (180, 20), "science",  buttonType, (0, 1), "Science Screen")
        newButton((30 + leftAlign, 90 + topAlign),  (180, 20), "maneuver", buttonType, (0, 2), "Mnvr. Screen")
        newButton((30 + leftAlign, 120 + topAlign), (180, 20), "graph",    buttonType, (0, 3), "Graph Screen")
        newButton((30 + leftAlign, 150 + topAlign), (180, 20), "engine",   buttonType, (0, 4), "Engine Screen")

        runOnce = 1

    if buttonType == 1 :
        if selectScroll[1] is not None:
            if not selectScroll[1] :
                dialogueBox   = None
                screenShowing = screenShowing
            if selectScroll[1] :
                if selectScroll[0] == "setting":
                    dialogueBox = None
                    screenShowing = "setting"
                if selectScroll[0] == "science":
                    dialogueBox = None
                    screenShowing = "science"
                if selectScroll[0] == "maneuver":
                    dialogueBox = None
                    screenShowing = "maneuver"
                if selectScroll[0] == "graph":
                    dialogueBox = None
                    screenShowing = "graph"
                if selectScroll[0] == "engine" :
                    dialogueBox = None
                    screenShowing = "engine"

    if buttonType == 0 :
        clearButtonsVar = ["setting", "science", "maneuver", "graph", "engine"]

        if activeButton == "setting" :
            dialogueBox = None
            screenShowing = "setting"
            clearButtons(clearButtonsVar)

        if activeButton == "science" :
            dialogueBox = None
            screenShowing = "science"
            clearButtons(clearButtonsVar)

        elif activeButton == "maneuver" :
            dialogueBox = None
            screenShowing = "maneuver"
            clearButtons(clearButtonsVar)

        elif activeButton == "graph" :
            dialogueBox = None
            screenShowing = "graph"
            clearButtons(clearButtonsVar)

        elif activeButton == "engine" :
            dialogueBox = None
            screenShowing = "engine"
            clearButtons(clearButtonsVar)

        elif activeButton == "a5" :
            dialogueBox = None
            clearButtons(clearButtonsVar)


# SETTINGS DIALOGUE
def settingsDialogue() :
    global dialogueBox
    global showBox
    global buttonToEdit
    global activeScroll
    global homeScreenFunctions

    # the position of the dialogue box
    posX, posY = 560 +leftAlign, 400 +topAlign

    rectFunc((posX, posY), (400, 300), 2, c["white"], c["dialGrey"])
    # title
    textFunc("Extra Screen Shortcuts", c["white"], (posX + 10, posY + 10), "left")

    # if buttons are scrollable
    if buttonType == 1 :
        # if 'yes' or 'no' button is pushed
        if selectScroll[1] is not None:
            # if 'yes' button
            if selectScroll[1]:

                # if 'button 'x'' is selected
                if selectScroll[0] == "button 1" :
                    showBox      = "setScreen"
                    buttonToEdit = 1
                    activeScroll = [0, 0]

                elif selectScroll[0] == "button 2" :
                    showBox      = "setScreen"
                    buttonToEdit = 2
                    activeScroll = [0, 0]

                elif selectScroll[0] == "button 3" :
                    showBox      = "setScreen"
                    buttonToEdit = 3
                    activeScroll = [0, 0]

                # if screen buttons are selected
                if selectScroll[0] == "science" :
                    homeScreenFunctions[buttonToEdit-1] = "science"
                    dialogueBox = None
                    showBox = "main"
                    #settingsWrite("settings\home screen shortcut settings.txt", homeScreenFunctions)

                elif selectScroll[0] == "maneuver" :
                    homeScreenFunctions[buttonToEdit-1] = "maneuver"
                    dialogueBox = None
                    showBox = "main"
                    #settingsWrite("settings\home screen shortcut settings.txt", homeScreenFunctions)

                elif selectScroll[0] == "graph" :
                    homeScreenFunctions[buttonToEdit-1] = "graph"
                    dialogueBox = None
                    showBox = "main"
                    #settingsWrite("settings\home screen shortcut settings.txt", homeScreenFunctions)

                elif selectScroll[0] == "engine" :
                    homeScreenFunctions[buttonToEdit-1] = "engine"
                    dialogueBox = None
                    showBox = "main"
                    #settingsWrite("settings\home screen shortcut settings.txt", homeScreenFunctions)

            # if 'no' button is selected
            elif not selectScroll[1] :
                dialogueBox = None
                showBox = "main"

    # if buttons are clickable
    if buttonType == 0 :
        if activeButton == "a5" :
            dialogueBox = None
            clearButtons(["yes", "no"])
        # if 'button 'x'' is selected
        if activeButton == "button 1" :
            showBox = "setScreen"
            buttonToEdit = 1
            activeScroll = [0, 0]

        elif activeButton == "button 2" :
            showBox = "setScreen"
            buttonToEdit = 2
            activeScroll = [0, 0]

        elif activeButton == "button 3" :
            showBox = "setScreen"
            buttonToEdit = 3
            activeScroll = [0, 0]

        # if screen buttons are selected
        if activeButton == "science" :
            homeScreenFunctions[buttonToEdit - 1] = "science"
            dialogueBox = None
            showBox = "main"
            #settingsWrite("settings\home screen shortcut settings.txt", homeScreenFunctions)

        elif activeButton == "maneuver" :
            homeScreenFunctions[buttonToEdit - 1] = "maneuver"
            dialogueBox = None
            showBox = "main"
            #settingsWrite("settings\home screen shortcut settings.txt", homeScreenFunctions)

        elif activeButton == "graph" :
            homeScreenFunctions[buttonToEdit - 1] = "graph"
            dialogueBox = None
            showBox = "main"
            #settingsWrite("settings\home screen shortcut settings.txt", homeScreenFunctions)

        elif activeButton == "engine" :
            homeScreenFunctions[buttonToEdit - 1] = "engine"
            dialogueBox = None
            showBox = "main"
            #settingsWrite("settings\home screen shortcut settings.txt", homeScreenFunctions)

    # main function
    # I'm using functions so that i dont have to have multiple dialogue boxes to display multiple dialogue screens
    def mainScreen() :
        global runOnce
        #info
        textFunc("Select shortcut to edit:", c["white"], (posX + 10, posY + 35), "left", 16)

        if runOnce == 0 :
            clearScrollButtons(["all"])
            clearButtons(["all"])

            newButton((posX + 10, posY + 60),  (150, 20), "button 1", buttonType, (0, 0), "Button 1")
            newButton((posX + 10, posY + 90),  (150, 20), "button 2", buttonType, (0, 1), "Button 2")
            newButton((posX + 10, posY + 120), (150, 20), "button 3", buttonType, (0, 2), "Button 3")

            runOnce = 1

    def setScreen() :
        global showBox
        global runOnce1

        showBox = "setScreen"

        # info
        textFunc("Select screen:", c["white"], (posX + 10, posY + 35), "left", 16)

        if runOnce1 == 0 :
            clearScrollButtons(["all"])
            clearButtons(["all"])

            for i, screeni in enumerate(extraScreens) :
                newButton((posX + 10, (posY + 60) + (i * 30)), (150, 20), screeni, buttonType, (0, i), screeni.capitalize())
                #print(buttonList)

            runOnce1 = 1


    if showBox == "main" :
        #runOnce = 0
        mainScreen()
    elif showBox == "setScreen" :
        #runOnce = 0
        setScreen()


# SETTINGS SCREEN DIALOGUE
def settingScreenDialogue() :
    global runOnce1
    global activeScroll
    global touchScreen
    global buttonType
    global fullscreen
    global sideButtons
    global screen
    global mainSettings

    # the position of the dialogue box
    posX, posY = 5 + leftAlign, 50 + topAlign

    lineSpace = 40

    if runOnce1 == 0 :
        newButton((posX + 20, posY + (lineSpace * 1) - 4), (324, 28), "fullscreen", buttonType, (0, 0), drawTime = "back")
        newButton((posX + 20, posY + (lineSpace * 2) - 4), (324, 28), "removeButtons", buttonType, (0, 1), drawTime = "back")
        newButton((posX + 20, posY + (lineSpace * 3) - 4), (324, 28), "touchScreen", buttonType, (0, 2), drawTime = "back")

        runOnce1 = 1

    # title
    textFunc("Settings", c["white"], (0 + leftAlign, 0 + topAlign), "left", 25)
    # extra crap
    textFunc("* = requires restart", c["white"], (10 + leftAlign, 30 + topAlign), "left", 18)
    textFunc("Restart to save settings", c["white"], (10 + leftAlign, 50 + topAlign), "left", 18)

    ##### fullscreen #####
    ######################

    textFunc("  Fullscreen", c["white"], (posX + 0, posY + (lineSpace * 1)), "left")
    toggleIndicator((posX + 300, posY + (lineSpace * 1)), fullscreen)

    ##### remove buttons #####
    ##########################

    # displays toogle indicator only when touchscreen is true
    if not touchScreen :
        textFunc("* Remove Side Buttons", c["darkGrey"], (posX + 0, posY + (lineSpace * 2)), "left")
        rectFunc((posX + 300, posY + (lineSpace * 2)), (40, 20), 1, c["white"], c["dialGrey"])
    elif touchScreen :
        textFunc("* Remove Side Buttons", c["white"], (posX + 0, posY + (lineSpace * 2)), "left")
        toggleIndicator((posX + 300, posY + (lineSpace * 2)), sideButtons)

    ##### touch screen #####
    ########################

    textFunc("  Touch Screen", c["white"], (posX + 0, posY + (lineSpace * 3)), "left")
    toggleIndicator((posX + 300, posY + (lineSpace * 3)), touchScreen)

    if touchScreen :
        if activeButton == "touchScreen" :
            touchScreen = not touchScreen

            if touchScreen :
                buttonType = 0
                clearScrollButtons("all")
                runOnce1 = 0
            elif not touchScreen :
                buttonType = 1
                clearButtons("all")
                runOnce1 = 0

            clearScrollButtons("all")
            clearButtons("reset")
            loadButtons()
            runOnce1 = 0

        if activeButton == "fullscreen" :
            fullscreen = not fullscreen

            if fullscreen :
                screen = pygame.display.set_mode((1920, 1080), HWSURFACE | DOUBLEBUF | FULLSCREEN)
            elif not fullscreen:
                if not displayWidth == width and not displayHeight == height :
                    screen = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF | RESIZABLE)

        if activeButton == "removeButtons" :
            sideButtons = not sideButtons

    elif not touchScreen :
        # if 'yes' or 'no' button is pushed
        if selectScroll[1] is not None :
            # if 'yes' button
            if selectScroll[1] :

                # if 'button 'x'' is selected
                if selectScroll[0] == "touchScreen" :
                    touchScreen = not touchScreen

                    if touchScreen :
                        buttonType = 0
                        clearScrollButtons("all")
                        runOnce1 = 0
                    elif not touchScreen :
                        buttonType = 1
                        clearButtons("all")
                        runOnce1 = 0

                    clearScrollButtons(["all"])
                    clearButtons("reset")
                    loadButtons()
                    runOnce1 = 0

                if selectScroll[0] == "fullscreen" :
                    fullscreen = not fullscreen

                if selectScroll[0] == "removeButton" :
                    sideButtons = not sideButtons

    mainSettings = [str(fullscreen), str(sideButtons), str(touchScreen)]


# TRANSMIT POWER DIALOGUE
def transmitPowerDialogue() :
    global selectScroll
    global dialogueBox
    global buttonType
    global selected
    global runOnce1
    global screenShowing

    # the dialogue box border
    rectFunc((602, 340), (511, 186), 2, c["white"], (30, 30, 30),"centre")

    if runOnce1 == 0 :
        newButton((562, 380), (80, 25), "OK", buttonType, (0, 0), "OK",)

        runOnce1 = 1

    textFunc("Insufficient Charge to Transmit Data", c["white"], (602, 264), "centre")
    textFunc("Required Charge:"+str(transmitCost), c["white"],(602,304),"centre")
    textFunc("Current Charge:"+str(int(vessel.resources.amount("ElectricCharge"))), c["white"],(602,324),"centre")

    if buttonType == 1 :
        # checks for either yes or no button (it has to do this so the box doesn't close immediately after opening)
        if selectScroll[1] is not None :
            # checks for 'yes' button (the green one)
            if selectScroll[1] :
                # checks dialogue box button was 'OK' (the one actually in the dialogue box)
                if selectScroll[0] == "OK" :
                    dialogueBox = None
            # checks for 'no' button (the red one)
            elif not selectScroll[1] :
                dialogueBox = None
                clearScrollButtons(["all"])

    if buttonType == 0 :
        if activeButton == "OK" :
            dialogueBox = None
            clearButtons(["OK"])
        elif activeButton == "a5" :
            dialogueBox = None
            clearButtons(["OK"])


# INOPERABLE EXPERIMENT DIALOGUE
def inoperableDialogue() :
    global selectScroll
    global dialogueBox
    global buttonType
    global selected
    global runOnce
    global screenShowing
    global allowTransmit

    # the dialogue box border
    rectFunc((381, 246), (441, 196), 2, c["white"], (30, 30, 30))

    if runOnce == 0 :
        newButton((481, 380), (80, 25), "no", buttonType, (0, 0), "No")
        newButton((642, 380), (80, 25), "yes", buttonType, (1, 0), "Yes")

        runOnce = 1

    textFunc("Transmitting this data will",c["white"],(602,264),"centre")
    textFunc("render the experiment inoperable.",c["white"],(602,284),"centre")
    textFunc("Do you still want to transmit?", c["white"], (602, 324), "centre")

    if buttonType == 1 :
        # checks for either yes or no button (it has to do this so the box doesn't close immediately after opening)
        if selectScroll[1] is not None :
            # checks for 'yes' button (the green one)
            if selectScroll[1] :
                # checks dialogue box button was 'yes' or 'no' (the one actually in the dialogue box)
                if selectScroll[0] == "yes" :
                    allowTransmit = True
                    dialogueBox = None
                    clearScrollButtons(["all"])
                if selectScroll[0] == "no" :
                    dialogueBox = None
                    clearScrollButtons(["all"])
            # checks for 'no' button (the red one)
            elif not selectScroll[1] :
                dialogueBox = None
                clearScrollButtons(["all"])

    if buttonType == 0 :
        if activeButton == "yes" :
            allowTransmit = True
            dialogueBox = None
            clearButtons(["yes", "no"])
        elif activeButton == "no" :
            dialogueBox = None
            clearButtons(["yes", "no"])
        elif activeButton == "a5" :
            dialogueBox = None
            clearButtons(["yes", "no"])


# GRAPH SETTINGS DIALOGUE
def graphSettingsDialogue() :
    global selectScroll
    global dialogueBox
    global runOnce

    # the dialogue box border
    posX, posY = 700 + leftAlign, 100 + topAlign
    boxWidth, boxHeight = 300, 500
    rectFunc((posX, posY), (boxWidth, boxHeight), 2, c["white"], c["dialGrey"])
    textFunc("Graph Settings", c["white"], (posX + 5, posY ), "left", 22)

    textFunc("Reset Graphs:", c["white"], (posX + 10, posY + 40))
    textFunc("Change Limits:", c["white"], (posX + 10, posY + 80))

    textFunc("Max Time:", c["white"], (posX + 10, posY + 110), "left", 18)
    textFunc("Max Altitude:", c["white"], (posX + 10, posY + 165), "left", 18)
    textFunc("Max Velocity:", c["white"], (posX + 10, posY + 215), "left", 18)

    textFunc(str(xLimit), c["grey"], (posX + (boxWidth /2), posY + 135), "centre", 18)
    textFunc(str(altLimit), c["grey"], (posX + (boxWidth / 2), posY + 190), "centre", 18)
    textFunc(str(velLimit), c["grey"], (posX + (boxWidth / 2), posY + 240), "centre", 18)

    def createEditButtons(name, pos, low, med, hig) :
        newButton((pos[0]      , pos[1]), (40, 20), name + "1" + str(hig), buttonType, (-5, 1), "<<<")
        newButton((pos[0] + 45 , pos[1]), (30, 20), name + "2" + str(med), buttonType, (-4, 1), "<<")
        newButton((pos[0] + 80 , pos[1]), (20, 20), name + "3" + str(low), buttonType, (-3, 1), "<")
        newButton((pos[0] + 190, pos[1]), (20, 20), name + "4" + str(low), buttonType, (-2, 1), ">")
        newButton((pos[0] + 215, pos[1]), (30, 20), name + "5" + str(med), buttonType, (-1, 1), ">>")
        newButton((pos[0] + 250, pos[1]), (40, 20), name + "6" + str(hig), buttonType, (0, 1), ">>>")

    if runOnce == 0 :
        newButton((posX + 210, posY + 40), (80, 25), "reset", buttonType, (0, 0), "Reset")

        #newButton((buttonPos[0]     , buttonPos[1]), (40, 20), "x-60", buttonType, (-5, 1), "<<<")
        #newButton((buttonPos[0] + 45, buttonPos[1]), (30, 20), "x-10", buttonType, (-4, 1), "<<")
        #newButton((buttonPos[0] + 80, buttonPos[1]), (20, 20), "x-1", buttonType, (-3, 1), "<")
        #newButton((buttonPos[0] + 190, buttonPos[1]), (20, 20), "x+1", buttonType, (-2, 1), ">")
        #newButton((buttonPos[0] + 215, buttonPos[1]), (30, 20), "x+10", buttonType, (-1, 1), ">>")
        #newButton((buttonPos[0] + 250, buttonPos[1]), (40, 20), "x+60", buttonType, (0, 1), ">>>")

        createEditButtons("x  ", (posX + 5, posY +135), 1, 10, 60)

        createEditButtons("alt", (posX + 5, posY + 190), 100, 1000, 10000)
        createEditButtons("vel", (posX + 5, posY + 240), 10, 100, 1000)

        runOnce = 1

    if not touchScreen :
        if activeButton == "a4" :
            if selectScroll == "reset" :
                pass
        if activeButton == "a5" :
            dialogueBox = None

    if touchScreen :
        if activeButton == "a5" :
            dialogueBox = None
            clearButtons(["all"])



startupScreen()



# MAIN LOOP
###########################################################################################################################
while 1 :
    try :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screenShowing = "shutdown"
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                mousePos = event.pos
                # set the button
                if button == 1:
                    click = (1, 0, 0)
                if button == 2:
                    click = (0, 1, 0)
                if button == 3:
                    click = (0, 0, 1)
            if event.type == VIDEORESIZE :
                # only does this when not fullscreen because it would cause a fullscreened mfd to resize immediately after full-screening
                if not fullscreen :
                    screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                # screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
                pygame.display.flip()

        # if mouse button one is clicked
        if click[0] == 1:
            returned = checkButtons(mousePos)
            # checks whether a the active button is the same as the one currently being clicked
            # this allows the click of a button to activate the active button once rather than repeatedly during the same click
            if returned != activeButton and not clicked :
                activeButton = returned
            elif returned == activeButton and clicked :
                activeButton = None
            clicked = True

        # resets the active button when mouse is released
        if click[0] == 0:
            clicked = False
            activeButton = None

        # reset mouse button
        click = (0, 0, 0)

        # sets the select scroll to blank
        selectScroll = [checkScrollButtons(activeScroll), None]

        displayWidth  = pygame.display.Info().current_w
        displayHeight = pygame.display.Info().current_h

        screen.fill((40, 40, 40))

        # edge lines
        pygame.draw.line(screen, c["white"], (89, 5), (89, 763), 1)
        pygame.draw.line(screen, c["white"], (1115, 5), (1115, 763), 1)

        drawButtons("back")
        drawScrollButtons("back")

        oldDialogueBox = dialogueBox

        if not touchScreen :
            for button in scrollButtonList :
                for nextButton in scrollButtonList :
                    #print("checking")
                    if button[2] == nextButton[2] :
                        break

                    if button[3] == nextButton[3] :
                        #print("same  " + str(button[2]) + "    " + str(nextButton[2]))
                        clearScrollButtons(["all"])
                        runOnce1 = 0
                        runOnce  = 0

        # sets the function of each button
        # sets the different screens when they are selected
        # orbit
        if activeButton == "a0":
            screenShowing = "orbit"
            dialogueBox = None
        # flight data
        elif activeButton == "a1":
            screenShowing = "flight"
            dialogueBox = None
        # resources
        elif activeButton == "a2":
            screenShowing = "resource"
            dialogueBox = None
        # extra screens
        elif activeButton == "a3":
            dialogueBox = "extra"
        # yes
        elif activeButton == "a4":
            # first var is the scroll button that is currently selected, the second var is the yes or no button
            selectScroll = [checkScrollButtons(activeScroll), True]
        # no
        elif activeButton == "a5":
            selectScroll = [checkScrollButtons(activeScroll), False]
        # home
        elif activeButton == "a6":
            screenShowing = "home"
            dialogueBox = None
        # power
        elif activeButton == "a7":
            dialogueBox = "power"

        # up
        elif activeButton == "j1":
            activeScroll[1] = activeScroll[1] - 1
        # right
        elif activeButton == "j2":
            activeScroll[0] = activeScroll[0] + 1
        # down
        elif activeButton == "j3":
            activeScroll[1] = activeScroll[1] + 1
        # left
        elif activeButton == "j4":
            activeScroll[0] = activeScroll[0] - 1

        # shows the correct screens
        if   screenShowing == "error" :
            errorScreen()
        elif screenShowing == "home" :
            homeScreen()
        elif screenShowing == "orbit" :
            orbitDataScreen()
        elif screenShowing == "flight" :
            flightDataScreen()
        elif screenShowing == "resource" :
            resourceScreen()
        elif screenShowing == "science" :
            scienceScreen()
        elif screenShowing == "maneuver" :
            maneuverScreen()
        elif screenShowing == "graph" :
            graphScreen()
        elif screenShowing == "engine" :
            engineScreen()
        elif screenShowing == "setting" :
            settingScreen()
        elif screenShowing == "shutdown" :
            shutdownScreen()

        if dialogueBox is not None and oldDialogueBox is not None :
            if dialogueBox != oldDialogueBox :
                clearScrollButtons(["all"])
                clearButtons(["all"])
                runOnce  = 0
                runOnce1 = 0

        # shows the correct dialogue boxes
        if dialogueBox is not None :
            # checks that the selected button is within the button list
            activeScroll = selectScrollCheck(activeScroll)

        if dialogueBox is None :
            clearScrollButtons(["all"])
            clearButtons(["all"])
            activeScroll = [0, 0]
            selectScroll = []
            runOnce = 0
            runOnce1 = 0
        elif dialogueBox == "power" :
            powerDialogue()
        elif dialogueBox == "extra" :
            extraDialogue()
        elif dialogueBox == "settings" :
            settingsDialogue()
        elif dialogueBox == "settingScreen" :
            settingScreenDialogue()
        elif dialogueBox == "transmitPower" :
            transmitPowerDialogue()
        elif dialogueBox == "inoperableDialogue" :
            inoperableDialogue()
        elif dialogueBox == "graphSettings" :
            graphSettingsDialogue()

        drawButtons("front")
        drawScrollButtons("front")

        if allowErrors :
            try :
                vessel       = conn.space_center.active_vessel
                gameTime     = conn.space_center.ut
                gameTimeText = timeConvert(gameTime, "smart")
            except krpc.error.RPCError :
                textFunc("Load a vessel then open a screen", c["white"], (601, 100), "centre")
            except AttributeError :
                textFunc("Cannot Connect", c["white"], (601, 100), "centre")
                checkConnection()
        else :
            vessel       = conn.space_center.active_vessel
            gameTime     = conn.space_center.ut
            gameTimeText = timeConvert(gameTime, "smart")

    except krpc.error.RPCError :
        print("KRPC Error: No Craft Loaded")
        if allowErrors :
            screenShowing = "error"
            error = "KRPC Error: No Craft Loaded"
            errorScreen()
        else :
            raise
    except (ConnectionResetError, AttributeError) :
        print("Connection Error")
        if allowErrors :
            checkConnection()
            screenShowing = "error"
            error = "Connection Error"
            errorScreen()
        else :
            raise
    except NameError :
        print("Name Error")
        if allowErrors :
            try :
                print("trying")
                vessel = conn.space_center.active_vessel
            except krpc.error.RPCError :
                print("KRPC Error: No craft loaded")
                screenShowing = "error"
                error = "No Craft Loaded"
                errorScreen()
            except AttributeError :
                print("Connection Error")
                screenShowing = "error"
                error = "Connection Error"
                errorScreen()
        else :
            raise
    finally :
        pass

    pygame.display.update()
