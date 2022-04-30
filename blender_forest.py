import bpy
import os
import csv
import math
import random

MAX_ORD = 5
PI = 3.14159265
CROP_RANGE_X = (-MAX_ORD, MAX_ORD)
CROP_RANGE_Y = (-MAX_ORD, MAX_ORD)
TIME_STEPS = 60
FRAMES_PER_STEP = 5

def flip_coin():
    val = random.random()
    if val > 0.75:
        return True
    return False

class DataLoader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = None
        self.rangeX = None
        self.rangeY = None

    def _set_range(self):
        xMin = None
        xMax = None
        yMin = None
        yMax = None
        for tree in self.data:
            if xMax is None or tree["x"] > xMax:
                xMax = tree["x"]
            elif xMin is None or tree["x"] < xMin:
                xMin = tree["x"]
            if yMax is None or tree["y"] > yMax:
                yMax = tree["y"]
            elif yMin is None or tree["y"] < yMin:
                yMin = tree["y"]
        self.rangeX = (xMin, xMax)
        self.rangeY = (yMin, yMax)

    def __in_range(self, val, range):
        min, max = range
        if val > min and val < max:
            return True
        return False

    def _crop(self, cropRangeX, cropRangeY):
        data = []
        for tree in self.data:
            if self.__in_range(tree["x"], cropRangeX) and self.__in_range(tree["y"], cropRangeY):
                data.append(tree)
        self.data = data
        self._set_range()
        self._center()

    def _center(self):
        minX, maxX = self.rangeX
        minY, maxY = self.rangeY
        centerX = (maxX + minX)/2.0
        centerY = (maxY + minY)/2.0
        for tree in self.data:
            tree["x"] -= centerX
            tree["y"] -= centerY
        self._set_range()

    # get x,y,z coordinates of trees from given filepath
    def load(self):
        data = []
        # open file
        with open(self.fileName, newline='') as csvfile:
            reader = csv.reader(csvfile)
            reader.__next__()
            for row in reader:
                tree = {}
                tree["x"] = float(row[1])
                tree["y"] = float(row[2])
                # z is always 0; no consideration of terrain
                tree["z"] = 0
                tree["health"] = [int(x) for x in row[3:]]
                data.append(tree)
        self.data = data
        self._set_range()
        self._center()
        self._crop(CROP_RANGE_X, CROP_RANGE_Y)
        return self.data

class Tree:
    def __init__(self, x, y, z=0, healthHistory = None ):
        self.x = x
        self.y = y
        self.z = z
        self.type = random.randint(1,1)
        self.health = healthHistory[0]
        self.healthHistory = healthHistory
        self.tree = None

    def load(self, health=4):
        self.health = health
        fileName = "./tree_models/{}/{}.fbx".format(self.type, self.health)
        bpy.ops.import_scene.fbx( filepath = fileName )
        self.tree = bpy.data.objects[-1]
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
            tree = Tree(row["x"], row["y"], row["z"], row["health"])
            tree.load()
            trees.append(tree)
        return trees

    def update(self, timeStep, strict=False):
        i = 0
        for tree in self.trees:
            if tree.health != tree.healthHistory[timeStep]:
                if flip_coin() or strict:
                    print("ROD SPREAD in tree {}".format(i))
                    tree.load(health=tree.healthHistory[timeStep])
            i += 1

def render_image(outputDir="./images/", index="0"):
    bpy.context.scene.render.filepath = os.path.join(outputDir, index)
    bpy.ops.render.render(write_still = True)

def move_camera(tx, ty, tz):
    rx = ((180.0 / PI) * math.asin(ty/(tx+.001)))
    ry = ((180.0 / PI) * math.acos(tx/(ty+.001)))
    if ty < 0.1 and ty > -0.1:
        rz = 0
    else:
        rz = ((180.0 / PI) * math.atan2(tx,(ty+.001)))
    print("coords:",tx, ty)
    print("angles:",rx, ry, rz)
    fov = 50.0

    scene = bpy.data.scenes["Scene"]
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.camera.data.angle = fov*(PI/180.0)
    scene.camera.rotation_mode = 'XYZ'
    scene.camera.rotation_euler[0] = rx*(PI/180.0)
    scene.camera.rotation_euler[1] = ry*(PI/180.0)
    scene.camera.rotation_euler[2] = rz*(PI/180.0)
    scene.camera.location.x = tx
    scene.camera.location.y = ty
    scene.camera.location.z = tz

def time_lapse(forest):
    i = 0
    r = MAX_ORD + 25
    tz = 35.0
    for timeStep in range(TIME_STEPS-1):
        for f in range(FRAMES_PER_STEP):
            forest.update(timeStep+1)
            tx = r * math.cos(3.0*i*(PI/180.0))
            ty = r * math.sin(3.0*i*(PI/180.0))
            move_camera(tx, ty, tz)
            render_image(index=str(i))
            i += 1
        forest.update(timeStep+1, strict=True)

def load_location_data(fileName):
    loader = DataLoader(fileName)
    data = loader.load()
    return data

def load_terrain():
    fileName = "./tree_models/plane.fbx"
    bpy.ops.import_scene.fbx( filepath = fileName )

def create_light():
    light_data = bpy.data.lights.new(name="my-light-data", type='SUN')
    light_data.energy = 5
    light_object = bpy.data.objects.new(name="my-light", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = (60, 60, 60)

def delete_cube_and_light():
    objs = bpy.data.objects
    objs.remove(objs["Light"], do_unlink=True)
    objs.remove(objs["Cube"], do_unlink=True)

def setup():
    delete_cube_and_light()
    create_light()
    #load_terrain()

def main(args):
    setup()
    locationData = load_location_data(args["fileName"])
    forest = Forest(locationData)
    time_lapse(forest)

if __name__ == "__main__":
    fileName = "kapapala_tracking.csv"
    args = {"fileName":fileName}
    main(args)
