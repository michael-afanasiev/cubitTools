#! /bin/bash

#SBATCH --partition=fichtner_compute
#SBATCH --nodes=1
#SBATCH --mincpus=10
#SBATCH --ntasks=1
#SBATCH --time=04:00:00
#SBATCH --job-name="refineMesh$1"
#SBATCH --output=output/refineMesh.%j.o
#SBATCH --error=output/refineMesh.%j.e

cd /users/afanasm/src/codeDevelopment/cubitTools/cubitTools

srun ./bin/refineRadialMesh.py -f /mnt/lnec/afanasm/cubitScratch/ -n $2 -r $1 
