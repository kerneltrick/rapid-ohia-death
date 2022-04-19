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
xPos, yPos, zPos = getCoords(os.path.expanduser("~/Desktop/Kapapala.csv"))

# find minimum x and y coordinates to bring trees closer to origin
xMin = min(xPos)
yMin = min(yPos)

# final x, y positions
x = []
y = []

# normalize every point and add to x and y list
for point in xPos:
    x.append(point - xMin)

for point in yPos:
    y.append(point - yMin)

# create a tree for every point
# may want to verify that lists x and y are same size
for i in range(len(xPos)):
    bpy.ops.curve.tree_add(do_update=True, bevel=True, prune=False, showLeaves=False, useArm=False, seed=0, handleType='0', levels=2, length=(0.8, 0.6, 0.5, 0.1), lengthV=(0, 0.1, 0, 0), taperCrown=0.5, branches=(0, 55, 10, 1), curveRes=(8, 5, 3, 1), curve=(0, -15, 0, 0), curveV=(20, 50, 75, 0), curveBack=(0, 0, 0, 0), baseSplits=3, segSplits=(0.1, 0.5, 0.2, 0), splitByLen=True, rMode='rotate', splitAngle=(18, 18, 22, 0), splitAngleV=(5, 5, 5, 0), scale=5, scaleV=2, attractUp=(3.5, -1.89984, 0, 0), attractOut=(0, 0.8, 0, 0), shape='7', shapeS='10', customShape=(0.5, 1, 0.3, 0.5), branchDist=1.5, nrings=0, baseSize=0.3, baseSize_s=0.16, splitHeight=0.2, splitBias=0.55, ratio=0.015, minRadius=0.0015, closeTip=False, rootFlare=1, autoTaper=True, taper=(1, 1, 1, 1), radiusTweak=(1, 1, 1, 1), ratioPower=1.2, downAngle=(0, 26.21, 52.56, 30), downAngleV=(0, 10, 10, 10), useOldDownAngle=True, useParentAngle=True, rotate=(99.5, 137.5, 137.5, 137.5), rotateV=(15, 0, 0, 0), scale0=1, scaleV0=0.1, pruneWidth=0.34, pruneBase=0.12, pruneWidthPeak=0.5, prunePowerHigh=0.5, prunePowerLow=0.001, pruneRatio=0.75, leaves=150, leafDownAngle=30, leafDownAngleV=-10, leafRotate=137.5, leafRotateV=15, leafScale=0.4, leafScaleX=0.2, leafScaleT=0.1, leafScaleV=0.15, leafShape='hex', bend=0, leafangle=-12, horzLeaves=True, leafDist='6', bevelRes=1, resU=4, armAnim=False, previewArm=False, leafAnim=False, frameRate=1, loopFrames=0, wind=1, gust=1, gustF=0.075, af1=1, af2=1, af3=4, makeMesh=False, armLevels=2, boneStep=(1, 1, 1, 1))

# change position of each tree to normalized x,y coordinates
i = 0
for tree in bpy.data.objects:
    tree.location = (x[i], y[i], zPos[i])
    i += 1
