# Introduction

In Hawaii's forests, Ohia trees are one of the ecologically important species in native Hawaiian Forests. A new pathogen known as Rapid Ohia Death (ROD) is a newly identified fungus that threatens native forests. Creating a visualization of the spread of Rapid Ohia Death is critical to communicating the danger this pathogen presents to Hawaii's forests. This software is a tool that helps us show the spread of Rapid Ohia Death. If you have the right data and the computing power, you could use this software to visualize any forest.<br>

We use [Blender](https://www.blender.org/download/) as our 3D modeling software and [Python](https://www.python.org/downloads/) to generate tree models and render images of our virtual forest. The data was provided to us by Dr. Ryan Perroy, a researcher on the spread of Rapid Ohia Death. The models that we used are in .fbx format, and we made in Blender using the Tree Sapling Plugin. 

The code was written by [Mark Jimenez](https://github.com/kerneltrick), [Ryp Ring](https://github.com/rypring) and Carina Shintaku

<br>

# How to use this code

**Data**

We first must understand the format of the data. Data given to us on the spread of Rapid Ohia Death cannot be shared publicly, however, the format of the data is roughly as seen below:

|Tree ID     | X_Coordinate |  Y_Coordinate       |  TimeStamp1
|------------|--------------|---------------------|-----------------
|1           |  2313.13     |  1278.90            |  4
|2           |  2452.45     |  1523.84            |  4
|3           |  2567.21     |  1442.54            |  2
|4           |  2242.05     |  1434.89            |  0

Tree_ID is an arbitrary number that identifies a particular tree, X_coordinate and Y_coordinate are the position of the tree and timestamp1 is the 'health' of a tree. 4 means the tree is healthy, 3 means that the tree is starting to yellow, 2 means the tree is starting to turn red (a clear sign of ROD, in this case) 1 means the tree has turned brown and is dying and 0 means the tree is a skeleton and is completely dead.

We had about 4000 total trees, with about 60 timestamps, what you see above is simply an example. 

The basic idea here is we place a tree at its coordinate, and choose the appropriate 3D model of a tree to place (as indicated by its health) <br>

**Models**

Now that we understand the format of the data this code uses, we need models to put into our 3D environment.  We created .fbx models in Blender with the tree sapling plugin and used those as our models. 

If you want to use more realistic models or any other model in .fbx format, that is fine. We chose "simple" models because it is very computationally demanding to make renders of 3D environments. Name the models as "0.fbx", "1.fbx", "2.fbx", "3.fbx" and "4.fbx" so that a model has the same name of the health of a tree. In order to add more variation to our forest, we had several folders with these 5 fbx files in them. These folders are named 1, 2 and 3. An example filepath to these models would be: "./tree_models/3/4.fbx" denoting a tree of type 4 (Healthy) and variation 3.

![](/github/tree_example.JPG)

We also need a terrain to place our trees on, so we made another model in Blender that is just a plane. Again, we kept it simple due to the computational demands of this program.

**Code**

At the top of the script, there's a config that allows you to tweak variables based on the type of visualization you want to make. 

MAX_ORD is the size of the x,y plane that the visualization will be generated on.

CAMERA_HEIGHT is the height of the camera, pointed towards the origin. 

START is the timestamp that you want to start at (should be 0)

STOP is the timestamp that you want to end at

FRAMES_PER_STEP is the number of frames at a particular location 

NUM_TREE_VARIETIES would be the number of variations on the fbx tree models you've used

**Run the code**

Now that we have the data, models and source code in the same directory, we can run the code using the following:

```bash
blender -P blender_forest.py
```

This will create a directory of images that will be used to make a short video of your visualization.

This program is very computationally intensive, and will take on the order of a few hours to render the whole set of images, depending on the number of trees, textures in the environment, etc. 

If someone wanted to be more creative with the environment they are putting the trees in, they can simply edit a .blend file and make an environment that they like. Then they would use:

```bash
blender --background myFile.blend -P blender_forest.py
```

It should be noted that all the trees are placed at z = 0, meaning that they are all on the ground.  

<br>

# Visualizing Rapid Ohia Death Spread

![2D Rod Spread Vizualization](/github/ohia_spread_2d.gif)

 
  

