#! /usr/bin/python2.6

import os
import sys
import cubit

path     = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/'
geomPath = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom/'
  
cubit.init ('.')

for file in os.listdir ( geomPath + 'regions/' ):

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