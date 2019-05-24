#Science Getter
import krpc,pygame,sys
pygame.init()

conn = krpc.connect(name="Science")
vessel = conn.space_center.active_vessel

screen = pygame.display.set_mode((750, 750))
font  = pygame.font.SysFont("courier new", 20)

firstPos = 100
scroll = 0

#Fix Scrolling
#Creates the GUI from the other subprograms
def DrawGUI(scroll):
    global overlap
    overlap = int(round(len(ScienceModules())/6,1))
    print(overlap)
    print(len(ScienceModules())/6)
    Min = scroll
    Max = (len(ScienceModules())-overlap)+scroll
    print(Min, Max, "\n")
    for i in range(Min,Max):
        ModuleWindow(i,scroll)
    Options()

#Gets the list of experiments on the vessel
def ScienceModules():
    experiments = vessel.parts.experiments
    return experiments

#Gets the data and draws onto GUI
def ModuleWindow(num,scroll):
    #Defines fonts and experiment boxes
    experimentStatus = {True:"Deployed",False:"Available"}
    smallFont  = pygame.font.SysFont("courier new", 16)
    area = pygame.Rect(firstPos,firstPos*(num+1),450,75)
    pygame.draw.rect(screen,(255,255,255),area,2)

    #Gets user friendly experiment title
    title = ScienceModules()[num].part.title
    titleObject = font.render(title,False,(255,255,255))
    screen.blit(titleObject,(firstPos+10,firstPos*(num+1)+10))

    #Displays experiment status; Available, Deployed or Inoprable
    if ScienceModules()[num].inoperable is True:
        status = "Status:Inoperable"
    elif ScienceModules()[num].available is True:
        status = "Status:"+experimentStatus[ScienceModules()[num].has_data]
    else:
        status = "Status:Unavailable"
    statusObject = smallFont.render(status,False,(255,255,255))
    screen.blit(statusObject,(firstPos+10,firstPos*(num+1)+40))

    #Gets the amount of science held in each experiment
    try:
        science = "Science:"+str(round(ScienceModules()[num].data[0].science_value,2))
    except IndexError:
        science = "Science:0.0"
    scienceObject = smallFont.render(science,False,(255,255,255))
    screen.blit(scienceObject,(firstPos+195,firstPos*(num+1)+40))

#Displays control options for experiments
def Options():
    #Temporary Scroll Button:
        pass

#PyGame GUI
while 1 :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((40, 40, 40))
    DrawGUI(scroll)
    #print(vessel.parts.sensors[0].value)

##    click = pygame.mouse.get_pressed()
##
##    if click[0] == 1:
##        print("Left Click")
##        scroll = 1
##    elif click[2] == 1:
##        print("Right Click")
##        scroll = -1
   
    pygame.display.update()

##experiments = vessel.parts.experiments
##
##for i in range(len(experiments)):
##    print(experiments[i].part.name)
##    #pass
##
##experiments[2].run()
##print(experiments[2].science_subject.title)
##print(experiments[2].biome)
##experiments[2].reset()



