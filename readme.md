== cubitTools ==

This collection of tools allows the automatic generation of the mesh used by the comprehensive earth model.

To regenerate the mesh from scratch, follow these steps.

1.) Generate the geometry creation driver script [./drivers/generateGeomDriver.py]. This will ask you a series of questions about the
    mesh chunks you would like to create, and generate a driver script [./drivers/geomDriver.sh]. Currently, geomDriver.sh is meant
    to be run as an interactive job (salloc --nodes=1 --ntasks=1 --mem=32GB --partition=fichtner_compute --exclusive), but this can
    be easily changed. This is not very computationally intensive, and just creates a whole bunch of .cub geometry files that define
    the spherical slices in the model.

2.) Run the script addModelChunksToEarth [./bin/addModelChunksToEarth.py]. This one does not need a driver script, as it simply works for
    all this files contained in the geometry directory. What this does is take all the cutters you have defined, and cuts them out of the 
    spherical shells defined in step (1). Quite a cool script. It also sets the sizes of the regions. Currently, this is a bit tedious,
    as you have to edit the code and add entries to a sizing dictionary, but this can easily be outsourced to a parameter file.

3.) The next step is to mesh the model. The driver script [./drivers/generateBaseMeshDriver] will create a script that is used to submit the 
    meshing as a series of batch jobs (submitting the .sbatch submit/job_meshDriver.sbatch]. The script created will also be in './drivers' and will be called 'baseMeshDriver.sh'. 
    Right now the script is set up for the dimensions of the CEM. You can simply run it and it will create your submission script. Submit this, and voila! Your fully meshed CEM now exists.
