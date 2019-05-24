import krpc
import time

conn = krpc.connect(name="Temperature")
vessel = conn.space_center.active_vessel

parts = vessel.parts.all

maxTemp = parts[0].max_temperature
maxSkinTemp = parts[0].max_skin_temperature

engines = [vessel.parts.engines[i].part.title for i in range(len(vessel.parts.engines))]
#print(engines)

#print(parts[part].title)
#if parts[part].title in engines:
#    print(True)
#else:
#    print(False)

#Hottest Part Temp:
# while True:
#     temps = [parts[i].skin_temperature for i in range(len(parts))]
#     hottest = temps.index(max(temps))
#     print(parts[hottest].title)

#Root Part Temp:
#print(parts[0].skin_temperature)

#time.sleep(1)

# while True:
#     temp = parts[part].temperature
#     skinTemp = parts[part].skin_temperature
#     print(str(round(temp,1))+"/"+str(maxTemp),str(int(temp/maxTemp*100))+"%")
#     #pass