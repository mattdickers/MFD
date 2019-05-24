import krpc, math
import numpy
conn = krpc.connect(name="Delta V Calculator")
vessel = conn.space_center.active_vessel

mass = vessel.mass
dryMass = vessel.dry_mass
isp = vessel.specific_impulse
#print(isp)

Dv = (9.81*isp)*(math.log(mass/dryMass))
#print(round(Dv),"m/s")

stage = 0
partStages = []
partActivateStages = []
missingParts = []
allParts = vessel.parts.all

engines = vessel.parts.engines

#Seperate all parts that are decoupled and activated into correct stages
while len(vessel.parts.in_stage(stage)) != 0:
    partStages.append(vessel.parts.in_decouple_stage(stage))
    partActivateStages.append(vessel.parts.in_stage(stage))
    stage += 1

if len(partStages) == 1:
    mass = vessel.mass
    dryMass = vessel.dry_mass

    seaLevelPressure = vessel.orbit.body.pressure_at(0)
    pressure = vessel.flight().static_pressure / seaLevelPressure

    atmIsp = engines[0].kerbin_sea_level_specific_impulse
    vacIsp = engines[0].vacuum_specific_impulse
    isp = atmIsp + ((vacIsp - atmIsp) * (1 - pressure))

    Dv = (vessel.orbit.body.surface_gravity*isp)*(math.log(mass/dryMass))
else:
    engineStages = [[] for i in range(len(partStages))]
    engineDecoupleStages = {}

    for engine in engines:
        for stage in range(len(partStages)):
            for part in partActivateStages[stage]:
                if engine.part == part:
                    engineStages[stage].append(engine)
            for part in partStages[stage]:
                if engine.part == part:
                    engineDecoupleStages[engine] = stage
    for engine in engines:
        if engine not in engineDecoupleStages:
            engineDecoupleStages[engine] = 0

    #Remove duplicate parts from partActivatesStages (parts that were duplicated from partStages)
    for Stage in range(len(partActivateStages)):
        for part in partActivateStages[Stage]:
            for stage in range(len(partStages)):
                if part in partStages[stage]:
                    partActivateStages[Stage].remove(part)

    #Find any missing parts
    for stage in range(len(partActivateStages)):
        for part in allParts:
            if any(part in sl for sl in partActivateStages) is False:
                if any(part in sl for sl in partStages) is False:
                    if part not in missingParts:
                        missingParts.append(part)


    #Stage DeltaV
    stage = 4
    for Stage in range(stage,-1,-1):
        for part in partStages[Stage]: #if get error here, stage number probably too high/wrong
            part.highlighted = True
        for part in partActivateStages[Stage]:
            part.highlighted = True
    for part in missingParts:
        part.highlighted = True

    # mass = (sum(part.mass for Stage in range(stage,-1,-1) for part in partStages[Stage])
    #         + sum(part.mass for Stage in range(stage,-1,-1) for part in partActivateStages[Stage])
    #         + sum(part.mass for part in missingParts))
    # print(mass)
    #
    # dryMass = (sum(part.dry_mass for Stage in range(stage,-1,-1) for part in partStages[Stage])
    #         + sum(part.dry_mass for Stage in range(stage,-1,-1) for part in partActivateStages[Stage])
    #         + sum(part.dry_mass for part in missingParts))
    # print(dryMass)

    #Get masses of stages and dry masses
    massStages = [[] for i in range(len(partStages))]
    for Stage in range(len(massStages)):
        massStages[Stage].append(sum(part.mass for part in partStages[Stage])
                                 + sum(part.mass for part in partActivateStages[Stage]))
    stageMass = sum(mass for Stage in range(stage,-1,-1) for mass in massStages[Stage]) + sum(part.mass for part in missingParts)

    fuelMasses = [[] for i in range(len(partStages))]
    fuelTypes = ["LiquidFuel","Oxidizer","SolidFuel","MonoPropellant","XenonGas"]

    for Stage in range(len(fuelMasses)):
        fuels = {}
        for fuel in fuelTypes:
            if vessel.resources_in_decouple_stage(Stage, False).amount(fuel) == 0:
                pass
            else:
                fuels[fuel] = (vessel.resources_in_decouple_stage(Stage, False).amount(fuel) * vessel.resources.density(fuel))
        fuelMasses[Stage].append(fuels)
    stageDryMass = stageMass - sum(mass[fuel] if fuel in fuelMasses[engineDecoupleStages[engineStages[stage][0]]][0] else 0
                                       for fuel in fuelTypes for mass in fuelMasses[engineDecoupleStages[engineStages[stage][0]]])
    if stageDryMass == stageMass:
        stageDryMass = sum(part.dry_mass for part in partStages[stage]) + sum(part.dry_mass for part in partActivateStages[stage]) + sum(part.dry_mass for part in missingParts)
    #Current Specific Impulse of Each Engine
    engineIsp = {}
    seaLevelPressure = vessel.orbit.body.pressure_at(0)
    pressure = vessel.flight().static_pressure / seaLevelPressure
    for Stage in range(len(engineStages)):
        for engine in engineStages[Stage]:
            atmIsp = engine.kerbin_sea_level_specific_impulse
            vacIsp = engine.vacuum_specific_impulse

            isp = atmIsp + ((vacIsp - atmIsp) * (1 - pressure))
            engineIsp[engine] = isp

    #print(len(engineIsp),"\n")

    if len(engineStages[stage]) > 1:
        try:
            isp = sum(engine.available_thrust for engine in engineStages[stage]) \
                  / sum((engine.available_thrust) / (engineIsp[engine]) for engine in engineStages[stage])
        except ZeroDivisionError:
            isp = 0
    else:
        try:
            isp = engineIsp[engineStages[stage][0]]
        except IndexError:
            print("No engine in stage")

    mass = stageMass
    dryMass = stageDryMass
    Dv = (vessel.orbit.body.surface_gravity*isp)*(math.log(mass/dryMass))
print(Dv)

#TODO test with side boosters, might need to look at multiple engines activated in same stage
#TODO add check for engine propellant type