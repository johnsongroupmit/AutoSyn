# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:16:58 2020

@author: atlan
"""

import shapely.geometry as sg

regions = []
regions.append([[0,0],[0,200],[100,200],[100,0]])
regions.append([[100,0],[100,200],[200,200],[200,0]])
height = [10,5]

polygons = []
for region in regions:
    polygons.append(sg.Polygon(region))
    
# =============================================================================
# lines = []
# for region in regions:
#     sides = []
#     for i in range(len(region)-1):
#         #print(i)
#         sides.append([region[i],region[i+1]])
#     sides.append([region[-1],region[0]])
#     lines.append(sides)
# =============================================================================
    
# =============================================================================
# Intersection calculation
# =============================================================================
# =============================================================================
# def cross_product(p1, p2):
# 	return p1[0] * p2[1] - p2[0] * p1[1]
# 
# def subtract(p1, p2):   #subtract p2 from p1
#     point = [p1[0] - p2[0], p1[1] - p2[1]]
#     return point
# 
# def direction(p1, p2, p3):
# 	return  cross_product(subtract(p3,p1), subtract(p2,p1))
# 
# def on_segment(p1, p2, p):
#     return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])
# 
# def intersect(line1, line2):
#     p1 = line1[0]
#     p2 = line1[1]
#     p3 = line2[0]
#     p4 = line2[1]
#     
#     d1 = direction(p3, p4, p1)
#     d2 = direction(p3, p4, p2)
#     d3 = direction(p1, p2, p3)
#     d4 = direction(p1, p2, p4)
# 
#     if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
#         ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
#         return 1
# 
#     elif d1 == 0 and on_segment(p3, p4, p1):
#         return 1
#     elif d2 == 0 and on_segment(p3, p4, p2):
#         return 1
#     elif d3 == 0 and on_segment(p1, p2, p3):
#         return 1
#     elif d4 == 0 and on_segment(p1, p2, p4):
#         return 1
#     else:
#         return 0
# =============================================================================

# =============================================================================
# Intersection calculation
# =============================================================================





regions = []
regions.append([[0,0],[0,200],[100,200],[100,0]])
regions.append([[100,0],[100,200],[200,200],[200,0]])
height = [10,5]
   
track_raw = [[50,50],[160,60]]

def clearance_height:
    safe_height = 0
    flag = 0
    lcl_safe_height = []
    
    polygons = []
    for region in regions:
        polygons.append(sg.Polygon(region))
        
    p1 = sg.Point(track_raw[0])
    p2 = sg.Point(track_raw[1])
    track = sg.LineString(track_raw)
    print(track)
    
    
    for i in range(len(polygons)):
        if polygons[i].contains(p1) and polygons[i].contains(p2):
            safe_height = height[i]
            flag = 1
            break
        if polygons[i].intersects(track):
            lcl_safe_height.append(height[i])
    
    if flag == 0:
        safe_height = min(lcl_safe_height)
    













def move(x=None, y=None, z=None, e=None, speed=None):         
    
    if x is not None or y is not None:
        
    #print "  ## move() ##"
    global currentPoint
    global lastPoint
    s = "G1 "
    if x is not None: 
        s += "X" + str(x) + " "
        lastPoint["x"]=currentPoint["x"]
        currentPoint["x"] = x 
    if y is not None: 
        s += "Y" + str(y) + " "
        lastPoint["y"]=currentPoint["y"]
        currentPoint["y"] = y 
    if z is not None: 
        s += "Z" + str(z) + " "
        lastPoint["z"]=currentPoint["z"]
        currentPoint["z"] = z 
    if e is not None:
        s += "E"+ str(-e) + " "
        lastPoint["e"]=currentPoint["e"]
        currentPoint["e"] = e
    if speed is not None:
        s += "F" + str(speed)
        lastPoint["speed"]=currentPoint["speed"]
        currentPoint["speed"] = speed

    #s += "\n"
    return s