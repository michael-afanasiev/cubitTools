#! /usr/bin/python2.6

import os
import sys
import cubit

# Initialize
unMeshed  = True
firstTime = True

# Get command line options.
if ( len(sys.argv) < 9 or sys.argv[1] == '--help' or sys.argv[1] == '-h' ):
  print 'Usage: ./generateBaseMesh -f \n-f base write path (contains /mesh and /geom) \n-p prefix \n-b bottom radius \n-t top radius'
  sys.exit()

for i in range (len (sys.argv) - 1):
  if (sys.argv[i] == '-f'):
    basePath = sys.argv[i+1]
  if (sys.argv[i] == '-p'):
    prefix = sys.argv[i+1]
  if (sys.argv[i] == '-b'):
    bottomRadius = int (sys.argv[i+1])
  if (sys.argv[i] == '-t'):
    topRadius = int (sys.argv[i+1])

path     = basePath
geomPath = basePath + 'geom/'

cubit.init ('.')

for file in os.listdir ( geomPath + 'regions/' ):

  # Only interested in files which come with the designated prefix.
  if file.startswith (prefix):
    pass
  else:
    continue

  # Split filename.
  fields      = file.split ('.')
  exoFileName = fields[0] + '.' + fields[1] + '.' + fields[2] + '.' \
    + fields[3] + '.ex2'
  newExoFileName = fields[0] + '.' + fields[1] + '.rad' + str (bottomRadius) + '-' \
    + str (topRadius) + '.' + fields[3] + '.ex2'
  newCubFileName = fields[0] + '.' + fields[1] + '.rad' + str (bottomRadius) + '-' \
    + str (topRadius) + '.' + fields[3] + '.cub'
    
  
  # Split radius part of filename to determine which chunks to merge.
  rads   = fields[2].split ('-')
  botRad = rads[0]
  botRad = int ( botRad[3::] )
  topRad = int ( rads[1] )

  # Merge all chunks that are between some radius values.
  if ( botRad >= bottomRadius and topRad <= topRadius ):
    if firstTime:
      cubit.cmd  ('open "' + geomPath + 'regions/' + file + '"')
      firstTime = False
    else:
      cubit.cmd ( 'import "' + geomPath + 'regions/' + file + '"' ) 

# This is a counter on how many times we have to go back and retry the sizing.
unMeshedTries = 0

cubit.cmd ( 'surf all sizing function constant' )

# UnMeshed gets set to false if any of the volumes fail to mesh the first time through.
while unMeshed:

  # Imprint and merge all the cute litte regions.
  cubit.cmd ( 'imprint vol all' )
  cubit.cmd ( 'merge vol all' )

  # Mesh surfaces first (this seems to be safer for some reason).
  cubit.cmd ( 'mesh surf all' )

  # Remind Cubit that yes we want a tetmesh.
  cubit.cmd ( 'vol all scheme tetmesh' )

  # Finish meshing.
  cubit.cmd ( 'mesh vol all' )

  # Set up a couple checks here to see if the mesh is sane. 
  unMeshed    = False
  badVols     = []
  numVolumes  = cubit.get_volume_count ()
  numSurfaces = cubit.get_surface_count ()
  surfIds     = [x for x in range (1, numSurfaces+1)]
  volIds      = [x for x in range (1, numVolumes+1)]

  # Go through all volumes to ensure that they're meshed.
  for vol in volIds:
    if ( cubit.is_meshed ("volume", vol) ):
      pass
    else:
      badVols.append (vol)
      print "Volume " + str (vol) + " could not mesh. Attempting to reduce mesh size."
      unMeshed = True
 
  # If some surfaces go unmeshed (I've seen this happen), go back through and try to adjust the size
  # If this happens more than 5 times, something is messed up, so let's quit.
  if unMeshed:
    cubit.cmd ('del mesh')
    unMeshedTries = unMeshedTries + 1

    if ( unMeshedTries == 6 ):
      sys.exit ( "Something is wrong with the meshing, I've tried 5 times and I can't get this to work. __QUITTING__" )
    
    # Decrease the surface size by 1 each time (in practice, this seems to do the trick).
    for surf in surfIds:
      if cubit.get_owning_volume ('surface', surf) in badVols:
        reqSize = cubit.get_requested_mesh_size ( 'surface', surf)
        print "Requested size of surface " + str(surf) + " " + str (reqSize) + "\n"
        cubit.cmd ('surf ' + str (surf) + ' size ' + str (reqSize - 1) )
        print "New requested size of surface " + str ( cubit.get_requested_mesh_size ( 'surface', surf ) )
       

# Smooth mesh (probably just for kicks).
cubit.cmd ( 'Volume all Smooth Scheme Laplacian' )
cubit.cmd ( 'Smooth Volume all' )

# Get some badass sidesets
cubit.cmd ( 'Nodeset 1 surface in volume all with not is_merged' )

# Write to exodus file.
cubit.cmd ('set large exodus file on')

# Save to cubit file as well.
cubit.cmd ('save as "' + geomPath + 'regions_meshed/' + newCubFileName + \
  '" overwrite')  
cubit.cmd ( 'export mesh "' + path + 'mesh/base/' + newExoFileName + \
  '" overwrite' )

# Clear everything and quit.
cubit.cmd ( 'reset' )
cubit.cmd ( 'quit' )
