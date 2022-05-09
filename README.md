# Introduction

Ohia trees are one of the ecological keystones of native Hawaiian Forests. Their importance is imminent in Hawaiian ecology, but their cultural and religious significance is also key to Hawaii's people. A pathogen known as Rapid Ohia Death (ROD) is a newly identified fungus that threatens native forests. Creating a visualization of the spread of Rapid Ohia Death is critical to communicating the danger this pathogen presents to Hawaii's forests. This software is a tool that helps us show the spread of Rapid Ohia Death. If you have the right data and the computing power, you could use this software to render 3D visualizations of ROD progression in any forest. Moreover, if you are a ROD researcher, and you have data on the progression of this pathogen in Native Hawaiian forests, you can use our tools here to visualize your data in 3D, without needing to understand complicated graphical tools, but with a simple knowledge of Python. If you are an artist or software developer and you can expand on our efforts to visualize the destruction of this dangerous pathogen, we encourage you build on these tools, so we have provided documentation on the process and components of our system in this README.

We use [Blender](https://www.blender.org/download/) as our 3D modeling software and [Python](https://www.python.org/downloads/) to generate tree models and render images of our virtual forest. The data was provided to us by Dr. Ryan Perroy, a researcher on the spread of Rapid Ohia Death. The models that we used are in .fbx format, and we made in Blender using the Tree Sapling Plugin.


This project was motivated by the work of researchers at the University of Hawaii at Hilo on discovering the nature of ROD spread. You can read the work that inspired this project here: [Spatial Patterns of ‘Ōhi‘a Mortality Associated with Rapid ‘Ōhi‘a Death and Ungulate Presence](https://www.mdpi.com/1999-4907/12/8/1035).


The code was written by [Mark Jimenez](https://github.com/kerneltrick), [Ryp Ring](https://github.com/rypring) and Carina Shintaku

## Requirements

[Download Python 3](https://www.python.org/downloads/) Python3 is required in order to use this codebase. Download Python 3 to get started!

[Download Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) Conda is also needed! Conda is an open source package management sytem that runs on Mac, Winodows, and Linux! Conda runs and updates packages needed for this souce code.

# Visualizing Rapid Ohia Death Spread

## Location Data

ROD can spread over an extended time frame, causing devastation to an enormous landmass over the course of a decade or more. [Researchers at the Univrsity of Hawaii](https://www.mdpi.com/1999-4907/12/8/1035) have collected location data in order to track the spread of ROD over time in a single forest, and discover the patterns that characterize the communication of the pathogen through a forest. This 2-D data is useful for visualizing how large of an area ROD can spread over in a short time. If you want to get a quick, simple 2d visualization of your data use the script

```bash
/utils/2d_change_over_time.py
```

This script simply reads your data file (data format is discussed below), and outputs a heatmap that visualizes a 2d timelapse of the health of the fortest:

![2D Rod Spread Vizualization](/github/2d_rod_spread.gif)


## 3D Visualization in Blender

[Blender](https://www.blender.org/download/) is a 3D design tool used by designers and graphic artists for rendering 3D scenes. Blender can be used for rendering intensely vivid and realistic 3D worlds:

![3D Rod Spread Vizualization 1](/github/ohia_pointcloud.gif)

The designers of this codebase are not graphic artists, we are software developers, so we wanted to build a tool to allow other software developers to investigate the visualization of ROD spread patterns. This codebase is built on tools provided by the [PyPl bpy library](https://pypi.org/project/bpy/). Bpy is a set of tools that lets us control blender's rendering background programmitcally via [Python3](https://pypi.org/project/bpy/). Bpy utilizes Blender's low level Python functionality, so anything possible in Blender can also be accomplished in Bpy:

<br>

![3D Rod Spread Vizualization 2](/github/3d_rod_spread_2.gif)

## System Flowchart

Our system follows a very simple loop. Data is read in (data format is specified below), and we then use Bpy to build a full, healthy ohia forest from 3D tree models in Blender. Trees are placed in the forest according to their location data in the input csv. Then, a timelapse loop begins; for each iteration of this loop, the next timestep in the csv is read and used to update the health of the trees in the forest.

![System Flowchart](/github/flowchart.png)

# How to use this code

### Clone this repo

In order to run our render script, you will need to clone this repo. We assume you have git installed on your computer, if not, [please see these instructsions]. We also assume that you have some basic familiarity with command line tools and can navigate to the right place in your computer. Finally, we assume that you have followed the above recommendations to install Blender, Python and Conda, which are prerequisites to running our system. With those requisites out of the way, run:

```bash
git clone git@github.com:kerneltrick/rapid-ohia-death.git
```
### Setup

Now that you have the code, change your working directory to the repo. We have included a setup shell script that will load the tree models we used here for our forest. See the below section on tree models for details on how these tree models are saved.

```bash
chmod 777 ./setup.sh
./setup.sh
```

Once you are done setting up your codebase, you are ready to start visualizing, but first, lets talk about your data.

### Data

We first must specify the format of the data. Data given to us on the spread of Rapid Ohia Death cannot be shared publicly, however, the format of the data is roughly as seen below:

|Tree ID     | X_Coordinate |  Y_Coordinate       |  TimeStamp1
|------------|--------------|---------------------|-----------------
|1           |  2313.13     |  1278.90            |  4
|2           |  2452.45     |  1523.84            |  4
|3           |  2567.21     |  1442.54            |  2
|4           |  2242.05     |  1434.89            |  0

Tree_ID is an arbitrary number that identifies a particular tree, X_coordinate and Y_coordinate are the position of the tree and timestamp1 is the 'health' of a tree. 4 means the tree is healthy, 3 means that the tree is starting to yellow, 2 means the tree is starting to turn red (a clear sign of ROD, in this case) 1 means the tree has turned brown and is dying and 0 means the tree is a skeleton and is completely dead.

We had about 4000 total trees, with about 60 timestamps, what you see above is simply an example.

The basic idea here is we place a tree at its coordinate, and choose the appropriate 3D model of a tree to place (as indicated by its health) <br>

### Models

Now that we understand the format of the data this code uses, we need models to put into our 3D environment.  We created .fbx models in Blender with the tree sapling plugin and used those as our models.

![](/github/tree_example.JPG)

If you want to use more realistic models or any other model in .fbx format, that is fine. We chose "simple" models because it is very computationally demanding to make renders of 3D environments. Name the models as "0.fbx", "1.fbx", "2.fbx", "3.fbx" and "4.fbx" so that a model has the same name of the health of a tree. In order to add more variation to our forest, we had several folders with these 5 fbx files in them. These folders are named 1, 2 and 3. An example filepath to these models would be: "/blender/tree_models/3/4.fbx" denoting a tree of type 4 (Healthy) and variation 3.

When you have all your files set up, your blender folder should look like this:

```bash
├── blender
│   ├── background.exr
│   ├── ground.fbx
│   └── tree_models
│       ├── 1
│       │   ├── 0.fbx
│       │   ├── 1.fbx
│       │   ├── 2.fbx
│       │   ├── 3.fbx
│       │   └── 4.fbx
│       ├── 2
│       │   ├── 0.fbx
│       │   ├── 1.fbx
│       │   ├── 2.fbx
│       │   ├── 3.fbx
│       │   └── 4.fbx
│       ├── 3
│       │   ├── 0.fbx
│       │   ├── 1.fbx
│       │   ├── 2.fbx
│       │   ├── 3.fbx
│       │   └── 4.fbx
│       └── 4
│           ├── 0.fbx
│           ├── 1.fbx
│           ├── 2.fbx
│           ├── 3.fbx
│           └── 4.fbx
```

We also need a terrain to place our trees on, so we made another model in Blender that is just a plane. Again, we kept it simple due to the computational demands of this program.

### Config

At the top of the script, there's a config that allows you to tweak variables based on the type of visualization you want to make.

<ul>
    <li> MAX_ORD is the size of the x,y plane that the visualization will be generated on. </li>
    <li> CAMERA_HEIGHT is the height of the camera, pointed towards the origin. </li>
    <li> START is the timestamp that you want to start at (should be 0) </li>
    <li> STOP is the timestamp that you want to end at </li>
    <li> FRAMES_PER_STEP is the number of frames at a particular location </li>
    <li> NUM_TREE_VARIETIES would be the number of variations on the fbx tree models you've used </li>
</ul>

## Run the code

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

The bpy script will finish running and produce a set of images. To render the video, type:

```bash
python ./utils/render_video.py
```

The output video will be saved in:

```bash
/videos
```

The output should look something like this:

![3D Rod Spread Vizualization 3](/github/3d_rod_spread_1.gif)

# Acknowledgements

We would like to thank the instructors at the University of Hawaii at Hilo Computer Science and Art Departments for guidance in developing these software tools. We would also like give special thanks to Dr. Ryan Perroy, who generously guided us and gave feedback throughout the design, planning, and development stages.
