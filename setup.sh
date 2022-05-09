#!/bin/bash

# SETUP ENV
pip install gdown

# SETUP DIRS
mkdir images
mkdir images/2d
mkdir images/3d
mkdir videos

# GET WEIGHTS
tree_models="10tWYEYthPRpV89Qml3t1H7HHRishK0GX"
gdown $tree_models -O ./blender.zip
unzip ./blender.zip
rm ./blender.zip

# GET DATA
#DATA="1EaM1nWAz5fdBYsX2Sgeb65wWETbQaegf"
#gdown $DATA -O ./kapapala_tracking.csv

echo "SETUP FINISHED"
