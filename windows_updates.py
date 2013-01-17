#!/usr/bin/env PYTHON
#script to query the Windows hotfixes installed, then scrape the titles from the MS KnowledgeBase
#Output a csv with the results
#Tested with Python 2.7 under Windows 7
#Michael Pursell 2013
##############################################################################################################

#import subprocess, urllib, re, string, sys, os

from subprocess import call
from urllib import urlopen
from re import findall
from string import lstrip

	
#function to setup some initial parameters and the WMI query	
def runQuery():
	
	call("cls", shell=True) #clear the terminal
	print("\n********************************************************************************")
	print("\nThis script will find the Hotfix IDs and the associated MS KnowledgeBase titles")
	print("Please make sure that you have a working internet connection!\n")
	question = raw_input("Proceed? Y/N...  ")
	
	
	if question == "y":
	
		#shell out the wmi query to output the hotifx ids and URLs to text file
		call("wmic qfe >> c:\updates.txt", shell=True)
		
		#set the input file and initial regex searches up to find the URLs and the KB ids from the txt file
		with open("c:\updates.txt", 'rb') as inputFile:
			
			#read in the file and convert it to utf-16,
			#required to avoid the wide charset that the wmic query outputs
			readFile = inputFile.read()
			convertedFile = readFile.decode('utf-16') 
			
			#regex for URLs - in this case all the URLs follow this pattern: http://support.microsoft.com/?kbid=2425227
			urlSearch = findall("\S+[=]\d\d\d\d+\s", convertedFile) 
			
			updateIDSearch = findall("KB\d+\s",convertedFile) #regex for KB ID
			
				
			#call search function
			searchHTML(convertedFile, urlSearch, updateIDSearch) 
			
			call("cls", shell=True) #Clear the terminal
			print("Completed! Check the root of C: for the updatesOutput.csv")
			#exit when done
			exit()
	else:
		exit()
		
		

#function to open the URLs, search the HTMl and pull content together into the output file. 
def searchHTML(convertedFile, urlSearch, updateIDSearch):
	
	#instantiate an empty list
	updateTitleList =[]		
	print("\nFinding update titles from the Microsoft Knowledge Base.\nThis may take some time...")
	
	with open("c:\updatesOutput.csv", 'a') as outputFile:
		for result in urlSearch:
			formattedResult = lstrip(result,'u') #strip the leading 'u' from the URLs after regex search
			
			#open the URL and read the contents
			htmlPage = urlopen(formattedResult)
			htmlRead = htmlPage.read()
			
			#specify start and end html tags and pull the content from inbetween them
			#in this case we're only interested in the titles that sit between the <h1> tags
			startTag = "<h1 class=\"title\" id=\"mt_title\">"
			endTag = "</h1>"
			startIndex = htmlRead.find(startTag)+len(startTag)
			endIndex = htmlRead.find(endTag)
			updateTitle = htmlRead[startIndex:endIndex]
			
			#code to help csv formatting
			updateTitleFormatted = updateTitle.replace(',',' ') #remove commas from dates in titles
			updateTitleString = updateTitleFormatted + ' '
			
			#append all our web scraped titles to a list
			updateTitleList.append(updateTitleString)
		
		#dictionary that zips together the list of titles with KB ids
		updateDict = dict(zip(updateTitleList,updateIDSearch))
		
		
		#iterate over the dictionary and write keys and values to the output file
		for key, value in updateDict.iteritems():
			outputFile.write("{}({})\n".format(key,value))	



def main():
	
	runQuery()
			
			
if __name__=="__main__":
	main()

