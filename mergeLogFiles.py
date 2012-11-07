#!/usr/bin/env python
#
#Script to merge a directory of log files into one log file
#Note, make sure the log files are in the right format.  The script will just append the data!
#Tested on Windows 7, Python 3.2
#Michael Pursell 2012

import os
from subprocess import call

def fileOps(log, parseDirectory, dirList):
    
    x=1
    try:
        for arg in dirList:
            with open(os.path.join(parseDirectory,dirList[x]), 'r') as file: #look at filename in dirList[x] position
                readFile = file.read()
                logFile = open(log, 'a')
                logFile.write(readFile)
                x +=1 #increment x to iterate over dirList
   
        
    except:  #if x should increase too much, catch and exit gracefully
            exit
    

def userInput(command): #pass command to allow easy use of cls command

    #grab the file names from the user and call file_ops to read / write / close
    log = input("Gimme a log file to write:  ")
    call(command, shell=True)
    
    parseDirectory = input("Gimme a directory to parse:   ")
    call(command, shell=True)
    
    try:
        dirList = os.listdir(parseDirectory) #get the files in the directory as a list
        
    except WindowsError:                  #catch the exception thrown when invaild dir name given
        print('You need to enter a valid directory!')
        main()

    fileOps(log, parseDirectory, dirList) #call file_ops
     

def main():

    command = 'cls'
    call(command, shell=True)

   
    userInput(command)
    
    #subprocess.call(command, shell=True)
    print('Success! Contents appended and log file closed')
 


if __name__ == "__main__":
    main()
