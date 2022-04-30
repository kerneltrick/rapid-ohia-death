import bpy
import os
import csv

# get x,y,z coordinates of trees from given filepath
def getCoords(file):
    # list of coordinates
    xCoord = []
    yCoord = []
    zCoord = []

    # open file
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # append x,y,z coordinates
            # z is always 0; no consideration of terrain
            xCoord.append(float(row['POINT_X']))
            yCoord.append(float(row['POINT_Y']))
            zCoord.append(0)
            # first ten coordinates only, if you want
            #if len(zCoord) >= 10:
                #break
    return (xCoord, yCoord, zCoord)

# unpack tuple into 3 seperate lists
# path to file is hardcoded from Ryp's machine
xPos, yPos, zPos = getCoords(os.path.expanduser("./kapapala_tracking.csv"))

# find minimum x and y coordinates to bring trees closer to origin
xMin = min(xPos)
yMin = min(yPos)

# final x, y positions
x = []
y = []

# normalize every point and add to x and y list
# x1 and x2 are the range to generate trees in
x1 = 0
x2 = 200
for i in range(len(xPos)):
    xPoint = xPos[i] - xMin
    yPoint = yPos[i] - yMin
    if (xPoint >= x1) and (xPoint <= x2):
        x.append(xPoint)
        y.append(yPoint)

# create a tree for every point
# may want to verify that lists x and y are same size
for i in range(len(x)):
    bpy.ops.import_scene.fbx("/users/mark/Repos/rapid-ohia-death/tree_models/1/4.fbx")

# change position of each tree to normalized x,y coordinates
i = 0
for tree in bpy.data.objects:
    tree.location = (x[i], y[i], zPos[i])
    i += 1
