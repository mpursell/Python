#!/usr/bin/env python
#Regex search for baby names from social security .htm file as per Google Python Lessons exercise
#
#Michael Pursell 2012


import re

def user_input():
      
    global decade_input                                     #set a couple of global variable from user input
    decade_input = input('Enter a decade to search:  ')

    global name_input
    name_input = input('Enter a name to search:  ')

    global log_file
    log_file = input('Enter a logfile to log search results: ')


def search(decade_input, name_input):

    if decade_input:
        reference_text = open("C:\python32\\babyname"+decade_input+'.htm', 'r') #take the filename from user decade input
        text = reference_text.read()                                            #read in the file
        match = re.search((name_input), text)                                   #search for the name given in user input
        match_pop = re.search((name_input)+'..........(\d+.\d+)', text)         #search for the popularity   

        
       
        if match != False:
            try:
          
                babyname = match.group(0)
                popularity = match_pop.group(1)
                print(babyname+" was found")
                print (popularity+" babies were named "+name_input+" in "+decade_input)
                log = open(log_file, 'a')                                  
                log.writelines(babyname+','+popularity+','+decade_input+'\n')
                log.close()
                
            except AttributeError:                                              #If no match is found try and catch the
                print('Name not found in decade '+decade_input)                 #exception
                exit
        else:                                                                   #
            print('Name not found in decade '+decade_input)                     #
            exit


        



def main():

    user_input()
    search(decade_input, name_input)
   
    
if __name__ == "__main__":
    main()
