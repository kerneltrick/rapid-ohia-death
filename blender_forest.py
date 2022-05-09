import bpy
import os
import csv
import math
import random
import sys


"""
==================================
              CONFIG
==================================
"""
MAX_ORD = 40
CAMERA_HEIGHT = 30
PI = 3.14159265
CROP_RANGE_X = (-MAX_ORD, MAX_ORD)
CROP_RANGE_Y = (-MAX_ORD, MAX_ORD)
START = 0
STOP = 60
TIME_STEPS = START - STOP
FRAMES_PER_STEP = 5
NUM_TREE_VARIETIES = 1
OUTPUT_VIDEO = "ROD_SPREAD_3D.avi"
"""
==================================
"""

def flip_coin():
    val = random.random()
    if val > 0.50:
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
                tree["health"] = [int(x) for x in row[3+START:3+STOP]]
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
        self.z = 0.0
        self.type = random.randint(1,NUM_TREE_VARIETIES)
        self.health = healthHistory[0]
        self.healthHistory = healthHistory
        self.name = None

    def load(self, health=4):
        if health < 0:
            health = 0
        self.health = health
        if self.name is not None:
            objs = bpy.data.objects
            print("number of objects before removal:", len(objs))
            objs.remove(objs[self.name], do_unlink=True)
            print("number of objects after removal:", len(objs))

        fileName = "./blender/tree_models/{}/{}.fbx".format(self.type, self.health)
        bpy.ops.import_scene.fbx( filepath = fileName )
        self.name = bpy.context.selected_objects[0].name
        print("imported", self.name)
        tree = bpy.context.selected_objects[0]
        tree.location = (self.x, self.y, self.z)

class Forest:
    def __init__(self, locationData):
        self.locationData = locationData
        self._models_dir = "./blender/tree_models/"
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
        print("NUM TREES:", len(trees))
        return trees

    def update(self, timeStep, strict=False):
        for tree in self.trees:
            if tree.health != tree.healthHistory[timeStep]:
                if flip_coin() or strict:
                    print("ROD SPREAD")
                    treeHealth = tree.health - 1
                    if strict:
                        treeHealth = tree.healthHistory[timeStep]
                    tree.load(health=treeHealth)

def render_image(outputDir="./images/", index="0"):
    bpy.context.scene.render.filepath = os.path.join(outputDir, index)
    bpy.ops.render.render(write_still = True)

def move_camera(tx, ty, tz, rx, ry, rz):
    fov = 100.0
    scene = bpy.data.scenes["Scene"]
    scene.render.resolution_x =1920
    scene.render.resolution_y = 1030
    scene.camera.data.angle = fov*(PI/180.0)
    scene.camera.rotation_mode = 'XYZ'
    scene.camera.rotation_euler[0] = rx*(PI/180.0)
    scene.camera.rotation_euler[1] = ry*(PI/180.0)
    scene.camera.rotation_euler[2] = rz*(PI/180.0)
    scene.camera.location.x = tx
    scene.camera.location.y = ty
    scene.camera.location.z = tz

def time_lapse_circle(forest):
    i = 0
    r = 1.5 * MAX_ORD
    for timeStep in range(START, STOP-1):
        print("Renderring frame", timeStep)
        for f in range(FRAMES_PER_STEP):
            forest.update(timeStep+1)
            tx = r * math.cos(i*(PI/180.0))
            ty = r * math.sin(i*(PI/180.0))
            tz = CAMERA_HEIGHT
            rx = (180.0 / PI) * math.atan2(r, tz)
            ry = 0.0
            if ty < 0.1 and ty > -0.1:
                rz = (90.0) * (tx / abs(tx))
            else:
                rz = 180.0 - ((180.0 / PI) * (math.atan2(tx,(ty+.001))))
            print("moving camera")
            move_camera(tx, ty, tz, rx, ry, rz)
            print("rendering image")
            render_image(index=str(i))
            i += 1
        forest.update(timeStep+1, strict=True)
    render_video("./videos/" + CONFIG["OUTPUT_VIDEO"], "./images/3d/")
    print("TIMELAPSE COMPLETE")

def load_location_data(fileName):
    loader = DataLoader(fileName)
    data = loader.load()
    return data

def load_terrain():
    fileName = "./tree_models/ground.fbx"
    bpy.ops.import_scene.fbx( filepath = fileName )

def create_light():
    light_data = bpy.data.lights.new(name="my-light-data", type='SUN')
    light_data.energy = 5
    light_object = bpy.data.objects.new(name="my-light", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = (60, 60, 60)

def delete_cube_and_light():
    objs = bpy.data.objects
    if "Light" in objs:
        objs.remove(objs["Light"], do_unlink=True)
    if "my-light" in objs:
        objs.remove(objs["my-light"], do_unlink=True)
    if "Cube" in objs:
        objs.remove(objs["Cube"], do_unlink=True)

def setup():
    delete_cube_and_light()
    create_light()
    #load_terrain()

def main(args):
    setup()
    locationData = load_location_data(args["fileName"])
    forest = Forest(locationData)
    time_lapse_circle(forest)

def render_video(video_name="../videos/ohia_spread", image_folder="../images/3d"):
    date = datetime(2010, 6, 10)
    endDate = datetime(2021, 10, 23)
    date += timedelta(days=1)

    if len(sys.argv) > 1:
        image_folder = sys.argv[1]
    if len(sys.argv) > 2:
        video_name = sys.argv[2]
    images = [img for img in os.listdir(image_folder) if (img.endswith(".png") or img.endswith(".jpg"))]
    numImages = len(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    fps = 10
    video = cv2.VideoWriter(video_name, 0, fps, (width,height))

    timeIncrement = (endDate - date) /numImages
    for i in range(numImages):
        imageFileName = str(i) + ".png"
        path = os.path.join(image_folder, imageFileName)
        image = cv2.imread(path)
        window_name = 'Image'
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 150)
        fontScale = 4
        color = (255, 255, 255)
        thickness = 2
        text = date.strftime("Year: %Y")
        image = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
        org = (50, 400)
        text = date.strftime("Month: %m")
        image = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
        print("writing image", i)
        video.write(image)
        date += timeIncrement

    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    fileName = "kapapala_tracking.csv"
    print("reading data from:", fileName)
    args = {"fileName":fileName}
    main(args)
