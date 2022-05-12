#!/bin/bash
## The first line (above) specifies the shell to use for parsing the
## remaining lines of the batch script.

## Required PBS Directives --------------------------------------
#PBS -A ONRDC37792433
##PBS -q standard
##PBS -q high
##PBS -q debug 
#PBS -q background 
#PBS -l select=1:ncpus=32:mpiprocs=32
#PBS -l walltime=4:00:00

## Optional PBS Directives --------------------------------------
##PBS -N zeng_test_ut1
##PBS -j oe
#PBS -S /bin/bash
#PBS -m be
##PBS -M zyd15549885598@gmail.com

## Execution Block ----------------------------------------------
# Environment Setup
# cd to your personal directory in the scratch file system

cd ${PBS_O_WORKDIR}

cp fort.11.second fort.11

## Launching ----------------------------------------------------

#aprun -n 32 ./fst > log.post.first 2>&1 
#aprun -n 32 ./fst > log.post.second 2>&1 
aprun -n 32 ./fst > log.post.third 2>&1 
# Submit next job
#qsub submit
