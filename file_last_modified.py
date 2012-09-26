#!/usr/bin/env python
#Script to log the contents of a given directory (write new or append current log) to a file with a last modified stamp

#Michael Pursell 2012

import os, datetime, re, time

#function to list directory objects and write them to given log file
def dir_parse(path, logfile):

    dir = os.listdir(path)              #list objects in the given file path
    x = 0                               #set x to be used for list counting
    for file in dir:
        while x < len(dir):                     #while x is less than the length of the dir list
            file = str(path+"\\"+dir[x])        #glue the path and list item together to form a path
            dir_stats = os.path.getmtime(file)  #grab the path "modified time" as a timestamp
            mod_time = time.ctime(dir_stats)    #convert the timestamp to legible time format
            x = x+1                             #increment x to iterate the next item in the dir list
            logfile.writelines(file+", "+str(mod_time)+" "+"\n") #write the line with the filename and timestamp to log

    logfile.close()


def question(log_path):
    
    question = input("Do you want to search the log for a file?:  ")
    if question == "y":
        filename = input("What file are you looking for: ")
        find_entry(log_path, filename)                       #call find_entry
    else:
        exit                                                 # if no file search is required, exit program



def find_entry(log_path, filename):

       print(log_path)
       log = open(log_path, 'r')                    #re-open log file with read privs
       readfile = log.read()                        #read the log file into memory
       search = bool(re.search(filename, readfile)) #search for the regular exp given by filename inputted in main()
       if search == True:                           # search returns as bool = check for true / false
           print(filename+" exists")
           question(log_path)                       #call question to loop code back to y/n prompt
       else:
           print("File does not exist!")
           question(log_path)                       #call question to loop code back to y/n prompt
           


def main():

    #set some global variables
    path = input("Enter the directory to parse (no trailing \\): " )
    log_path = input("Enter the path and filename for the log file:  ")
    choice = input("Write or Append log? w or a:  ")
    if choice == 'w':
        try:                                                    #try and open the file
            logfile = open(log_path, 'w')                                                
            dir_parse(path, logfile,)                           #call parse and search functions
            question(log_path)
        except IOError:                                         #if an IO error is thrown, catch the exception
            print("File is already open or permission denied")
            exit
    else:                                                       #if we're not writing, we're appending!
        try:
            logfile = open(log_path, 'a')       
            dir_parse(path, logfile,)                           #call parse and search functions 
            question(log_path)
        except IOError:
            print("File is already open or permission denied")
            exit

    
    
  


if __name__ == "__main__":
    main()
