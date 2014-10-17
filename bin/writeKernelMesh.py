#!/usr/bin/env python

import os
import sys
import cubit
import argparse
import element_selection as es

def saveTmpFile ():
  
  cubit.cmd ('save as "tmp.cub" overwrite')
  
def openTmpFile ():
  
  cubit.cmd ('open "tmp.cub"')

def removeTmpFile ():
  
  os.remove ("./tmp.cub")
  
def openCubitFile (fileName):
  
  cubit.cmd ('open "' + fileName + '"')
  
def importCubitFile (fileName):

  cubit.cmd ('import "' + fileName + '"')
  

def getAllVolumeIds ():

  cubit.cmd ('compress all')
  numVolumes = cubit.get_volume_count ()
  volumeIds  = [x for x in range (1, numVolumes+1)]
  
  return volumeIds
  
if (len (sys.argv) < 2 or sys.argv[1] == '--help' or sys.argv[1] == '-h'):
  sys.exit ('''
  Usage: ./writeKernelMesh -c -m -k
  -c [model volume outline]
  -m [master mesh directory]
  -k [kernel mesh write directory]
  ''')
  
cubit.init ('.')

for i in range (len (sys.argv)):
  
  if sys.argv[i] == '-c':
    modelCutterPath = sys.argv[i+1]

  if sys.argv[i] == '-m':
    meshPath = sys.argv[i+1]

  if sys.argv[i] == '-k':
    kernelWritePath = sys.argv[i+1]
    
for file in os.listdir (meshPath):
  
  if (not file.endswith ('.cub')):
    continue
    
  # Open the mesh file, and compress id space.
  openCubitFile (meshPath + '/' + file)
  cubit.cmd     ('compress all')
  
  # Import the cutter  
  importCubitFile (modelCutterPath)
  
  # Get all volume ids
  volumeIds = getAllVolumeIds ()
  
  # Get cutter vol id.
  volIdCutter = max (volumeIds)
  
  # Get overlapping volumes.
  searchVolumes = []
  for id in volumeIds:
    overLapping = cubit.get_overlapping_volumes ([id, volIdCutter])
    for vol in overLapping:
      if vol != volIdCutter:
        searchVolumes.append (vol)
  
  # Report
  print "Found " + str (len (searchVolumes)) + " intersecting volumes."

  # Find overlapping ids.
  overlap_tets = []

  # Save to temp file.
  saveTmpFile ()
  
  for id in searchVolumes:
    
    openTmpFile ()
    print "Finding tets in volume: " + str (id),
    tet_list = cubit.get_volume_tets (id)
    temp = es.getTetsOverlapPassedVols (tet_list, [volIdCutter])
    overlap_tets.extend (temp)


  removeTmpFile ()
  cubit.silent_cmd ('set duplicate block elements on')
  cubit.silent_cmd ('block 100 tet ' + es.toStr (overlap_tets))
  cubit.silent_cmd ('block 100 name "kernel"')
  
  cubit.silent_cmd ('set large exodus file on')
  cubit.silent_cmd ('export mesh "' + kernelWritePath + '/kernelMesh.ex2" block 100 overwrite')