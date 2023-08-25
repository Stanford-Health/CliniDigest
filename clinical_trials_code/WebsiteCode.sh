#!/bin/bash

# fill in sbatch info

module purge

# TODO: add full path before WebsiteCode.py
srun python WebsiteCode.py
