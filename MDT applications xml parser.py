#Script to parse the MDT Applications.xml and the results of an SQL query on
#the MDT database.  This returns:
#Applications.xml : guid -> application name
#SQL query : role -> guid
#The purpose of the script is to compare the lists and output the role with the applicable
#application names listed.  It will also check the dependencies of the application bundles
#and list them at the bottom of the output file.

#First you need to set the locations of the xml file, sql results csv and the log file:
#You also need to make sure that the GUIDs listed below for the app bundles are correct.

#Tested with Python 2.7 on Windows 7 
#Michael Pursell 2013

#!/usr/env/ PYTHON


from xml.dom import minidom
import csv

################set file names here#################################
global xmlFileName
xmlFileName = "Y:\\Deploy\\MDSDevelopment\\Control\\Applications.xml"

global log
log = "c:\\output.txt"

global sqlFile
sqlFile = "C:\\sqlQuery.csv"



##########set the guids for application bundles here################

global desktopBundle32
global desktopBundle64
global laptopBundle32
global laptopBundle64

desktopBundle32 = '{f30ba9b5-8d89-428d-8e4c-776bad8c5ee2}'
desktopBundle64 = '{48c0fbd1-151d-48e4-8c80-727bf46d3a8b}'
laptopBundle32 = '{f07420b6-6087-43be-9994-452ab1a9d453}'
laptopBundle64 = '{254602ae-e6c5-480d-8e5e-78afef891d0c}'
ibsBundle = '{50c6be98-fffc-4690-9d4c-fb9beab32881}'
cerBundle = '{b697d8e7-8162-4c05-84a2-cb2eddc9efac}'
cidBundle = '{bffd0b03-e1fb-48ac-8fd7-fc181a088769}'
chBundle32 = '{009b817e-56a4-46be-b051-2a42e64a4fd1}'
vpnBundle = '{8036776c-ea2a-4f94-9165-e2705172c5d4}'


#####################################################################



#function to grab the name and guid from the xml
def getGuids(nodelist, appList):
  
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

			#append tuples of (name, guid) to the list
			appList.append((name, guids.value))
			

	
	
	#with open(log, 'w') as logFile:
		
		#iterate over the list of tuples
		#for entry in appList:
		#	logFile.write('{}\n'.format(str(entry)))
	
	return appList
	
#function to read in the text file from a SQl dump
#To create the dump execute the query SELECT Role, Applications FROM RoleApplications
def sqlQuery(sqlFile,sqlList):

	with open(sqlFile) as sql:

		sqlRead = csv.reader(sql, delimiter=',')
		
		for line in sqlRead:
			#print line[0]
			sqlList.append((line[0], line[1]))
			
	return sqlList

			
def main():

	#parse the xml
	xmlfile = minidom.parse(xmlFileName)

	#apps are wrapped in 'application' elements in this xml
	nodelist = xmlfile.getElementsByTagName('application')

	#create a blank apps list
	appList = []

	#create a blank sql list
	sqlList = []
	
	#create a blank final presentation list
	finalList= []

	#populate the lists with the returns from the functions
	appList = getGuids(nodelist, appList)
	sqlList = sqlQuery(sqlFile, sqlList)
	
	#iterate over the lists and match the guids in the tuples[0]
	with open (log, 'w')as logger:
		for entry in appList:
			for item in sqlList:
				if entry[1] == item[1]:
					#append the matches to the final list
					finalList.append((item[0], entry[0]))
		

		#sort the final list for easier reading and write it out
		finalList = (sorted(finalList))
		for listItem in finalList:
			logger.write('{}, {} \n'.format(listItem[0], listItem[1]))
					
	#call function to find bundle dependencies
	depends(nodelist, appList)


	
#function to find the dependencies of a given application bundle	
#function fails DRY pretty badly; needs refactoring at some point. 

def depends(nodelist, appList):
	
	
		#iterate over our nodes in each 'application' element
		#and check for guids that equal our bundle guids we've already defined
		for item in nodelist:
			
			guids = item.getAttributeNode('guid')
			
			if  guids.value == desktopBundle32:
				
				
				with open(log, 'a') as logger:
					logger.write('\n\nDESKTOP BUNDLE 32BIT\n')
					#print('\n\nDESKTOP BUNDLE 32BIT\n')
					#find all the tags labelled 'Dependency'		
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]
								logger.write('{}\n'.format(app[0]))
					
			elif guids.value == desktopBundle64:
				
				
				with open(log, 'a') as logger:
				
					logger.write('\n\nDESKTOP BUNDLE 64BIT\n')
					#print('\n\nDESKTOP BUNDLE 64BIT\n')
						
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]
								logger.write('{}\n'.format(app[0]))

			elif guids.value == laptopBundle32:
	
	
				with open(log, 'a') as logger:
				
					logger.write('\n\nLAPTOP BUNDLE 32BIT\n')
					#print('\n\nLAPTOP BUNDLE 32BIT\n')
						
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]
								logger.write('{}\n'.format(app[0]))
							
			elif guids.value == laptopBundle64:

			
				with open(log, 'a') as logger:
				
					logger.write('\n\nLAPTOP BUNDLE 64BIT\n')
					#print('\n\nLAPTOP BUNDLE 64BIT\n')
						
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]	
								logger.write('{}\n'.format(app[0]))	

		
			elif guids.value == ibsBundle:
	
	
				with open(log, 'a') as logger:
				
					logger.write('\n\nIBS APPS BUNDLE\n')
					#print('\n\nIBS APPS BUNDLE\n')
						
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]	
								logger.write('{}\n'.format(app[0]))		
								
			elif guids.value == cerBundle:
	
	
				with open(log, 'a') as logger:
				
					logger.write('\n\nCER APPS BUNDLE\n')
					#print('\n\nIBS APPS BUNDLE\n')
							
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]	
								logger.write('{}\n'.format(app[0]))	
								
								
							
			elif guids.value == cidBundle:
	
	
				with open(log, 'a') as logger:
				
					logger.write('\n\nCID APPS BUNDLE\n')
					#print('\n\nIBS APPS BUNDLE\n')
						
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]	
								logger.write('{}\n'.format(app[0]))	
				
			elif guids.value == chBundle32:
	
	
				with open(log, 'a') as logger:
				
					logger.write('\n\nCAPITA HEALTH APPS BUNDLE\n')
					#print('\n\nIBS APPS BUNDLE\n')
						
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]	
								logger.write('{}\n'.format(app[0]))	
			
			
			elif guids.value == vpnBundle:
	
	
				with open(log, 'a') as logger:
				
					logger.write('\n\nVPN BUNDLE\n')
					#print('\n\nIBS APPS BUNDLE\n')
						
					names = item.getElementsByTagName('Dependency')

					for name in names:

						#clean the leading and trailing xml tags from the name	
						name = name.toxml()
						name = name.strip('<Dependency>')
						name = name.strip('</Dependency>')
						
						for app in appList:
							if name == app[1]:
								#print app[0]	
								logger.write('{}\n'.format(app[0]))	
								
								
								
								
if __name__=="__main__":
	main()
