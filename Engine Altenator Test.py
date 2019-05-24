import krpc

conn = krpc.connect(name="Charge Resources")
vessel = conn.space_center.active_vessel

def elecGeneration() :
    genDict = {"cells":1.5,"cellArrays":18.0,"rtg":0.8}
    # partType can be: panels, cells, generators or, alternators
    panels         = vessel.parts.solar_panels
    cells          = vessel.parts.with_title("Fuel Cell")
    cellArrays     = vessel.parts.with_title("Fuel Cell Array")
    generators     = vessel.parts.with_title("PB-NUK Radioisotope Thermoelectric Generator")
    allAlternators = vessel.parts.with_module("ModuleAlternator")
    alternators    = []
    other          = cells + cellArrays + generators

    panelGen      = 0
    alternatorGen = 0
    otherGen      = 0
    cellGen       = 0
    totalGen      = 0

    # filter out engines that arent in the current stage
    for alternator in allAlternators :
        currentStage = vessel.control.current_stage
        if alternator.stage == currentStage :
            alternators.append(alternator)

    # energy production panels
    for panel in panels :
        panelGen =+ panel.energy_flow

    # production from alternators
    for alternator in alternators :
        #print(alternator.modules[4].fields)

        alternatorGen =+ float(alternator.modules[4].get_field("Alternator Output"))
        #print(alternatorGen)

    for item in vessel.parts.with_module("ModuleGenerator") :
        #print(item.name)
        pass

    for item in cells :
         for mod in item.modules :
             try:
                 try:
                     cell = int(str(mod.get_field("Fuel Cell")).strip("output cap: ")[:-1])/100*genDict["cells"]
                 except ValueError:
                     cell = 0
                 cellGen += float(cell)
             except krpc.error.RPCError:
                 pass
             #print(cellGen)

    for item in cellArrays:
        for mod in item.modules:
            #print(mod.get_field("Fuel Cell Array"))
            pass


    infoToReturn = {"panels": panelGen,
                    "alternators" : alternatorGen,
                    "fuel cells" : cellGen,
                    "other": otherGen,
                    "total": totalGen}

    return infoToReturn

while True:
    elecGeneration()