import sys, pygame, krpc, time, math
from colorsList import c
pygame.init()

PI          = math.pi
TWOPI       = 2*PI
HALFPI      = PI/2
font        = pygame.font.SysFont("courier new", 20)

screen = pygame.display.set_mode((1080, 768))

def drawCross(givenColor, crossPos, size, width=1):
    pos = list(crossPos)

    pygame.draw.line(screen, givenColor, (pos[0] + size, pos[1] + size), (pos[0] - size, pos[1] - size), width)
    pygame.draw.line(screen, givenColor, (pos[0] - size, pos[1] + size), (pos[0] + size, pos[1] - size), width)


def ellipse(ellipsePos, radius, height, cross) :
    crossPoint = [0, 0]

    detail = 100
    step = (2 * PI) / detail
    stepAcc = 0

    ellipsePosX = ellipsePos[0]
    ellipsePosY = ellipsePos[1]

    points = [0 for i in range(detail)]

    for i in range(0, detail) :
        points[i] = ellipsePosX + radius * math.cos(stepAcc), ellipsePosY - height * radius * math.sin(stepAcc)
        stepAcc = stepAcc + step

    if cross[0] :
        crossPoint = [ellipsePosX + radius * math.cos(cross[1]), ellipsePosY - height * radius * math.sin(cross[1])]

        # the code doesnt draw a cross here because the crosspos is used to draw the moons

    return {"points" : points, "crossPos" : crossPoint}


def hyperbola(hyperbolaPos, semiMaj, semiMin, soiRadius):
    focusCentre = math.sqrt((semiMaj ** 2) + (semiMin ** 2))
    xVal = math.sqrt((semiMin ** 2 * (soiRadius ** 2 * semiMin ** 2 + soiRadius ** 2 * semiMaj ** 2 + 2 * soiRadius * semiMaj ** 3 + 2 * soiRadius * semiMin ** 2 * semiMaj - semiMin ** 4 - semiMin ** 2 * semiMaj ** 2)) / (semiMin ** 4 + 2 * semiMin ** 2 * semiMaj ** 2 + semiMaj ** 4))

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

        distBetweenV = distBetween((0, focusCentre), point)

        # debugging aids
        drawCross(c["green"], (point[0] + hyperbolaPosX, point[1] + hyperbolaPosY), 1)
        if i == 60 :
            pygame.draw.line(screen, c["darkRed"], (0 + hyperbolaPosX, focusCentre + hyperbolaPosY), (point[0] + hyperbolaPosX, point[1] + hyperbolaPosY))
        #print(angleBetween((0 + hyperbolaPosX, focusCentre + hyperbolaPosY), (point[0] + hyperbolaPosX, point[1] + hyperbolaPosY)))

        # if distance from focus to point is larger than soi radius then doint add it to the points list
        if distBetweenV > soiRadius :
            pass
        else :
            # translate to correct position
            point[0] += hyperbolaPosX
            point[1] += hyperbolaPosY

            points.append(point)

    return points


def distBetween(point1, point2) :
    diffVec = [point2[0] - point1[0], point2[1] - point1[1]]
    diffVec[0] = abs(diffVec[0])
    diffVec[1] = abs(diffVec[1])

    diffMagOut = math.sqrt(diffVec[0] **2 + diffVec[1] **2)

    return diffMagOut


def angleBetween(point1, point2) :
    xDist = point2[1] - point1[1]
    yDist = point2[0] - point1[0]

    angle = math.atan(xDist / yDist) / PI * 180

    return angle


eccentricity = 1
semiMajor, semiMinor = 100, 90

while 1:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()

    screen.fill((40, 40, 40))

    pos = (500, 200)

    semiMajor+=0.1

    radius = 200

    points = hyperbola(pos, semiMajor, semiMinor, radius)
    pygame.draw.lines(screen, c["blue"], False, points, 1)
    drawCross(c["white"], pos, 5)
    #drawCross(c["white"], (pos[0], pos[1] + 40), 5)

    focusCentre = math.sqrt((semiMajor ** 2) + (semiMinor ** 2))

    soiShape = ellipse((pos[0], pos[1] + focusCentre), radius, 1, (False, 0))
    pygame.draw.lines(screen, c["white"], True, soiShape["points"])

    drawCross(c["red"], (pos[0], pos[1] + focusCentre), 5)

    pygame.display.update()







