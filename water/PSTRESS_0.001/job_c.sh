#!/bin/bash

#PBS -q short-c
#PBS -l select=1:mpiprocs=16:ompthreads=7 
#PBS -W group_list=gw70
#PBS -l walltime=48:00:00
#PBS -N "water"
#PBS -j oe

source /work/gw70/w70003/.basic_settings_core

cd ${PBS_O_WORKDIR} 

python calc.py