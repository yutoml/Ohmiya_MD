#!/bin/bash

#PBS -q debug-c
#PBS -l select=1:mpiprocs=16:ompthreads=7 
#PBS -W group_list=gw70
##PBS -l walltime=8:00:00
#PBS -N "exe_vasp"
#PBS -j oe

source /work/gw70/w70003/.basic_settings_core

cd ${PBS_O_WORKDIR} 

exe_VASP 1> vasp.out 2> vasp.err
#python calc.py