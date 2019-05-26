import sys, pygame, krpc, time, math
import numpy as np
import matplotlib.pyplot as plt

pygame.init()

black = 0, 0, 0
lightGrey = 200, 200, 200
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 127, 255
PI = math.pi
TWOPI = 2 * PI
HALFPI = PI / 2
font = pygame.font.SysFont("courier new", 20)

screen = pygame.display.set_mode((1204, 768), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

Ap_markerL = pygame.image.load("pictures\Ap_markerL.png")
Pe_markerL = pygame.image.load("pictures\Pe_markerL.png")
Ap_markerM = pygame.image.load("pictures\Ap_markerM.png")
Pe_markerM = pygame.image.load("pictures\Pe_markerM.png")
Ap_markerS = pygame.image.load("pictures\Ap_markerS.png")
Pe_markerS = pygame.image.load("pictures\Pe_markerS.png")

conn = krpc.connect(name="Maps")
ksc = conn.space_center
vessel = conn.space_center.active_vessel

deg = np.pi / 180
km = 1000

leftAlign = 90
topAlign = 0


def drawCross(givenColor, crossPos, size=5, width=1):
    pos = list(crossPos)

    pygame.draw.line(screen, givenColor, (pos[0] + size, pos[1] + size), (pos[0] - size, pos[1] - size), width)
    pygame.draw.line(screen, givenColor, (pos[0] - size, pos[1] + size), (pos[0] + size, pos[1] - size), width)


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

def GetLatLon(dt):
    i = vessel.orbit.inclination
    ω = vessel.orbit.argument_of_periapsis
    Ω = vessel.orbit.longitude_of_ascending_node
    e = vessel.orbit.eccentricity
    a = vessel.orbit.semi_major_axis
    M0 = vessel.orbit.mean_anomaly_at_epoch
    V0 = vessel.orbit.true_anomaly
    μ = vessel.orbit.body.gravitational_parameter

    M1 = M0 + np.sqrt((μ) / (a ** 3)) * (dt - vessel.orbit.epoch)

    maxIter = 15
    maxError = 1e-11

    count = 0
    if e<0.8:
        E = M1
    F = E - e * np.sin(M1) - M1
    while np.all((np.abs(F) > maxError)) and np.all(count < maxIter):
        E = E - F / (1 - e * np.cos(E))
        F = E - e * np.sin(E) - M1
        count += 1

    V1 = 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(E/2))
    r = (a*(1-e**2))/(1+e*np.cos(V1))

    position = r*np.array([[np.cos(Ω)*np.cos(ω+V1) - np.sin(Ω)*np.sin(ω+V1)*np.cos(i)],
                           [np.sin(Ω)*np.cos(ω+V1) + np.cos(Ω)*np.sin(ω+V1)*np.cos(i)],
                           [np.sin(ω+V1)*np.sin(i)]])

    lat = np.sin(position[2]/r)/deg
    lon = np.arctan2(position[1],position[0])/deg
    return lat, lon

def DrawMap(mapPos, body, mapType, level, prevOrbit, nextOrbit, color, vessel):
    ksc = conn.space_center
    deg = math.pi / 180
    imgSize = 256  # size of each map image
    levelsDict = {0: [2, 1, 256, 128, 3, 100, 16], 1: [4, 2, 512, 256, 5, 200, 30], 2: [8, 4, 1024, 512, 7, 450, 45]}
    mapPosDict = {0: 0, 1: imgSize, 2: 3 * imgSize}  # defines where the map images are positioned
    latLonScales = {0: 81.48733086, 1: 162.9746617, 2: 325.9493235}  # Convters lat/lon to pixels based on level
    markerScales = {0: [Ap_markerS, Pe_markerS, 11], 1: [Ap_markerM, Pe_markerM, 17], 2: [Ap_markerL, Pe_markerL, 23]}
    detail = 500  # Number of points to plot in the orbit (500 is default)

    mapImages = [r"pictures\\map_images\\" + str(body) + "\\" + str(mapType) + "\\" + str(level) + "\\" + str(
        column) + "_" + str(row) + ".png"
                 for column in range(levelsDict[level][0]) for row in range(levelsDict[level][1])]
    for image in range(len(mapImages)):
        screen.blit(pygame.image.load(mapImages[image]), (mapPos[0] + (imgSize * int(mapImages[image][-7]))
                                                          , mapPos[1] + mapPosDict[level] - (
                                                                      imgSize * int(mapImages[image][-5]))))

    tmin = vessel.orbit.epoch - prevOrbit * vessel.orbit.period
    tmax = tmin + nextOrbit * vessel.orbit.period

    # array of times - evenly spaced
    dt = np.linspace(tmin, tmax, detail)

    # array of latitude and longitudes, converted to degrees
    lat, lon = GetLatLon(dt)

    # Convert lat and lon from degrees to pixels
    for i in range(len(lat)):
        lat[i] = np.radians(-(lat[i])) * latLonScales[level] + mapPos[1] + levelsDict[level][
            3]  # Made negative as for some reason it is inverted by default
        lon[i] = np.radians(lon[i]) * latLonScales[level] + mapPos[0] + levelsDict[level][2]
    points = list(zip(lon, lat))

    print(points)

    # Plot orbit
    for i in range(len(points)):
        try:
            if points[i + 1][0] - points[i][0] > 0:
                pygame.draw.line(screen, color, (points[i]), (points[i + 1]), level + 1)
        except IndexError:
            pass

    # # Plot Aposapsis and Periapsis
    # apoLat = orbit.latitude_at_apoapsis() / deg
    # apoLon = orbit.longitude_at_apoapsis() / deg
    #
    # periLat = orbit.latitude_at_periapsis() / deg
    # periLon = orbit.longitude_at_periapsis() / deg
    #
    # # Convert lat/lon of apo/peri to pixels
    # apoLat = np.radians(-apoLat) * latLonScales[level] + mapPos[1] + levelsDict[level][3]
    # apoLon = np.radians(apoLon) * latLonScales[level] + mapPos[0] + levelsDict[level][2]
    # periLat = np.radians(-(periLat)) * latLonScales[level] + mapPos[1] + levelsDict[level][3]
    # periLon = np.radians(periLon) * latLonScales[level] + mapPos[0] + levelsDict[level][2]
    #
    # screen.blit(markerScales[level][0],
    #             (int(apoLon) - int(markerScales[level][2] / 2), int(apoLat) - int(markerScales[level][2])))
    # screen.blit(markerScales[level][1],
    #             (int(periLon) - int(markerScales[level][2] / 2), int(periLat) - int(markerScales[level][2])))


    # Plot Vessel Position
    vesselLat = vessel.flight().latitude
    vesselLon = vessel.flight().longitude

    vesselLat = np.radians(-vesselLat) * latLonScales[level] + mapPos[1] + levelsDict[level][3]
    vesselLon = np.radians(vesselLon) * latLonScales[level] + mapPos[0] + levelsDict[level][2]

    drawCross(black, (vesselLon, vesselLat), levelsDict[level][4], level + 1)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            pygame.display.flip()

    screen.fill((40, 40, 40))

    DrawMap((100, 100), vessel.orbit.body.name, "sat", 0, 0.25, 1.5, red, vessel)
    # DrawMap((100,100),"eeloo","biome",2,0,0,red)

    pygame.display.update()

#TODO currently very very broken; does not display, likely problem with point calculation
