#!/bin/bash

# SETUP ENV
pip install gdown

# SETUP DIRS
mkdir blender
mkdir images
mkdir videos

# GET WEIGHTS
tree_models="1rh880TADXrl3AlrLmePUK_4qG2G2Lzjb"
gdown $tree_models -O ./blender.zip
unzip ./blender.zip
rm ./blender.zip

# GET DATA
DATA="1EaM1nWAz5fdBYsX2Sgeb65wWETbQaegf"
gdown $DATA -O ./kapapala_tracking.csv

echo "SETUP FINISHED"
