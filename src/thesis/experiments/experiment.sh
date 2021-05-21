#!/bin/bash

#Experiment Parameters
GRID_RESOLUTION=50
TRAINING_SLICE=0.75
TEST_SLICE=0.25
GRID_POINTS_FILENAME="data/grid_points/squaremap_"$GRID_RESOLUTION"m.json"

#Clean Directories
rm -f log/*.log
rm -f data/technique_data/*/*.csv

#Executes the programs
python normalizer_generator.py
python square_grid_generator.py $GRID_RESOLUTION
python split_data.py $TRAINING_SLICE $TEST_SLICE
python train_techniques.py $GRID_POINTS_FILENAME
python test_techniques.py $GRID_POINTS_FILENAME

echo 'Done'