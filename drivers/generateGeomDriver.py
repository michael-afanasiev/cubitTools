#! /usr/bin/python

f = open ('./drivers/geomDriver.sh', 'w')

switch = 'alive'

while switch != 'exit':

  top  = input ('Enter top: ')
  bot  = input ('Enter bottom: ')
  disc = input ('Enter discretization: ')
  size = input ('Input chunk size: ')

  for i in range (bot, top, size):
    f.write ('srun ./bin/generateEarthChunks.py -b ' + str (i) + ' -t ' + str (i+size) + ' -d ' + str (disc) + ' -f /mnt/lnec/afanasm/cubitScratch/geom/masters/ \nsleep 2\n')

  switch = raw_input ('Type "exit" to exit, otherwise hit return to add more regions: ')

  


