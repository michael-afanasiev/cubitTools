#! /usr/bin/python2.6

import os
import sys
import cubit

if ( len (sys.argv) < 2 or sys.argv[1] == '-help' ):
  sys.exit ('Usage: ./setupMesh <-m|-g> [-o] \n-m generate mesh and geometry \
    \n-g only generate geometry \n[-o] overwrite mesh files')    
mode = sys.argv[1]

if ( len (sys.argv) > 2 ):
  overWrite = True
  print 'Warning :: Overwriting mesh files.'
  raw_input ('Press enter is this is ok.\n')
else:
  overWrite = False

path     = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/'
geomPath = '/Users/michaelafanasiev/Development/src/code/' \
  'comprehensive_earth_model/Exodus/scaleUp/geom/'
  
cubit.init ('.')

for file in os.listdir ( geomPath + 'masters/' ):
  
  fields      = file.split ('.')
  exoFileName = fields[0] + '.' + fields[1] + '.' + fields[2] + '.' \
    + fields[3] + '.ex2'    
    
  if ( mode == '-g' or not os.path.isfile (path + 'mesh/' + exoFileName) or 
    overWrite ):
  
    cubit.cmd  ('open "' + geomPath + 'cutters/all_cutters.cub')
  
    Japan         = False
    Europe        = False
    Anatolia      = False
    Australia     = False
    SouthAtlantic = False
  
    names = []
    sizes = []

    # Set up surface sizing functions.
    fields    = file.split ('.')
    radRegion = fields[2]
    if radRegion == 'rad0000-1221':
      params = { 'Europe': 100, 'Japan': 100, 'SouthAtlantic': 100, 
        'Australia': 100, 'Anatolia': 30 }
    if radRegion == 'rad1221-3480':                                     
      params = { 'Europe': 100, 'Japan': 100, 'SouthAtlantic': 100, 
        'Australia': 100, 'Anatolia': 30 }
    if radRegion == 'rad3480-5371':                                     
      params = { 'Europe': 100, 'Japan': 100, 'SouthAtlantic': 100, 
        'Australia': 100, 'Anatolia': 30 }
    if radRegion == 'rad5371-5701':                                     
      params = { 'Europe': 100, 'Japan': 100, 'SouthAtlantic': 100, 
        'Australia': 100, 'Anatolia': 30 }
    if radRegion == 'rad5701-5971':                                     
      params = { 'Europe': 50, 'Japan':  50, 'SouthAtlantic':  50, 
        'Australia': 50, 'Anatolia': 30  }
    if radRegion == '5971-6271':                                     
      params = { 'Europe': 50, 'Japan':  50, 'SouthAtlantic':  50, 
        'Australia': 50, 'Anatolia': 30  }
    if radRegion == 'rad6271-6319':                                     
      params = { 'Europe': 50, 'Japan':  50, 'SouthAtlantic':  50, 
        'Australia': 50, 'Anatolia': 30  }
    if radRegion == 'rad6319-6351':                                     
      params = { 'Europe': 50, 'Japan':  50, 'SouthAtlantic':  50, 
        'Australia': 50, 'Anatolia': 30  }
    if radRegion == 'rad6351-6371':                                     
      params = { 'Europe': 50, 'Japan':  50, 'SouthAtlantic':  50, 
        'Australia': 50, 'Anatolia': 30  }

    cubit.cmd ('import "' + geomPath + 'masters/' + file + '"')    
    cubit.cmd ('compress all')
    numVolumes = cubit.get_volume_count ()

    volumeIds   = [x for x in range (1, numVolumes+1)]    
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
        if cubit.get_entity_name ('volume', num).startswith ('Anatolia'):
          Anatolia = True
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
    if Anatolia:
      print 'Found Anatolia'
      names.append ('Anatolia')
      sizes.append (params['Anatolia'])
    if Europe:
      print 'Found Europe'
      names.append ('Europe')
      sizes.append (params['Europe'])      
    
    for region in names:
        
      cubit.cmd ('subtract volume with name "' + region + 
        '_cutter" from volume with name "masters*"')
  
    cubit.cmd ('del vol with name "*_cutter')          
  
    if ( cubit.get_volume_count() > 1 ):
      cubit.cmd ( 'imprint all' )
      cubit.cmd ( 'merge all' )   

    cubit.cmd ('compress all')    
      
    if names:
      for region, size in zip (names, sizes):
        cubit.cmd ('vol with name "' + region + '*" scheme tetmesh')
        cubit.cmd ('surf in vol with name "' + region + '*" size ' + 
          str (size) )        
        cubit.cmd ('surf in vol with name "' + region + '*" sizing function ' + 
          'constant' )
          
    cubit.cmd ('vol with name "masters*" scheme tetmesh')
    cubit.cmd ('surf in vol with name "masters*" size 100')                    
    cubit.cmd ('surf all sizing function constant')

    cubit.cmd ('save as "' + geomPath + 'regions/' + file + '" overwrite')  
  
    if ( mode == '-m' ):
      cubit.cmd ( 'mesh volume all' )
      cubit.cmd ( 'unite body all include_mesh' )
      cubit.cmd ( 'set large exodus file on' )
      cubit.cmd ( 'export mesh "' + path + 'mesh/' + exoFileName + 
        '" overwrite' )
  
    cubit.cmd ('reset')         

if cubit.get_error_count () != 0:
  print "Unfortunately, I found some errors"