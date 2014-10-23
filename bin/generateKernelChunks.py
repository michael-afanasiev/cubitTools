#!/usr/bin/env python

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

# User specifies where the read directories are.
if ( len (sys.argv) < 4 or sys.argv[1] == '--help' or sys.argv[1] == '-h' ):
  sys.exit ('Usage: ./addModelChunksToEarth.py -f \n-f master_path \n-k kernel_path \n-s save_path')    

# Read in command line options.
for i in range (len (sys.argv) - 1 ):
  if sys.argv[i] == '-f':
    masterPath = sys.argv[i+1]
  if sys.argv[i] == '-k':
    kernelPath = sys.argv[i+1]
  if sys.argv[i] == '-s':
      savePath = sys.argv[i+1]

# Initialize cubit.
cubit.init ('.')

# Here we loop through all the files in the master earth chunk directory
for file in os.listdir (masterPath):
  
  fields      = file.split ('.')
  
  cubit.cmd  ('open "' + masterPath + '/' + file + '"')

  cubit.cmd ('import "' + kernelPath + "'")    
  cubit.cmd ('compress all')
  numVolumes = cubit.get_volume_count ()

  volumeIds   = [x for x in range (1, numVolumes+1)]    
  overLapping = cubit.get_overlapping_volumes ( volumeIds )

  if not overLapping:
    continue

  cubit.cmd ('intersect volume all')           
  cubit.cmd ('compress all')
  cubit.cmd ('surf all scheme trimesh')
  cubit.cmd ('vol all scheme tetmesh')
  cubit.cmd ('surf all size 50')
  cubit.cmd ('surf all sizing function constant')

  # write and reset for next file.
  cubit.cmd ('save as "' + savePath + file + '" overwrite')  
  cubit.cmd ('reset')         

if cubit.get_error_count () != 0:
  print "Unfortunately, I found some errors"
