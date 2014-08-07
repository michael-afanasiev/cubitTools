#! /usr/bin/python

import sys

prefix = [ 'col000-090.lon000-090', 'col000-090.lon090-180', 'col000-090.lon180-270', 'col000-090.lon270-360',
           'col090-180.lon000-090', 'col090-180.lon090-180', 'col090-180.lon180-270', 'col090-180.lon270-360' ]

# Need even divisers.
top = []
bot = []
for rad in range (6371, 6351, -10):
    top.append (rad)
    bot.append (rad-10)

for rad in range (6351, 6271, -20):
    top.append (rad)
    bot.append (rad-20)

for rad in range (6271, 5971, -50):
    top.append (rad)
    bot.append (rad-50)

for rad in range (5971, 5701, -45):
    top.append (rad)
    bot.append (rad-45)

for rad in range (5701, 5371, -55):
    top.append (rad)
    bot.append (rad-55)

f = open ( 'drivers/meshDriver.sh', 'w' )
for pref in prefix:
    for t, b in zip (top, bot):
        f.write ( 'sbatch ./submit/job_baseMesh.sbatch ' + pref + ' ' + str (t) + ' ' + str (b) + '\n')
