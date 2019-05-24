import krpc, math
import time
conn = krpc.connect(name="Stage Splitter")
vessel = conn.space_center.active_vessel

stage = 0

partStages = []
partActivateStages = []
missingParts = []
allParts = vessel.parts.all

#Seperate all parts that are decoupled and activated into correct stages
while len(vessel.parts.in_stage(stage)) != 0:
    partStages.append(vessel.parts.in_decouple_stage(stage))
    partActivateStages.append(vessel.parts.in_stage(stage))
    stage += 1
print(partStages)

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

# Get wet and dry masses of each stage
massStages = [[] for i in range(len(partStages))]
dryMassStages = [[] for i in range(len(partStages))]

################# FOR TRANSFER (massStages at least)
for Stage in range(len(massStages)):
    massStages[Stage].append(sum(part.mass for part in partStages[Stage])
                             + sum(part.mass for part in partActivateStages[Stage])) #NEED TO ADD MISSING PARTS MASS WHEN FINDING TOTAL MASS

for Stage in range(len(massStages)):
    dryMassStages[Stage].append(sum(part.dry_mass for part in partStages[Stage])
                             + sum(part.dry_mass for part in partActivateStages[Stage])) #NEED TO ADD MISSING PARTS MASS WHEN FINDING TOTAL MASS
print(massStages)
print(dryMassStages)
print(sum(part.dry_mass for part in missingParts))

#Stage DeltaV
stage = 3
for Stage in range(stage,-1,-1):
    for part in partStages[Stage]: #if get error here, stage number probably too high/wrong
        part.highlighted = True
    for part in partActivateStages[Stage]:
        part.highlighted = True
for part in missingParts:
    part.highlighted = True

################# FOR TRANSFER (maybe) -> not really used anymore
stageMass = sum(mass for Stage in range(stage,-1,-1) for mass in massStages[Stage]) + sum(part.mass for part in missingParts)
print(stageMass)
stageDryMass = dryMassStages[stage][0] + sum(mass for Stage in range(stage-1,-1,-1) for mass in massStages[Stage]) +  \
                sum(part.dry_mass for part in missingParts)
print(stageDryMass)
for Stage in range(stage-1,-1,-1):
    #print(Stage)
    pass


################# FOR TRANSFER
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
stageDryMass = stageMass - sum(mass[fuel] if fuel in fuelMasses[stage-1][0] else 0 for fuel in fuelTypes for mass in fuelMasses[stage-1])
print(stageDryMass)

#Test Dv calculation:
mass = stageMass
dryMass = stageDryMass
isp = 250.77942904644047
Dv = (vessel.orbit.body.surface_gravity*isp)*(math.log(mass/dryMass))
print(Dv)

#TODO use masses of one stage less than when the engine is activated