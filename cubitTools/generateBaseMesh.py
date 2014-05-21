#! /usr/bin/python2.6

import os
import sys
import cubit

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
    print "SKIPPED"
    continue

  fields      = file.split ('.')
  exoFileName = fields[0] + '.' + fields[1] + '.' + fields[2] + '.' \
    + fields[3] + '.ex2'
    
  cubit.cmd  ('open "' + geomPath + 'regions/' + file + '"')    
    
  cubit.cmd ('mesh volume all')
#  cubit.cmd ('unite body all include_mesh')
  cubit.cmd ('set large exodus file on')
  cubit.cmd ('save as "' + geomPath + 'regions_meshed/' + file + '" overwrite')  
  cubit.cmd ( 'export mesh "' + path + 'mesh/base/' + exoFileName + 
    '" overwrite' )
  cubit.cmd ('reset')
