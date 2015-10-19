#!/usr/bin/env python
# -*- coding: utf8 -*-
# simple script to easy build all presentation at once

import os
import subprocess
import codecs
from datetime import datetime, timedelta


# locate working directory
mainFolder = os.path.dirname(os.path.realpath(__file__))
courses = os.walk(mainFolder).next()[1]

# get git data
os.chdir(mainFolder)
gitLog = subprocess.check_output(['git', 'log', '-1'])
gitOrigin = subprocess.check_output(['git', 'remote', 'show', 'origin'])

commit = gitLog.partition('commit')[2].partition('\n')[0].strip()
author = gitLog.partition('Author:')[2].partition('\n')[0].strip().replace('>',r'\textgreater{}').replace('<',r'\textless{}')
lastUpdateString = gitLog.partition('Date:')[2].partition('\n')[0].strip()
remote = gitOrigin.partition('Fetch URL:')[2].partition('\n')[0].strip()

# format the date
lastUpdateStrings = lastUpdateString.split('+')
lastUpdate = datetime.strptime(lastUpdateStrings[0].strip(), "%a %b %d %H:%M:%S %Y")

dH = int(lastUpdateStrings[1][:2])
dM = int(lastUpdateStrings[1][2:])

lastUpdate += -timedelta(hours=dH, minutes=dM)
lastUpdate = lastUpdate.strftime("%d.%m.%Y um %H:%M (UTC)")

# build the version slide
versionText = ur'''
\begin{block}{Version} 
    \textbf{Commit ID:} %s \vspace{0.5em}\newline
	  Letzte Änderung am %s 
	  durch %s \vspace{0.5em}\newline
	  \textbf{Quelle:} %s
\end{block}
''' %(commit, lastUpdate, author, remote)

# save the version file
versionFile = codecs.open(os.path.join(mainFolder, 'resources', 'version'), encoding='utf-8', mode='w')
versionFile.write(versionText)
versionFile.close()

# run pdflatex twice on all tex files and clean up afterwards
for course in courses:
    if course != 'resources' and not course.startswith('.'):
        lectures = os.walk(os.path.join(mainFolder, course)).next()[1]
        
        for lecture in lectures:
            os.chdir(os.path.join(mainFolder, course, lecture))
        
            for lectureFile in os.listdir('.'):
                if lectureFile.endswith('.tex'):
                    print('Processing: ' + os.path.join(mainFolder, course, lecture))
                    subprocess.call(['pdflatex', lectureFile], stdout=open(os.devnull, 'wb'))
                    subprocess.call(['pdflatex', lectureFile], stdout=open(os.devnull, 'wb'))
        
            for tempLectureFile in os.listdir('.'):
                if tempLectureFile.endswith(('.aux', '.log', '.nav', '.out', '.snm', '.toc')):
                    os.remove(tempLectureFile)

# remove the version file to prevent old version data is included when the source 
# is not compiled by this script
os.remove(os.path.join(mainFolder, 'resources', 'version'))