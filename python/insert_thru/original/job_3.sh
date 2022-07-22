#!/bin/bash

# Set some environment variables 
FREE_ENERGY=$(pwd)
MDP=$FREE_ENERGY/MDP
LAMBDA=3

mkdir Lambda_$LAMBDA
cd Lambda_$LAMBDA

# ENERGY MINIMIZATION 1: STEEP  

mkdir EM 
cd EM

gmx grompp -f $MDP/min_$LAMBDA.mdp -c $FREE_ENERGY/Lambda_$((LAMBDA-1))/PROD/prod$((LAMBDA-1)).gro -r $FREE_ENERGY/centered.gro -p $FREE_ENERGY/topol.top -n $FREE_ENERGY/index.ndx -o min_$LAMBDA.tpr
gmx mdrun -nt 4 -deffnm min_$LAMBDA 
sleep 2

# NVT EQUILIBRATION 

cd ../
mkdir NVT
cd NVT

gmx grompp -f $MDP/nvt_$LAMBDA.mdp -c ../EM/min_$LAMBDA.gro -r $FREE_ENERGY/centered.gro -p $FREE_ENERGY/topol.top -n $FREE_ENERGY/index.ndx -o nvt$LAMBDA.tpr
gmx mdrun -ntmpi 1 -ntomp 4 -deffnm nvt$LAMBDA 
sleep 2

# NPT EQUILIBRATION

cd ../
mkdir NPT
cd NPT

gmx grompp -f $MDP/npt_$LAMBDA.mdp -c ../NVT/nvt$LAMBDA.gro -r $FREE_ENERGY/centered.gro -p $FREE_ENERGY/topol.top -n $FREE_ENERGY/index.ndx -t ../NVT/nvt$LAMBDA.cpt -o npt$LAMBDA.tpr
gmx mdrun -ntmpi 1 -ntomp 4 -deffnm npt$LAMBDA 
sleep 2

# PRODUCTION MD 

cd ../
mkdir PROD
cd PROD

gmx grompp -f $MDP/prod_$LAMBDA.mdp -c ../NPT/npt$LAMBDA.gro -r $FREE_ENERGY/centered.gro -p $FREE_ENERGY/topol.top -n $FREE_ENERGY/index.ndx -t ../NPT/npt$LAMBDA.cpt -o prod$LAMBDA.tpr
gmx mdrun -ntmpi 1 -ntomp 4 -deffnm prod$LAMBDA 
sleep 2


