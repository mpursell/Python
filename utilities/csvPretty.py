#!/usr/bin/env PYTHON
#csv to HTML prettifier - counts the frequency of items in the csv columns
#outputs an HTML table.
#Tested using Python 3.2 on Windows 7
#Michael Pursell 2012

import os, csv, re, sys, subprocess
from collections import Counter, OrderedDict
from pprint import pprint

def main():

    myPath = input("Enter the path to a .csv file to parse: ")
    logPath = input("Enter a path and an HTML file for output: ")
    description = input("Enter some descriptive text:  ")

    #write some initial stylesheet info and html
    with open(logPath, 'a') as log:
        
        log.write("<html>")
        log.write("<head>")
        log.write("<meta content='IE=edge' />")
        log.write("<style type='text/css'>")
        log.write(".wrapper{margin-left: 75px; margin-right: 75px;}")
        log.write(".logo{height: 50px; width: 100px; clear: both; margin-bottom: 5px;}")
        log.write(".title{height: 80px; width: 100%; background-color: #024D73; color: #FFF; font-family: Calibri; border-radius: 15px; text-align: center; box-shadow: 5px 5px 5px 2px #888; margin-bottom: 20px;padding-top: 1px; padding-top: 10px;}")
        log.write(".textHolder{width: 100%; color: #888; font-family: Calibri; padding-top: 1px; margin-bottom: 15px;  margin-left: 15px;}")
        log.write(".tableContent{height:50%; float: left; margin-right:15px; margin-left: 15px; margin-bottom: 15px;}")
        log.write("table, th, td{padding:10px; border:1px solid #888; border-collapse: collapse; font-family:Calibri;}")
        log.write("th{background-color: #024D73; color:#FFF; font-weight: bold;}")
        log.write("</style>")
        log.write("</head>")
        log.write("<body>")
        log.write("<div class='wrapper'>")
        log.write("<div class='logo'>")
        log.write("<img src='http://www.capita-its.co.uk/images/logo.jpg' alt='Capita IT Services' />")
        log.write("</div>")
        log.write("<div class='title'>")
        log.write("<h1>CSV Presenter</h1>")
        log.write("</div>")
        log.write("<div class='textHolder'>")
        log.write("<p>{}</p>".format(description))
        log.write("</div>")
        
        
    

    buildLogFile(myPath, logPath)


def buildLogFile(myPath, logPath):

   
    
    with open(myPath, 'r') as myFile:
        myFileReader = csv.reader(myFile)

        columnList = next(myFileReader) #grab the first line of the csv for the column headers
        print("\nColumns to select \n\n{}\n".format(columnList))
        userColumn = input("Enter a column number to search (leftmost column is 0): ")
        print("\nColumn '{}' selected\n".format(columnList[int(userColumn)]))

        #instantiate a list
        csvList = []
        
        for row in myFileReader:
            #iterate over rows in csv, for each item in myFileReader select the right list index
            value = row[int(userColumn)]
            #append to the list
            csvList.append(value)
          
    listCount = Counter(csvList) #counts items and creates dict from csvList of item: frequency pairs
    #pprint(OrderedDict(sorted(listCount.items(), key = lambda x: x[1]))) #pretty prints the OrderedDict


    #print("\n {} entries in total".format(listLength))
    writeHTML(columnList, userColumn, listCount, logPath, myPath)


    listLength = len(csvList)
       

    
#function to write an HTML log
def writeHTML(columnList, userColumn, listCount, logPath, myPath):

    with open(logPath, 'a') as log:

    
        log.write("<div class='tableContent'>")
        log.write("<table><tr><th>{}</th><th>Count</th></tr>".format(columnList[int(userColumn)]))

        for listCountItem in OrderedDict(sorted(listCount.items(), key = lambda x: x[1])):
            log.write("<tr><td>{}</td><td>{}</td></tr>".format(listCountItem, listCount[listCountItem]))
        log.write("</table>")
        log.write("</div>")
        log.write("</div>")
        log.write("</body>")
        log.write("</html>")

    question = input("Go again to capture more columns? (y/n)  ")
    if question == "y":
        buildLogFile(myPath, logPath)
    else:
        subprocess.call("\"c:\program files\internet explorer\iexplore.exe\" \"{}\"".format(logPath), shell=True)
            

if __name__=="__main__":
    main()
                       
            
            
        
            


