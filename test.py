import krpc, math
import time
conn = krpc.connect(name="Delta V Calculator")
vessel = conn.space_center.active_vessel
#TODO use for one of them dank memes boi
stage = 0

while True:
    partStages = []
    partActivateStages = []

    engines = vessel.parts.engines

    while len(vessel.parts.in_stage(stage)) != 0:
        partStages.append(vessel.parts.in_decouple_stage(stage))
        partActivateStages.append(vessel.parts.in_stage(stage))
        stage += 1

    engineStages = [[] for i in range(len(partStages))]

    for engine in engines:
        engineData = []
        for stage in range(len(partStages)):
            for part in partStages[stage]:
                if engine.part == part:
                    #print(stage,"\n")
                    engineData.append(engine)
                    engineStages[stage].append(engine)


    for stage in range(len(partStages)):
        for part in partStages[stage]:
            part.highlighted = True
            time.sleep(000.1)
            part.highlighted = False
        for part in partActivateStages[stage]:
            part.highlighted = True
            time.sleep(000.1)
            part.highlighted = False