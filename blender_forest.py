import bpy
import os
import csv
import numpy as np

class DataLoader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = None
        self.rangeX = None
        self.rangeY = None

    def _set_range(data):
        xMin = None
        xMax = None
        yMin = None
        yMax = None
        for tree in data:
            if xMax is None or tree["x"] > xMax:
                xMax = tree["x"]
            elif xMin is None or tree["x"] < xMax:
                xMax = tree["x"]
            if yMax is None or tree["y"] > yMax:
                yMax = tree["y"]
            elif xMin is None or tree["y"] < yMax:
                yMax = tree["y"]
        self.rangeX = (xMin, xMax)
        self.rangeY = (yMin, yMax)

    def _crop(data, cropRangeX, cropRangeY):



    # get x,y,z coordinates of trees from given filepath
    def load(self):
        data = []
        # open file
        with open(self.fileName, newline='') as csvfile:
            reader = csv.reader(csvfile)
            reader.__next__()
            i=0
            for row in reader:
                tree = {}
                tree["x"] = float(row[1])
                tree["y"] = float(row[2])
                # z is always 0; no consideration of terrain
                tree["z"] = 0
                tree["health"] = [float(x) for x in row[3:]]
                data.append(tree)
                i+=1
                if i > 10:
                    break
        data = self._section(data, (x1, x2), (y1, y2))
        self.data = data
        return self.data

class Tree:
    def __init__(self, x, y, z=0):
        self.type = fileName[0]
        self.x = x
        self.y = y
        self.z = z
        self.tree = None

    def load(self, fileName):
        bpy.ops.import_scene.fbx( filepath = fileName )
        self.tree = bpy.context.object
        self.tree.location = (self.x, self.y, self.z)

class Forest:
    def __init__(self, locationData):
        self.locationData = locationData
        self._models_dir = "./tree_models/"
        self.trees = self._build_forest()

    def _build_forest(self):
        """
        locationData - [{"x","y","z","health"}]
        """
        trees = []
        for row in self.locationData:
            path = self._models_dir + "1/4.fbx"
            tree = Tree(row["x"], row["y"], row["z"])
            tree.load(path)
            trees.append(tree)

        return trees

def time_lapse(forest):
    pass

def load_location_data(fileName):
    loader = DataLoader(fileName)
    data = loader.load()
    return data

def main(args):
    locationData = load_location_data(args["fileName"])
    forest = Forest(locationData)
    time_lapse(forest)

if __name__ == "__main__":
    fileName = "kapapala_tracking.csv"
    args = {"fileName":fileName}
    main(args)
