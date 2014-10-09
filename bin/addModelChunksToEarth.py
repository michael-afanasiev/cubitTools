#! /usr/bin/python2.6

import os
import sys
import cubit
import fileinput

def readParameters ():

  """ Just a little function to read in parameter names and surface sizing functions from a parameter file
  called regions.txt. Lines with comments are ignored, and a dictionary of region names and sizes is 
  returned. """

  params = {}

  for line in fileinput.input ('./regions.txt'):
    
    if line.startswith ('#') or not line.strip ():
      continue

    fields = line.split ('=')
    name, size = fields[0].strip (), float (fields[1])
    params.update ({name: size})

  return params

# Read parameter file.
params = readParameters ()

# User specifies where the read directories are.
if ( len (sys.argv) < 2 or sys.argv[1] == '--help' or sys.argv[1] == '-h' ):
  sys.exit ('Usage: ./addModelChunksToEarth.py -f \n-f base write path (contains /mesh and /geom)')    

# Read in command line options.
for i in range (len (sys.argv) - 1 ):
  if sys.argv[i] == '-f':
    basePath = sys.argv[i+1]

# Code looks for a /geom directory to find the earth chunk files (generated in previous step).
path     = basePath
geomPath = basePath + 'geom/'
  
# Initialize cubit.
cubit.init ('.')

# Here we loop through all the files in the master earth chunk directory
for file in os.listdir ( geomPath + 'masters/' ):
  

  fields      = file.split ('.')
  
  cubit.silent_cmd  ('open "' + geomPath + 'cutters/all_cutters.cub')

  paramBool = params.copy ()
  for key in paramBool.keys ():
    paramBool[key] = False

  names = []
  sizes = []

  # Set up surface sizing functions.
  fields    = file.split ('.')
  radRegion = fields[2]

  cubit.silent_cmd ('import "' + geomPath + 'masters/' + file + '"')    
  cubit.silent_cmd ('compress all')
  numVolumes = cubit.get_volume_count ()

  volumeIds   = [x for x in range (1, numVolumes+1)]    
  overLapping = cubit.get_overlapping_volumes ( volumeIds )

  if overLapping:
    for i in range (0, len(overLapping) - 1, 2 ):
      if ( overLapping[i] > overLapping[i+1] ):          
        vol1 = str (overLapping[i])
        vol2 = str (overLapping[i+1])
      else:
        vol1 = str (overLapping[i+1])
        vol2 = str (overLapping[i])

      cubit.silent_cmd ('intersect volume ' + vol1 + ' ' + vol2 + ' keep')           
  
  cubit.silent_cmd ('compress all')

  
  numVolumes  = cubit.get_volume_count ()
  volumeIds   = [x for x in range (1, numVolumes+1)]    
  overLapping = cubit.get_overlapping_volumes ( volumeIds )
  if overLapping:
    for num in overLapping:
      for key in paramBool.keys ():
        if cubit.get_entity_name ('volume', num).startswith (key) and key not in names:
          names.append (key)
          sizes.append (params[key])
     
  # for all named regions, subtract them from the master earth.
  for region in names:
      
    cubit.silent_cmd ('subtract volume with name "' + region + 
      '_cutter" from volume with name "masters*"')

  # delete all the cutters when we're finished with them
  cubit.silent_cmd ('del vol with name "*_cutter')       

  # compress namespace.
  cubit.silent_cmd ( 'compress all' )    
    
  # set the sizing functions of the master earth.
  cubit.silent_cmd ('vol with name "masters*" scheme tetmesh')
  cubit.silent_cmd ('surf in vol with name "masters*" size 100')                    
  cubit.silent_cmd ('curve in vol with name "masters*" size 100')

  # go and apply the sizing functions to the proper volumes.
  if names:
    for region, size in zip (names, sizes):
      cubit.silent_cmd ('vol with name "' + region + '*" scheme tetmesh')
      cubit.silent_cmd ('surf in vol with name "' + region + '*" size ' + 
        str (size) )
      cubit.silent_cmd ('curve in vol with name "' + region + '*" size ' +
        str (size) )        
 
  # name element blocks for master earth...
  blockCount = 1
  cubit.silent_cmd ('block ' + str (blockCount) + ' volume with name "masters*"')
  cubit.silent_cmd ('block ' + str (blockCount) + ' name "master"')
 
  # and nodesets...
  cubit.silent_cmd ('Nodeset ' + str (blockCount) + ' volume with name "masters*"')
  cubit.silent_cmd ('Nodeset ' + str (blockCount) + ' name "master"')

  # now go through and group the rest of the regions into blocks and nodesets
  blockCount = 2
  for region in names:

    cubit.silent_cmd ('block ' + str (blockCount) + ' volume with name "' + region + '*"')
    cubit.silent_cmd ('block ' + str (blockCount) + ' name "' + region + '"')

    cubit.silent_cmd ('Nodeset ' + str (blockCount) + ' volume with name "' + region + '*"')
    cubit.silent_cmd ('Nodeset ' + str (blockCount) + ' name "' + region + '"')

    blockCount = blockCount + 1


  # Get some badass sidesets
  cubit.cmd ( 'Sideset 1 surface in volume all with not is_merged' )

  # write and reset for next file.
  cubit.silent_cmd ('save as "' + geomPath + 'regions/' + file + '" overwrite')  
  cubit.silent_cmd ('reset')         

if cubit.get_error_count () != 0:
  print "Unfortunately, I found some errors"
