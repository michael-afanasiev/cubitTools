#! /usr/bin/python2.6

import os
import sys
import cubit

geomPath = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom/'
  
cubit.init ('.')
cubit.cmd  ('set journal off')
for file in os.listdir ( geomPath + 'masters/' ):
  
  cubit.cmd  ('open "' + geomPath + 'cutters/all_cutters.cub')
  
  Japan         = False
  Europe        = False
  Australia     = False
  SouthAtlantic = False
  
  names = []
  sizes = []

  # Set up surface sizing functions.
  fields    = file.split ('.')
  radRegion = fields[2]
  if radRegion == 'rad0000-1221':
    params = { 'Europe': 85, 'Japan':  55, 'SouthAtlantic': 100, 
      'Australia': 100 }
  if radRegion == 'rad1221-3480':                                     
    params = { 'Europe': 85, 'Japan':  55, 'SouthAtlantic': 100, 
      'Australia': 100 }
  if radRegion == 'rad3480-5371':                                     
    params = { 'Europe': 100, 'Japan': 55, 'SouthAtlantic': 100, 
      'Australia': 100 }
  if radRegion == 'rad5371-5701':                                     
    params = { 'Europe': 100, 'Japan': 55, 'SouthAtlantic': 100, 
      'Australia': 100 }
  if radRegion == 'rad5701-5971':                                     
    params = { 'Europe': 55, 'Japan':  55, 'SouthAtlantic': 100, 
      'Australia': 100 }
  if radRegion == 'rad5971-6271':                                     
    params = { 'Europe': 28, 'Japan':  55, 'SouthAtlantic': 100, 
      'Australia': 100 }
  if radRegion == 'rad6271-6319':                                     
    params = { 'Europe': 28, 'Japan':  55, 'SouthAtlantic': 100, 
      'Australia': 100 }
  if radRegion == 'rad6319-6351':                                     
    params = { 'Europe': 10, 'Japan':  55, 'SouthAtlantic': 100, 
      'Australia': 100 }
  if radRegion == 'rad6351-6371':                                     
    params = { 'Europe': 10, 'Japan':  55, 'SouthAtlantic': 100, 
      'Australia': 100 }

  cubit.cmd ('import "' + geomPath + 'masters/' + file + '"')    
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

  numVolumes  = cubit.get_volume_count ()
  volumeIds   = [x for x in range (numVolumes)]    
  overLapping = cubit.get_overlapping_volumes ( volumeIds )
  if overLapping:
    for num in overLapping:
      if cubit.get_entity_name ('volume', num).startswith ('SouthAtlantic'):
        SouthAtlantic = True
      if cubit.get_entity_name ('volume', num).startswith ('Australia'):
        Australia = True
      if cubit.get_entity_name ('volume', num).startswith ('Europe'):
        Europe = True
      if cubit.get_entity_name ('volume', num).startswith ('Japan'):
        Japan = True
        
  if Japan:
    print 'Found Japan'
    names.append ('Japan')
    sizes.append (params['Japan'])          
  if SouthAtlantic:
    print 'Found SouthAtlantic'
    names.append ('SouthAtlantic')
    sizes.append (params['SouthAtlantic'])
  if Australia:
    print 'Found Australia'
    names.append ('Australia')
    sizes.append (params['Australia'])
  if Europe:
    print 'Found Europe'
    names.append ('Europe')
    sizes.append (params['Europe'])      
    
  for region in names:
        
    cubit.cmd ('subtract volume with name "' + region + 
      '_cutter" from volume with name "masters*"')
  
  cubit.cmd ('del vol with name "*_cutter')      
  cubit.cmd ('compress all')

  cubit.cmd ('vol all scheme tetmesh')  
  cubit.cmd ('surf all scheme trimesh')  
  cubit.cmd ('surf all sizing function constant')
  cubit.cmd ('surf all size 100')

  if names:
    for region, size in zip (names, sizes):
      cubit.cmd ('surf in vol with name "' + region + '*" size ' + 
        str (size) )

  cubit.cmd ('save as "' + geomPath + 'regions/' + file + '" overwrite') 
  cubit.cmd ('reset')         

if cubit.get_error_count () != 0:
  print "Unfortunately, I found some errors"