import pygame, sys
from pygame.locals import *
from colorsList import c

pygame.init()

width  = 1204
height = 768
screen = pygame.display.set_mode((width, height),HWSURFACE|DOUBLEBUF|RESIZABLE)

def textFunc(text, textColor, pos, direc = "left", fontSize = 20, widthLim = 0) :
    textFont = pygame.font.SysFont("monospace", fontSize)
    textObject = textFont.render(text, False, textColor)
    count = 0
    #Adjust font size to fit given width
    while textObject.get_width() > widthLim:
        if widthLim == 0:
            break
        count += 1
        textFont = pygame.font.SysFont("monospace", fontSize - count)
        textObject = textFont.render(text, False, textColor)

    if direc == "centre" :
        posX = (pos[0] - textFont.size(text)[0] / 2)
    elif direc == "right" :
        posX = (pos[0] - textFont.size(text)[0])
    elif direc == "." and "." in text :
        distToDec = len(text.split(".")[0]) * (textFont.size(text)[1] / 2)
        posX = (pos[0] - distToDec)
    else:
        posX = pos[0]
    # add/render the text to screen
    screen.blit(textObject, (posX, pos[1]))

string = "memes"
width = 50

while 1:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE :
                screen = pygame.display.set_mode(event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                pygame.display.flip()

    screen.fill((40, 40, 40))

    pygame.draw.line(screen, c["red"], (100,100), (100,150), 1)
    pygame.draw.line(screen, c["red"], (100 + width, 100), (100 + width, 150), 1)

    textFunc(string, c["white"], (100,100), widthLim=width)

    pygame.display.update()