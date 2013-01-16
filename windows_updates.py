#!/usr/bin/env PYTHON
#script to query the Windows hotfixes installed, then scrape the titles from the MS KnowledgeBase
#Output a csv with the results
#Michael Pursell 2013
##############################################################################################################

import subprocess, urllib, re, string, sys

def main():
  
	#wmi query to output the hotifx ids and URLs to text file
	subprocess.call("wmic qfe >> c:\updates.txt", shell=True)
	
	#set the input file and initial regex searches up to find the URLs and the KB ids from the txt file
	with open("c:\updates.txt", 'rb') as inputFile:
		readFile = inputFile.read()
		convertedFile = readFile.decode('utf-16') #required to avoid the wide charset that the wmic query outputs
		urlSearch = re.findall("\S+[=]\d\d\d\d+\s", convertedFile) #regex for URLs
		updateIDSearch = re.findall("KB\d+\s",convertedFile) #regex for KB ID
		
		#call search function
		search(convertedFile, urlSearch, updateIDSearch) 
		
		#exit when done
		sys.exit()
		
		

#function to open the URLs, search the HTMl and pull content together into the output file. 
def search(convertedFile, urlSearch, updateIDSearch):
	
	#instantiate an empty list
	updateTitleList =[]		
	print("Finding update titles from the Microsoft Knowledge Base.  This may take some time...")
	
	with open("c:\updatesOutput.csv", 'a') as outputFile:
		for result in urlSearch:
			formattedResult = string.lstrip(result,'u') #strip the inexplicable leading 'u' from the URLs
			
			#open the URL and read the contents
			htmlPage = urllib.urlopen(formattedResult)
			htmlRead = htmlPage.read()
			
			#specify start and end html tags and pull the content from inbetween them
			startTag = "<h1 class=\"title\" id=\"mt_title\">"
			endTag = "</h1>"
			startIndex = htmlRead.find(startTag)+len(startTag)
			endIndex = htmlRead.find(endTag)
			updateTitle = htmlRead[startIndex:endIndex]
			
			#code to help csv formatting
			updateTitleFormatted = updateTitle.replace(',',' ') #remove commas from dates in titles
			updateTitleString = updateTitleFormatted + ','#add a comma at the end of the title
			
			
			updateTitleList.append(updateTitleString)
		
		#dictionary that zips together the list of titles with KB ids
		updateDict = dict(zip(updateTitleList,updateIDSearch))
		
		
		
		for key, value in updateDict.iteritems():
			outputFile.write("{}{}\n".format(key,value))	


			
if __name__=="__main__":
	main()
