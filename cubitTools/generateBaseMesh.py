#! /usr/bin/python2.6

import os
import sys
import cubit

if ( len(sys.argv) < 2 ):
  print 'Usage: ./generateBaseMesh base write path (contains /mesh and /geom)'
  sys.exit()

basePath = sys.argv[1]

path     = basePath
geomPath = basePath + 'geom/'

cubit.init ('.')

for file in os.listdir ( geomPath + 'regions/' ):

  if file == 'cubit01.jou':
    continue

  fields      = file.split ('.')
  exoFileName = fields[0] + '.' + fields[1] + '.' + fields[2] + '.' \
    + fields[3] + '.ex2'
    
  cubit.cmd  ('open "' + geomPath + 'regions/' + file + '"')    
    
  cubit.cmd ('mesh volume all')
  cubit.cmd ('unite body all include_mesh')
  cubit.cmd ('set large exodus file on')
  cubit.cmd ('save as "' + geomPath + 'regions_meshed/' + file + '" overwrite')  
  cubit.cmd ( 'export mesh "' + path + 'mesh/base/' + exoFileName + 
    '" overwrite' )
  cubit.cmd ('reset')
