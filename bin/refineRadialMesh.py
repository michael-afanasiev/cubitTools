#! /usr/bin/python2.6

import os
import time
import sys
import cubit
 
if ( len (sys.argv) < 2 or sys.argv[1] == '--help' or sys.argv[1] == '-h' ):
  sys.exit ('Usage: ./refineRadialMesh.py -f -n -r \
    \n-f base write path (contains /mesh and /geom) \
    \n-n number of tets through thickness \
    \n-r rad region (e.g. rad6351-6371)' )


for i in range ( len (sys.argv) - 1 ):
  if sys.argv[i] == '-f':
    basePath = sys.argv[i+1]
  if sys.argv[i] == '-n':
    numThrough = str (sys.argv[i+1])
  if sys.argv[i] == '-r':
    reqRegion = sys.argv[i+1]

print 'Radial region: ' + reqRegion
print 'N_through: ' + numThrough

path     = basePath
geomPath = basePath + 'geom/'

time.sleep (2)
cubit.init ('.')

print 'Running'

for file in os.listdir ( geomPath + 'regions_meshed/' ):

  if file.startswith ('col000-090.lon000-090'):
  
    fields      = file.split ('.')
    radRegion   = fields[2]
    exoFileName = fields[0] + '.' + fields[1] + '.' + fields[2] + '.' \
      + fields[3] + '.ex2'

    if ( radRegion != reqRegion ):
      continue
    
    cubit.cmd  ('open "' + geomPath + 'regions_meshed/' + file + '"')
       
    surfs = [i for i in range (1, cubit.get_surface_count()+1)]
       
    targets = []
    for surf in surfs:
      if ( cubit.get_surface_type (surf) == 'sphere surface' ):
        targets.append (str ( surf ))
    
    for i in range (0, len(targets)-1, 2 ):
      refineString = 'Refine min_through_thickness ' + numThrough + ' source surface ' + \
        targets[i] + ' target surface ' + targets[i+1] + ' anisotropic'
     
      cubit.cmd ( refineString )

    cubit.cmd ( 'save as "' + geomPath + 'regions_refined/' + file + '" overwrite' )
    cubit.cmd ( 'export mesh "' + path + 'mesh/refined/' + exoFileName + 
      '" overwrite' )
 
 