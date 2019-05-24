#Vessel Viewer Test
import krpc
import time

conn = krpc.connect(name="Science")
vessel = conn.space_center.active_vessel

root = vessel.parts.root
stack = [(root,0)]
while stack:
    part, depth = stack.pop()
    if part.axially_attached:
        attach_mode = "Axial"
    else:
        attach_mode = "Radial"
    print(depth,part.title,"-",attach_mode)
    for child in part.children:
        stack.append((child,depth+1))
    part.highlighted = True
    time.sleep(0.1)
    
