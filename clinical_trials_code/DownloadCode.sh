#!/bin/bash

# fill in sbatch info

module purge

# Download data
cd $TMPDIR
srun curl -L -o AllPublicXML.zip https://clinicaltrials.gov/AllPublicXML.zip

# Unzip data
mkdir inputs
cd inputs
srun unzip ../AllPublicXML.zip

# TODO: add full path before MainCode.py
srun python DownloadCode.py
