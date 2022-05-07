# Introduction

In Hawaii's forests, Ohia trees are one of the ecologically important species in native Hawaiian Forests. A new pathogen known as Rapid Ohia Death (ROD) is a newly identified fungus that threatens native forests. Creating a visualization of the spread of Rapid Ohia Death is critical to communicating the danger this pathogen presents to Hawaii's forests. This software is a tool that helps us show the spread of Rapid Ohia Death. If you have the right data and the computing power, you could use this software to visualize any forest.<br>

We use [Blender](https://www.blender.org/download/) as our 3D modeling software and [Python](https://www.python.org/downloads/) to generate tree models and render images of our virtual forest. The data was provided to us by Dr. Ryan Perroy, a researcher on the spread of Rapid Ohia Death. The models that we used are in .fbx format, and we made in Blender using the Tree Sapling Plugin. 

The code was written by [Mark Jimenez](https://github.com/kerneltrick), [Ryp Ring](https://github.com/rypring) and Carina Shintaku

<br>

# How to use this code

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

Now that we understand the format of the data this code uses, we need models to put into our 3D environment.  We created .fbx models in Blender with the tree sapling plugin and used those as our models. 

If you want to use more realistic models or any other model in .fbx format, that is fine. We chose "simple" models because it is very computationally demanding to make renders of 3D environments. Name the models as "0.fbx", "1.fbx", "2.fbx", "3.fbx" and "4.fbx" so that a model has the same name of the health of a tree. In order to add more variation to our forest, we had several folders with these 5 fbx files in them. These folders are named 1, 2 and 3. An example filepath to these models would be: "./3/4.fbx" denoting a tree of type 4 variation 3.

<br>

# Visualizing Rapid Ohia Death Spread

![2D Rod Spread Vizualization](/githyb/rod_spread_2d.gif)

 
  

