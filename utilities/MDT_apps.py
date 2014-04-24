#Script to parse the MDT 2012 Applications.xml from DEPLOYSHARE\Control and the results of an SQL query on
#the MDT database.  This returns:
#Applications.xml : guid -> application name
#SQL query : role -> guid
#The purpose of the script is to compare the lists and output the role with the applicable
#application names listed.  It will also check the dependencies of the application bundles
#and list them at the bottom of the output file.

#Tested with Python 2.7 on Windows 7 
#Michael Pursell 2013

#!/usr/env/ PYTHON


from xml.dom import minidom
from string import lstrip
import pyodbc, subprocess

#globals not really required here.  Set up this way to make it easy to remember
#to set them up at the top of the script.

################ set file names #################################
global xmlFileName
global log


#location of the applications.xml
xmlFileName = "Y:\\Deploy\\MDSDevelopment\\Control\\Applications.xml"

#just a text log file with all the build apps logged
log = "c:\\MDTapps.txt"

blankDoc = 'C:\\Users\\<username>\\Documents\\Build Docs\\blank_MDS.docx'


##########  MDT guids for application bundles ################

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

################# set the SQL connection details ######################
global sqlserver
global sqldatabase
global sqluser
global sqlpassword

sqlserver = ''
sqldatabase = ''
sqluser = ''
sqlpassword = ''

################ VERSIONING INFO NEEDS TO BE SET BY USER ####################
global docDate
global docVersion
global docAuthor
global docUpdateReason

docDate = ''
docVersion = ''
docAuthor = ''
docUpdateReason = ''

######################### CURRENT OPERATING SYSTEMS ########################

global xp
global sevenpro32
global sevenpro64

xp = 'Windows XP.'
sevenpro32 = 'Windows 7 Professional 32bit'
sevenpro64 = 'Windows 7 Professional 64bit'



############################################################################

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

	
	return appList
	
	
	
#function to query the SQl database for role and application.
def sqlRoleQuery(sqlList):

	#establish the connection
	#Note: have to use the deprecated %s instead of .format() in the connection string
	cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;Trusted_Connection=Yes'%(sqlserver, sqldatabase, sqluser,sqlpassword))
	cursor = cnxn.cursor()
	
	#SQL statements
	cursor.execute("SELECT role, applications FROM RoleApplications")
	rows = cursor.fetchall()
	
	#append each row in the results to our sqlList
	for row in rows:
		sqlList.append((row.role, row.applications))

	return sqlList


	
#function to query the SQL database for role and Domain Name
def sqlDomainQuery(sqlDomainList):

	#establish the connection
	#Note: have to use the deprecated %s instead of .format() in the connection string
	cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;Trusted_Connection=Yes'%(sqlserver, sqldatabase, sqluser,sqlpassword))
	cursor = cnxn.cursor()
	
	#SQL statements
	cursor.execute("SELECT Role, DomainName FROM RoleSettings WHERE DomainName <> 'NULL' AND DomainName <> ' '")
	rows = cursor.fetchall()
	
	#append each row in the results to our sqlList
	for row in rows:
		sqlDomainList.append((row.Role, row.DomainName))
	
	return sqlDomainList


#function to query the SQL database for role and OU name	
def sqlOUQuery(sqlOUList):

	#establish the connection
	#Note: have to use the deprecated %s instead of .format() in the connection string
	cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;Trusted_Connection=Yes'%(sqlserver, sqldatabase, sqluser,sqlpassword))
	cursor = cnxn.cursor()
	
	#SQL statements
	cursor.execute("SELECT Role, CustomerOU FROM RoleSettings WHERE CustomerOU <> 'NULL' AND CustomerOU <> ' '")
	rows = cursor.fetchall()
	
	#append each row in the results to our sqlList
	for row in rows:
		sqlOUList.append((row.Role, row.CustomerOU))
	
	return sqlOUList
	
#function to query the SQL database for role and machine name prefix	
def sqlPrefixQuery(sqlPrefixList):

	#establish the connection
	#Note: have to use the deprecated %s instead of .format() in the connection string
	cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;Trusted_Connection=Yes'%(sqlserver, sqldatabase, sqluser,sqlpassword))
	cursor = cnxn.cursor()
	
	#SQL statements
	cursor.execute("SELECT Role, ComputernamePrefix FROM RoleSettings WHERE ComputernamePrefix <> 'NULL' AND ComputernamePrefix <> ' '")
	rows = cursor.fetchall()
	
	#append each row in the results to our sqlList
	for row in rows:
		sqlPrefixList.append((row.Role, row.ComputernamePrefix))
	
	return sqlPrefixList
	
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


#function to create documents from a blank document template blank_MDS.docx
def generateDocs(sqlList, sqlDomainList, sqlOUList, sqlPrefixList, finalList):

	#create a list we'll use just for the role names
	sqlRoleList= []
	
	#populate the list with sql role names from sql list
	for entry in sqlList:
		sqlRoleList.append(entry[0])
	
	#create a set to remove duplicates
	sqlRoleList = set(sqlRoleList)
	
	choice = raw_input('\n**WARNING**\nGenerating documents will take some time.\nThere are currently {} SQL roles to produce documentation for.\nWould you like to generate MDS documents (y/n)?  '.format(len(sqlRoleList)))
	#choose whether to generate documents
	if choice == 'y':
			
		for entry in sqlRoleList:

			#extract the docx into the given path
			subprocess.call("7za x -o\"c:\\blankdoc\" -y \"{}\"".format(blankDoc), shell=True)

			#set the document.xml file as the file we want to edit
			document  = "c:\\blankdoc\\word\\document.xml"
			
			###### Versioning replacements #######
			
			#setup our replacement text
			#currently using FakeXXX to demarcate where replacements are needed
			title = ('FakeTitle')
			new_title = entry
			
			smalltitle = ('FakeSmallTitle')
			new_smalltitle = (new_title)
			
			version = ('FakeVersion')
			new_version = (docVersion)
			
			author = ('FakeAuthor')
			new_author = (docAuthor)
			
			date = ('FakeDate')
			new_date = (docDate)
			
			update = ('FakeUpdates')
			new_update = (docUpdateReason)
			
			apps = ('FakeApps')

			#do the replacements in memory
			with open(document, 'r') as doc:
				
				readfile = doc.read()
				readfile = readfile.replace(title, new_title)
				readfile = readfile.replace(smalltitle, new_smalltitle)
				readfile = readfile.replace(version, new_version)
				readfile = readfile.replace(author, new_author)
				readfile = readfile.replace(date, new_date)
				readfile = readfile.replace(update, new_update)
				
				####### Application replacements ########
				
				#if the role name for the application is the same as the sqlList role
				#replace FakeApps with the list of applications from finalList
				
				applicationList = []
				for item in finalList:
					
					if item[0] == entry:
						
						#applicationList.append(item[1])
						applicationList.append('<w:p><w:pPr><w:ind w:left=\"0\" /> <w:rPr><w:szCs w:val=\"18\" /></w:rPr></w:pPr><w:r><w:rPr><w:szCs w:val=\"18\" /> </w:rPr><w:t>{}</w:t> </w:r></w:p>'.format(item[1]))
					
				
				#join the list items into a string so we can write them out
				applications = ''.join(applicationList)	
				
				#replace placeholder text with application list
				readfile = readfile.replace(apps, applications)
				
				
				########## Domain Name replacements ############
				
				for domain in sqlDomainList:
					if domain[0] == entry:
						readfile = readfile.replace('FakeDomainName', domain[1])
					
						
				
				########## Machine Prefix replacments ###########
				
				for prefix in sqlPrefixList:
					if prefix[0] == entry:
						if 'Laptop' in entry:
							readfile = readfile.replace('FakePrefix', prefix[1]+'LT')
						else:
							readfile = readfile.replace('FakePrefix', prefix[1]+'DT')
					
				
				########## OU name replacements ################
				
				for ou in sqlOUList:
					if ou[0] == entry:
						readfile = readfile.replace('FakeOUName', ou[1])	
					
				
				############### OS replacements ####################
				
				if '64' in entry:
					readfile = readfile.replace('FakeOS', sevenpro64)
					
				elif 'x86' in entry:
					readfile = readfile.replace('FakeOS', sevenpro32)
					
				elif '32' in entry:
					readfile = readfile.replace('FakeOS', sevenpro32)
									
				else:
					readfile = readfile.replace('FakeOS', xp)
				
				
				#write the document.xml file back out with amendments
				with open(document, 'w') as file:
					
					try:
						file.write(readfile)
					except:
						#not ideal - sqlOUQuery returns a strange result character for CHKS that throws an exception
						pass
					
				#re-archive the files as a .docx file		
				subprocess.call("7za a -tzip \"c:/results/{}.docx\" \"c:/blankdoc/\*\"".format(entry), shell= True)

	else:
		print('Done')	


		
		
def main():


	#parse the MDT applications.xml
	xmlfile = minidom.parse(xmlFileName)

	#apps are wrapped in 'application' elements in this xml
	nodelist = xmlfile.getElementsByTagName('application')

	#create a blank apps list
	appList = []

	#create blank sql lists to populate with queries
	sqlList = []
	sqlDomainList =[]
	sqlNamingList = []
	sqlOUList = []
	sqlPrefixList = []
	
	#create a blank final presentation list
	finalList= []

	#populate the lists with the returns from the functions
	appList = getGuids(nodelist, appList)
	sqlList = sqlRoleQuery(sqlList)
	sqlDomainList = sqlDomainQuery(sqlDomainList)
	sqlOUList = sqlOUQuery(sqlOUList)
	sqlPrefixList = sqlPrefixQuery(sqlPrefixList)
	
	#iterate over the lists and match the guids in the tuples[0]
	with open (log, 'w')as logger:
		for entry in appList:
			for item in sqlList:
				#if the guids match up, write the log entry
				if entry[1] == item[1]:
					#append the matches to the final list
					finalList.append((item[0], entry[0]))
		

		#sort the final list for easier reading and write it out
		finalList = (sorted(finalList))
		for listItem in finalList:
			logger.write('{}, {} \n'.format(listItem[0], listItem[1]))
					
	#call function to find bundle dependencies
	depends(nodelist, appList)
	
	#for item in sqlOUList:
	#	print item
	generateDocs(sqlList, sqlDomainList, sqlOUList, sqlPrefixList, finalList)
	



if __name__=="__main__":
	main()
