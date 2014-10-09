#! /bin/bash

#SBATCH --partition=fichtner_compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:30:00
#SBATCH --mem=2GB
#SBATCH --job-name="generateBaseMesh.$1"
#SBATCH --output=output/generateBaseMesh.%j.o
#SBATCH --error=output/generateBaseMesh.%j.e

cd /users/afanasm/src/codeDevelopment/cubitTools

srun ./bin/generateBaseMesh.py -f /mnt/lnec/afanasm/cubitScratch/ -p $1 -t $2 -b $3
