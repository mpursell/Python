#Script to parse the MDT Applications.xml and scrape the 
#name and guid of each application, then store in a dictionary.

#!/usr/env/ PYTHON


from xml.dom import minidom
from xml.dom.minidom import Node

################set the xml file name here########################
global xmlFileName
xmlFileName = "/home/mike/Applications.xml"
##################################################################



#function to grab the name and guid from the xml
def getGuids(xmlfile, nodelist, appDict):
  
	#iterate over our nodes in each 'application' element
	for item in nodelist:
		
		#find the name in each element
		names = xmlfile.getElementsByTagName('Name')
		
		#for each name we want the guid which is set as an attribute in 
		#this particular xml file		
		for name in names:

			#get the attribute and then return its value
			guids = item.getAttributeNode('guid')
			guid = guids.value
			
			#toxml() outputs the name with leading and trailing <Name> tags
			#so we'll strip those tags
			appname = name.toxml()
			appname = appname.replace('<Name>','')
			appname = appname.replace('</Name>','')
			
			#append the clean strings to the blank dictionary
			appDict [appname]=guid

	
	with open('/home/mike/output.txt', 'w') as logFile:
	#iterate over the dictionary		
		for entry, value in appDict.iteritems():
		
		
			logFile.write('{}, {}\n'.format (entry, value))

			print ('{} {}'.format (entry, value))
		
	return appDict
			


def main():
	
	#parse the xml
	xmlfile = minidom.parse(xmlFileName)
	
	#apps are wrapped in 'application' elements in this xml
	nodelist = xmlfile.getElementsByTagName('application')

	#create a blank dictionary
	appDict = {}

	getGuids(xmlfile, nodelist, appDict)

if __name__=="__main__":
	main()
