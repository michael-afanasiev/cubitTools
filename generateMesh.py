#! /usr/bin/python2.6

import os
import sys
import cubit

path     = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/'
geomPath = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom/'
  
cubit.init ('.')
cubit.cmd  ('set journal off')

for file in os.listdir ( geomPath + 'regions/' ):
  
  fields = file.split ('.')
  exoFileName = fields[0] + '.' + fields[1] + '.' + fields[2] + '.' \
    + fields[3] + '.ex2' 
  
  cubit.cmd ( 'open "' + geomPath + 'regions/' + file + '"' )
  
  numVols = cubit.get_volume_count ()
  if numVols > 1:
    cubit.cmd ( 'imprint volume all' )
    cubit.cmd ( 'merge volume all' )
    
  cubit.cmd ( 'compress all' )
  cubit.cmd ( 'mesh surface all' )
  cubit.cmd ( 'mesh volume all' )
  
  cubit.cmd ( 'set large exodus file on' )
  cubit.cmd ( 'export mesh "' + path + 'mesh/' + exoFileName + '" overwrite' )
  cubit.cmd ( 'reset' )