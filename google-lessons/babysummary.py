#Summarise baby names alphabetically by decade of choice
#Google Python Lessons Exercise
#
#Michael Pursell 2012

#!/usr/bin/env/python


import re

def search(text):

    find = re.findall("<td align=\"center\">(\w+)</td> <td>(\d+,\d+)</td>", text)   #find the regex
    names = dict(find)                                                              #add results to a dict

def log(logfile)
    logfile.write(str(decade)+'\n')                                                 #write some title stuff
    logfile.write('Name, Popularity \n')                                            #

    for key, value in sorted(names.iteritems()):                            
        logfile.writelines(str(key)+','+str(value)+'\n')                            #iterate the dict and write log
    logfile.close()

def user_input():

    global decade                                                                   #set up some global vars
    decade = input('What decade would you like to search?  ')
    reference_file = open("c:\\python27\\babynames"+str(decade)+".htm")
    

    global text
    text = reference_file.read()

    logpath = input("Enter a path for output file:  ")

    global logfile
    logfile = open(logpath, 'a')

    
def main():
    
    user_input()
    try:                                                                            #try and catch if text or log is invalid
        search(text, logfile)
    except:
        print('Exiting')
        exit
    
    

if __name__ =="__main__":
    main()
