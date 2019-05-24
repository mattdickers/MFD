import sys, pygame, krpc, time, math
import random

pygame.init()

black = 0, 0, 0
lightGrey = 200, 200, 200
backGrey = 40, 40, 40
dialGrey = 30, 30, 30
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 127, 255
PI = math.pi
TWOPI = 2 * PI
HALFPI = PI / 2
font = pygame.font.SysFont("courier new", 20)

screen = pygame.display.set_mode((1204, 768), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
times = []


def rectFunc(pos, size, borderWidth, borderColor, innerColor):
    area = pygame.Rect((pos[0], pos[1]), (size[0], size[1]))

    if innerColor is not None:
        pygame.draw.rect(screen, innerColor, area)

    pygame.draw.rect(screen, borderColor, area, 1)

    # if color2 is not None
    if innerColor is not None:
        if borderWidth != 1:
            for i in range(0, borderWidth):
                area = pygame.Rect((pos[0] + (i - 1), pos[1] + (i - 1)),
                                   (size[0] - (2 * (i - 1)), size[1] - (2 * (i - 1))))
                pygame.draw.rect(screen, borderColor, area, 1)


def textFunc(text, textColor, pos, direc="left", fontSize=20):
    textFont = pygame.font.SysFont("monospace", fontSize)

    if direc == "centre":
        posX = (pos[0] - textFont.size(text)[0] / 2)
    elif direc == "right":
        posX = (pos[0] - textFont.size(text)[0])
    else:
        posX = pos[0]
    # create text object
    textObject = textFont.render(text, False, textColor)
    # add/render the text to screen
    screen.blit(textObject, (posX, pos[1]))


def ProgressBar(Time, transmitting, boxPos):
    global startTime
    if transmitting == True:
        if len(times) == 0:
            times.append(time.time())
            startTime = times[0]

        diff = 300 / Time
        progress = (time.time() - startTime) * diff

        rectFunc((boxPos[0]-10, boxPos[1]-40), (320, 130), 2, white, dialGrey)
        rectFunc(boxPos, (300, 50), 1, white, dialGrey)

        if progress < 300:
            textFunc("Transmitting", white, (boxPos[0]+150, boxPos[1]-25), "centre")
            rectFunc(boxPos, (progress, 50), 0, white, white)
            rectFunc((boxPos[0], boxPos[1] + 55), (300, 25), 0, dialGrey, dialGrey)
            textFunc(str(round(round(progress, 0) / 3, 1)) + "%", white, (boxPos[0]+150, boxPos[1]+55), "centre")

        elif progress > 300:
            rectFunc((boxPos[0], boxPos[1] - 25), (300, 100), 0, dialGrey, dialGrey)
            textFunc("Transmit Complete", white, (boxPos[0]+150, boxPos[1]-25), "centre")
            rectFunc(boxPos, (300, 50), 0, white, white)
            textFunc(str(100) + "%", white, (boxPos[0]+150, boxPos[1]+55), "centre")
            if (time.time() - startTime) > Time + 1:
                transmitting = False

        # TODO Temporary for timing test
        textFunc("Actual:", white, (175, 275), "centre")
        textFunc(str(round(time.time() - startTime, 2)), white, (250, 275), "centre")
        textFunc("Predicted:", white, (115, 295), "CENTRE")
        textFunc(str(Time), white, (250, 295), "centre")

    if transmitting == False:
        try:
            #textFunc("Dunne", white, (100, 100), "centre")  # TODO Remove before flight
            times.pop(0)
        except IndexError:
            pass

    return transmitting


transmit = True
transmitTime = 10
transmittingDict = {0: False, 1: True}

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'],
                                             pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            pygame.display.flip()

    screen.fill((40, 40, 40))

    transmit = ProgressBar(transmitTime, transmit, (100, 100))

    if transmit == False:
        transmit = transmittingDict[random.randint(0, 1)]
        transmitTime = random.randint(2, 100)
        print(transmit, transmitTime)

    pygame.display.update()
