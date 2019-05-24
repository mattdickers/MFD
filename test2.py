import krpc, math
import time
conn = krpc.connect(name="Stage Splitter")
vessel = conn.space_center.active_vessel

stage = 3

fuelMasses = [[{}], [{'LiquidFuel': 900.0, 'Oxidizer': 1100.0}], [{}], [{'LiquidFuel': 2700.0, 'Oxidizer': 3300.0}], [{}]]
fuelTypes = ["LiquidFuel","Oxidizer","SolidFuel","MonoPropellant","XenonGas"]

# for fuel in fuelTypes:
#     #print(fuel)
#     for mass in fuelMasses[stage]:
#         try:
#             print(mass[fuel])
#         except KeyError:
#             pass

mass = vessel.mass - sum(mass[fuel] if fuel in fuelMasses[stage][0] else 0 for fuel in fuelTypes for mass in fuelMasses[stage])

#if fuelTypes[0] in fuelMasses[0][0]: