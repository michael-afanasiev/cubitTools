#! /bin/bash

#SBATCH --partition=fichtner_compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=04:00:00
#SBATCH --job-name="generateBaseMesh.$1"
#SBATCH --output=output/generateBaseMesh.%j.o
#SBATCH --error=output/generateBaseMesh.%j.e

cd /users/afanasm/src/codeDevelopment/cubitTools/cubitTools

if [ "$1" == "" ]; then echo "You forgot to specify prefix."; scancel %j; stop; fi

srun ./bin/generateBaseMesh.py -f /mnt/lnec/afanasm/cubitScratch/ -p $1
