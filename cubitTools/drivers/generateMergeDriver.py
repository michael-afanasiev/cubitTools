#! /usr/bin/python

import sys
import os

if len (sys.argv) < 2 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
    sys.exit ("usage: ejoinRefiend -t [top] -b [bottom] -f [path]")

for i in range ( len (sys.argv) ):
    if sys.argv[i] == '-t':
        top = int (sys.argv[i+1])
    if sys.argv[i] == '-b':
        bot = int (sys.argv[i+1])
    if sys.argv[i] == '-f':
        pat = sys.argv[i+1]

outDir = pat + 'mesh/conjoined'
a = 'sbatch ./submit/job_mergeMesh.sbatch "ejoin  --output ' + outDir + '/col000-090.lon000-090.rad' + str (bot) + '-' + str (top) + '.000.ex2'
b = 'sbatch ./submit/job_mergeMesh.sbatch "ejoin  --output ' + outDir + '/col000-090.lon090-180.rad' + str (bot) + '-' + str (top) + '.000.ex2'
c = 'sbatch ./submit/job_mergeMesh.sbatch "ejoin  --output ' + outDir + '/col000-090.lon180-270.rad' + str (bot) + '-' + str (top) + '.000.ex2'
d = 'sbatch ./submit/job_mergeMesh.sbatch "ejoin  --output ' + outDir + '/col000-090.lon270-360.rad' + str (bot) + '-' + str (top) + '.000.ex2'
e = 'sbatch ./submit/job_mergeMesh.sbatch "ejoin  --output ' + outDir + '/col090-180.lon000-090.rad' + str (bot) + '-' + str (top) + '.000.ex2'
f = 'sbatch ./submit/job_mergeMesh.sbatch "ejoin  --output ' + outDir + '/col090-180.lon090-180.rad' + str (bot) + '-' + str (top) + '.000.ex2'
g = 'sbatch ./submit/job_mergeMesh.sbatch "ejoin  --output ' + outDir + '/col090-180.lon180-270.rad' + str (bot) + '-' + str (top) + '.000.ex2'
h = 'sbatch ./submit/job_mergeMesh.sbatch "ejoin  --output ' + outDir + '/col090-180.lon270-360.rad' + str (bot) + '-' + str (top) + '.000.ex2'

for file in os.listdir (pat + 'mesh/refined'):

    fields    = file.split ('.')
    radFields = fields[2]
    botRad    = int (radFields[3:7])
    topRad    = int (radFields[8:12])
    
    if botRad >= bot and topRad <= top:

        if fields[0] == 'col000-090':
            if fields[1] == 'lon000-090':
                a = a + ' ' + pat + 'mesh/refined/' + file

        if fields[0] == 'col000-090':
            if fields[1] == 'lon090-180':
                b = b + ' ' + pat + 'mesh/refined/' + file


        if fields[0] == 'col000-090':
            if fields[1] == 'lon180-270':
                c = c + ' ' + pat + 'mesh/refined/' + file

        if fields[0] == 'col000-090':
            if fields[1] == 'lon270-360':
                d = d + ' ' + pat + 'mesh/refined/' + file


        if fields[0] == 'col090-180':
            if fields[1] == 'lon000-090':
                e = e + ' ' + pat + 'mesh/refined/' + file


        if fields[0] == 'col090-180':
            if fields[1] == 'lon090-180':
                f = f + ' ' + pat + 'mesh/refined/' + file


        if fields[0] == 'col090-180':
            if fields[1] == 'lon180-270':
                g = g + ' ' + pat + 'mesh/refined/' + file


        if fields[0] == 'col090-180':
            if fields[1] == 'lon270-360':
                h = h + ' ' + pat + 'mesh/refined/' + file

file = open ('./drivers/mergeDriver.sh', 'w')
file.write (a + '"\n')
file.write (b + '"\n')
file.write (c + '"\n')
file.write (d + '"\n')
file.write (e + '"\n')
file.write (f + '"\n')
file.write (g + '"\n')
file.write (h + '"')
file.close ()
