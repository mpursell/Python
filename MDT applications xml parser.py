#Script to parse the MDT Applications.xml and scrape the
#name and guid of each application, then store in a dictionary.

#!/usr/env/ PYTHON


from xml.dom import minidom

################set the xml file name here########################
global xmlFileName
xmlFileName = "/home/mike/Applications.xml"
##################################################################



#function to grab the name and guid from the xml
def getGuids(nodelist, appDict):
  
	#iterate over our nodes in each 'application' element
	for item in nodelist:


		#find all the tags labelled 'Name'		
		names = item.getElementsByTagName('Name')
		
		#grab the GUIDs from the attributes of the 'application' tag
		#denoted by 'item'
		guids = item.getAttributeNode('guid')
		
		for name in names:
			
			#clean the leading and trailing xml tags from the name	
			name = name.toxml()
			name = name.replace('<Name>', '')
			name = name.replace('</Name>','')
			
			#add the items to the dictionary with the guid as the key
			appDict[guids.value]=name
	
	#iterate over the dictionary
	for key, value in appDict.iteritems():
		print ('{}, {}'.format(key, value))
	

def main():

	#parse the xml
	xmlfile = minidom.parse(xmlFileName)

	#apps are wrapped in 'application' elements in this xml
	nodelist = xmlfile.getElementsByTagName('application')

	

	#create a blank dictionary
	appDict = {}

	getGuids(nodelist, appDict)



if __name__=="__main__":
	main()
