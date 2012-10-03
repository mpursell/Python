#!/usr/bin/env python
#
#Script to merge a directory of log files into one log file
#Note, make sure the log files are in the right format.  The script will just append the data!
#Michael Pursell 2012

import sys, os, subprocess

def file_ops(log, user_input, dir_list):
    x=1
    try:
        for arg in dir_list:
            file = open(user_input+'\\'+dir_list[x], 'r') #look at filename in dir_list[x] position
            read_file = file.read()
            logfile = open(log, 'a')
            logfile.write(read_file+'\n')
            x=x+1 #increment x to iterate over dir_list
        logfile.close
    except IndexError:  #if x should increase too much, catch and exit gracefully
            exit
    
        


def user_input(command):

    #grab the file names from the user and call file_ops to read / write / close
    log = input('Enter log file to append:  ')
    subprocess.call(command, shell=True)
    user_input = input('Gimme a directory to parse:   ')
    subprocess.call(command, shell=True)
    dir_list = os.listdir(user_input) #get the files in the directory as a list

    file_ops(log, user_input, dir_list) #call file_ops
     

def main():

    command = 'cls'
    choice = input('Append file? (Y/N): ')
    subprocess.call(command, shell=True)

    if choice == 'y':
        user_input(command)
        subprocess.call(command, shell=True)
        print('Success! Contents appended and log file closed')
    elif choice == 'n':
        print('Exiting')
        exit
    else:
        print('You need to choose yes or no!')
        exit


if __name__ == "__main__":
    main()
