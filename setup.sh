#!/bin/bash

# SETUP ENV
pip install gdown

# SETUP DIRS
mkdir blender
mkdir images
mkdir videos

# GET WEIGHTS
tree_models="16tGVyZICngIh8NyGJYmoX84JncA3tKW-"
gdown $BINARY_MODEL -O ./saved_weights/binary_model_default.zip
unzip ./saved_weights/binary_model_default.zip -d ./saved_weights/

# GET DATA
DATA="1ddl19yfm_2uv7_zoYC73SCEW_hB-4aAZ"
gdown $DATA -O ./data/Kauai_CRP.zip
unzip ./data/Kauai_CRP -d ./data/

echo "SETUP FINISHED"
