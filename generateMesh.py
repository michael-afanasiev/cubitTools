#! /usr/bin/python2.6

import os
import sys
import cubit

geomPath = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom/'
  
  
names = ['Japan', 'Europe', 'Australia']
sizes = ['50', '10', '85']
cubit.init ('.')
cubit.cmd  ('set journal off')
cubit.cmd  ('open "' + geomPath + 'cutters/all_cutters.cub')

for file in os.listdir ( geomPath ):
  
  if ( file == 'col000-090.lon090-180.rad6351-6371.000.cub' ):
  
    cubit.cmd ('import "' + geomPath + file + '"')    
    cubit.cmd ('compress all')
    numVolumes = cubit.get_volume_count ()
  
    volumeIds   = [x for x in range (numVolumes)]    
    overLapping = cubit.get_overlapping_volumes ( volumeIds )
    
    if overLapping:
      for i in range (0, len(overLapping) - 1, 2 ):
        if ( overLapping[i] > overLapping[i+1] ):          
          vol1 = str (overLapping[i])
          vol2 = str (overLapping[i+1])
        else:
          vol1 = str (overLapping[i+1])
          vol2 = str (overLapping[i])

        cubit.cmd ('intersect volume ' + vol1 + ' ' + vol2 + ' keep')           
        
    cubit.cmd ('compress all')
    
    for region in names:
            
      cubit.cmd ('subtract volume with name "' + region + 
        '_cutter" from volume with name "masters*"')
      
    cubit.cmd ('del vol with name "*_cutter')      
    cubit.cmd ('compress all')
    
    cubit.cmd ('vol all scheme tetmesh')  
    cubit.cmd ('surf all scheme trimesh')  
    cubit.cmd ('surf all sizing function constant')
    cubit.cmd ('surf all size 85')
    
    for region, size in zip (names, sizes):
      cubit.cmd ('surf in vol with name "' + region + '*" size ' + size )
    
    cubit.cmd ('mesh surf all')
    cubit.cmd ('mesh vol all')
    
    cubit.cmd ( 'set large exodus file on\n' )
        
    cubit.cmd ('export mesh "~/Desktop/test.ex2" overwrite')
    cubit.cmd ('save as "~/Desktop/test.cub" overwrite')          