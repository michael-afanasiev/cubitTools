#! /usr/bin/python2.6

import os
import sys
import cubit

unMeshed = True

if ( len(sys.argv) < 5 or sys.argv[1] == '--help' or sys.argv[1] == '-h' ):
  print 'Usage: ./generateBaseMesh -f \n-f base write path (contains /mesh and /geom) \n-p prefix'
  sys.exit()

for i in range (len (sys.argv) - 1 ):
  if (sys.argv[i] == '-f'):
    basePath = sys.argv[i+1]
  if (sys.argv[i] == '-p'):
    prefix = sys.argv[i+1]

path     = basePath
geomPath = basePath + 'geom/'

cubit.init ('.')

for file in os.listdir ( geomPath + 'regions/' ):

  if file.endswith ('.jou'):
    continue

  if file.startswith (prefix):
    pass
  else:
    continue

  fields      = file.split ('.')
  exoFileName = fields[0] + '.' + fields[1] + '.' + fields[2] + '.' \
    + fields[3] + '.ex2'
    
  cubit.cmd  ('open "' + geomPath + 'regions/' + file + '"')    
    
  
  while unMeshed:
  
    cubit.cmd ('mesh vol all')
    unMeshed    = False
    badVols     = []
    numVolumes  = cubit.get_volume_count ()
    numSurfaces = cubit.get_surface_count ()
    surfIds     = [x for x in range (1, numSurfaces+1)]
    volIds      = [x for x in range (1, numVolumes+1)]
    for vol in volIds:
        if ( cubit.is_meshed ("volume", vol) ):
          pass
        else:
          badVols.append (vol)
          print "Volume " + str (vol) + " could not mesh. Attempting to reduce mesh size."
          unMeshed = True

    if unMeshed:
        cubit.cmd ('del mesh')

    for surf in surfIds:
      if cubit.get_owning_volume ('surface', surf) in badVols:
          reqSize = cubit.get_requested_mesh_size ( 'surface', surf)
          print "Requested size of surface " + str(surf) + " " + str (reqSize) + "\n"
          cubit.cmd ('surf ' + str (surf) + ' size ' + str (reqSize - 1) )
          print "New requested size of surface " + str ( cubit.get_requested_mesh_size ( 'surface', surf ) )

  unMeshed = True
#  cubit.cmd ('unite body all include_mesh')
  cubit.cmd ('set large exodus file on')
  cubit.cmd ('save as "' + geomPath + 'regions_meshed/' + file + '" overwrite')  
  cubit.cmd ( 'export mesh "' + path + 'mesh/base/' + exoFileName + 
    '" overwrite' )
  cubit.cmd ('reset')
