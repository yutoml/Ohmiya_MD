#!/bin/bash

#PBS -q regular-g
#PBS -l select=2:mpiprocs=1:ompthreads=72 
#PBS -W group_list=gw70
#PBS -l walltime=48:00:00
#PBS -N "water"
#PBS -j oe

source /work/gw70/w70003/.basic_settings_core

cd ${PBS_O_WORKDIR} 

exe_VASP 1> vasp.out 2> vasp.err
#python calc.py