#!/usr/bin/env PYTHON
#Will count the given entries in a csv file if you know the item
#and column name you're searching

import os, csv, re

def main():

    
    myPath = input("Gimme a csv to parse: ")
    with open(myPath, 'r') as myFile:
        myFileReader = csv.reader(myFile)
        userItem = input("Enter an item: ")
        userColumn = input("Enter a column name to search: ")
        x = 0
        for userColumn in myFileReader:
            if userItem in userColumn:
                x = x+1
        print("\n\n{}: {} entries".format(userItem, x))
            


if __name__=="__main__":
    main()
