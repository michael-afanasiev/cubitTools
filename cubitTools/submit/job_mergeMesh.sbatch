#! /bin/bash

#SBATCH --partition=fichtner_compute
#SBATCH --nodes=1
#SBATCH --mincpus=20
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --job-name="mergeMesh$1"
#SBATCH --output=output/mergeMesh.%j.o
#SBATCH --error=output/mergeMesh.%j.e

module load netcdf/4.3.1-intel

cd /users/afanasm/src/codeDevelopment/cubitTools/cubitTools

echo $1

srun $1
