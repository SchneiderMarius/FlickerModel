#!/bin/bash
# Add the conda environment you want to run your script in to the $PATH. Use
#   conda env list
# to see the full path of all your conda environments
PATH=/mnt/hpc/home/schneiderm/anaconda3/envs/Neuron-env/bin/:$PATH

# Execute the Python script and pass two arguments along
python PoissonSynWrapper2.py $1 $2 $3 $4 $5 $6 $7 $8 $9 $10