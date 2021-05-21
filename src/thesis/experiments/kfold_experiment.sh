#!/bin/bash

#Experiment Parameters
GRID_RESOLUTION=10
K=10

#Clean Directories
#rm -f log/*.log
#rm -f data/samples/kfolds/*.csv
rm -f data/technique_data/*/*.csv

#Executes the programs
#python normalizer_generator.py
python square_grid_generator.py $GRID_RESOLUTION
python kfold.py -k $K -r $GRID_RESOLUTION

#Notify phone about the script completion
telegram_sendmessage.sh "Your K-Fold experiment (K=$K, RES=$GRID_RESOLUTION) has finished."

#Send log file to telegram
LOG_FILE=log/$(ls log -1 | tail -n 1)
telegram_sendfile.sh $LOG_FILE