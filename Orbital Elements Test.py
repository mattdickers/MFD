import sys, pygame, krpc, time, math
import numpy as np

conn = krpc.connect(name="Orbit")
ksc = conn.space_center
vessel = conn.space_center.active_vessel
orbit = vessel.orbit

G = 6.67408e-11
π = np.pi
deg = np.pi/180
μ = vessel.orbit.body.gravitational_parameter

t0 = ksc.ut
i = orbit.inclination
Ω = orbit.longitude_of_ascending_node
ω = orbit.argument_of_periapsis
e = orbit.eccentricity
a = orbit.semi_major_axis
M0 = orbit.mean_anomaly_at_epoch
V0 = orbit.true_anomaly
epoch = orbit.epoch
period = orbit.period

prevOrbit = 0.25
nextOrbit = 1.5
detail = 500

tmin = epoch - prevOrbit*period
tmax = tmin + nextOrbit*period
dt = np.linspace(tmin,tmax,detail)

def lonOfPe():
    PeriLon = (Ω + ω) % (2 * π)
    return PeriLon/deg
#works, but done know if is correct

# while True:
#     i = orbit.inclination
#     θ = ω + V
#     lat1 = np.arcsin(np.sin(θ)*np.sin(i))
#     lat = lat1/deg
#     print(lat)

def EccentricAnomalyIterate():
    global E
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
    return E

def ConvertToCartesian():
    q = np.array([[a*(np.cos(E)-e)],
                 [a*np.sqrt(1-e**2)*np.sin(E)],
                  [0]],dtype=np.float64)
    qx = q[0][0]
    qy = q[1][0]

    x = np.linspace(tmin,tmax,detail)
    y = np.linspace(tmin,tmax,detail)
    z = np.linspace(tmin,tmax,detail)
    #r = (a*(1-e**2))/(1+e*np.cos(V)) #degrees
    #r1 = (a * (1 - e ** 2)) / (1 + e * np.cos(V)*deg) #radians

    R_Ω = np.array([[np.cos(Ω), -np.sin(Ω), 0],
                    [np.sin(Ω), np.cos(Ω), 0],
                    [0, 0, 1]])
    R_i = np.array([[1, 0, 0],
                   [0, np.cos(i), -np.sin(i)],
                   [0, np.sin(i), np.cos(i)]])
    R_ω = np.array([[np.cos(ω), -np.sin(ω), 0],
                    [np.sin(ω), np.cos(ω), 0],
                   [0, 0, 1]])

    xyzMatrix = np.matmul(np.matmul(R_Ω,R_i),R_ω)
    #q1 = [q[0][0].tolist(),q[1][0].tolist(),q[2].tolist()]
    print(np.matmul(q,xyzMatrix)) #TODO need to fix fact that q is an array of arrays, and hence cannot be multiplied -> maybe set q datatype to float, and make z values be an aray of all 0s

def GetLatLon():
    M1 = M0 + np.sqrt((μ) / (a ** 3)) * (dt - epoch)

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
    return lat, lon #TODO check how logical these values are

#M1 = M0 + np.sqrt((μ)/(a**3))*(dt-epoch)
#EccentricAnomalyIterate()
#ConvertToCartesian2()
lat, lon = GetLatLon()
print(lon)