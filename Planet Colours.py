import sys, pygame, krpc, time, math
pygame.init()

black       =   0,   0,   0
lightGrey   = 200, 200, 200
white       = 255, 255, 255
red         = 255,   0,   0
green       =   0, 255,   0
blue        =   0, 127, 255
PI          = math.pi
TWOPI       = 2*PI
HALFPI      = PI/2
font        = pygame.font.SysFont("courier new", 20)
planetColours = {"Sun":(255,240,0),"Kerbol":(255,240,0),"Moho":(95,76,65)
                 ,"Eve":(135,75,161),"Gilly":(116,102,91),"Kerbin":(30,60,200)
                 ,"Mun":(94,96,95),"Minmus":(97,147,128),"Duna":(111,47,27)
                 ,"Ike":(91,90,91),"Dres":(157,152,151),"Jool":(42,70,29)
                 ,"Laythe":(49,103,148),"Vall":(126,170,172),"Tylo":(167,157,143)
                 ,"Bop":(102,87,78),"Pol":(238,207,155),"Eeloo":(205,217,218)}
targetOrbit = (185,255,4)
manouverOrbit = (107,83,0)

screen = pygame.display.set_mode((1080, 768))

while 1:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()

    screen.fill((40, 40, 40))

    pygame.draw.circle(screen,planetColours["Kerbol"],(300,300),100,1)

    pygame.display.update()
