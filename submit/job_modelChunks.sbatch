#! /bin/bash

#SBATCH --partition=fichtner_compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=01:00:00
#SBATCH --mem=32GB
#SBATCH --exclusive
#SBATCH --job-name="generateBaseMesh.$1"
#SBATCH --output=output/addModelChunksToEarth.%j.o
#SBATCH --error=output/addModelChunksToEarth.%j.e

cd /users/afanasm/src/codeDevelopment/cubitTools

srun ./bin/addModelChunksToEarth.py -f /mnt/lnec/afanasm/cubitScratch/ 
