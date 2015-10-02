#!/usr/bin/env python
# simple script to easy build all presentation at once

import os
import subprocess

mainFolder = os.path.dirname(os.path.realpath(__file__))
courses = os.walk(mainFolder).next()[1]

for course in courses:
    if course != 'resources' and not course.startswith("."):
        lectures = os.walk(os.path.join(mainFolder, course)).next()[1]
        
        for lecture in lectures:
            os.chdir(os.path.join(mainFolder, course, lecture))
        
            for lectureFile in os.listdir("."):
                if lectureFile.endswith(".tex"):
                    print('Processing: ' + os.path.join(mainFolder, course, lecture))
                    subprocess.call(["pdflatex", lectureFile], stdout=open(os.devnull, 'wb'))
                    subprocess.call(["pdflatex", lectureFile], stdout=open(os.devnull, 'wb'))
        
            for tempLectureFile in os.listdir("."):
                if tempLectureFile.endswith(('.aux', '.log', '.nav', '.out', '.snm', '.toc')):
                    os.remove(tempLectureFile)
