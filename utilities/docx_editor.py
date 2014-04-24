#Script to open docx files, replace given OS and software versions, and re-package the docx file.
#It will parse the given directory, edit ALL documents and write them to a directory\newDocs folder
#Requires the 7za command line tool in the Python directory
#Tested on Windows 7 with Python 2.7
#Michael Pursell 2013


import os, subprocess


def main():

	###################################################################################
	#
	#Set these variables first
	#
	###################################################################################
	
	#set author, version and reason for update
	#used for the Document Information and Revision History
	authorFirstName = ('Michael')
	authorLastName = ('Pursell')
	version = ('1.1')
	updateReason = ('Q1 2013 updates')
	editDate = ('25/01')
	editYear = ('2013')

	#set variables for Source OS
	
	#Windows 7
	oldSourceOS2012 = ('2012.4')
	oldSourceOS2013 = ('2013.1')
	newSourceOS = ('2013.1')
	
	#XP
	oldSourceXP = ('XPSP3_22')
	newSourceXP = ('XPSP3_23')
	
	
	oldPatchDay = ('28')
	oldPatchDate = ('June 2012')
	newPatchDay = ('01')
	newPatchDate = ('December 2012')
	
	oldUpdatePackages = ('Windows Updates to September via MDT Packages')
	newUpdatePackages = ('')
	
	
	# Set variables for old and new software versions
	
	adobeFlashOld = ('Adobe Flash 11.4.402.265')
	adobeFlashNew = ('Adobe Flash 11.5.502.110')
	
	adobeReaderOld = ('Adobe Reader 10.1.4')
	adobeReaderNew = ('Adobe Reader 11.0')
	
	adobeShockwaveOld =('Adobe Shockwave 11.6.6.636')
	adobeShockwaveNew =('Adobe Shockwave 11.6.8.638')
	
	mcafeeFrameWorkOld = ('McAfee Framework v4.5')
	mcafeeFrameWorkNew = ('McAfee Framework v4.6')
	
	mcafeeAVOld =('McAfee AntiVirus 8.7') 
	mcafeeAVNew =('McAfee AntiVirus 8.8 - Patch 2')
	
	landeskOld = ('LANDesk COR07 Agent v1.3')
	landeskNew = ('LANDesk Agent v1.4')


	#set the paths to the input and extracted files
	oldDocPath = raw_input('Enter the directory to parse:  ')
	listFiles = os.listdir(oldDocPath)
	
	extractDir = ('c:\extract')
	newDocPath = ('{}\newDocs'.format(oldDocPath))
	
	#############################################################################################################################################
	#
	# If the document format or layout hasn't changed DO NOT edit the xml variables set here
	#
	#############################################################################################################################################
	
	
	#set some xml searches and replaces up to edit the unpacked docx file, version and author tables. 
	
	#for the Document Information table
	oldDocumentVersion = ('<w:t>Version</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="6344" w:type="dxa"/></w:tcPr><w:p w14:paraId="50B5BF77" w14:textId="1FD6419E" w:rsidR="006B7E05" w:rsidRDefault="00A74936" w:rsidP="0030048F"><w:pPr><w:pStyle w:val="TableBody"/></w:pPr><w:r><w:t>1.0</w:t></w:r></w:p></w:tc></w:tr><w:tr w:rsidR="006B7E05" w14:paraId="71CFD25C" w14:textId="77777777" w:rsidTr="004E6F9C"><w:tc><w:tcPr><w:tcW w:w="2976" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="17365D" w:themeFill="text2" w:themeFillShade="BF"/></w:tcPr><w:p w14:paraId="6E4BA623" w14:textId="77777777" w:rsidR="006B7E05" w:rsidRPr="004E6F9C" w:rsidRDefault="006B7E05" w:rsidP="00683DBF"><w:pPr><w:pStyle w:val="TableBody"/><w:rPr><w:b/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr></w:pPr><w:r w:rsidRPr="004E6F9C"><w:rPr><w:b/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr><w:t>Authors</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="6344" w:type="dxa"/></w:tcPr><w:p w14:paraId="67318533" w14:textId="3A21D30E" w:rsidR="006B7E05" w:rsidRDefault="006B7E05" w:rsidP="003D63C0"><w:pPr><w:pStyle w:val="TableBody"/></w:pPr></w:p></w:tc></w:tr><w:tr w:rsidR="006B7E05" w14:paraId="3FAA004A" w14:textId="77777777" w:rsidTr="004E6F9C"><w:tc><w:tcPr><w:tcW w:w="2976" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="17365D" w:themeFill="text2" w:themeFillShade="BF"/></w:tcPr><w:p w14:paraId="4CC615A6" w14:textId="77777777" w:rsidR="006B7E05" w:rsidRPr="004E6F9C" w:rsidRDefault="006B7E05" w:rsidP="00683DBF"><w:pPr><w:pStyle w:val="TableBody"/><w:rPr><w:b/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr></w:pPr><w:r w:rsidRPr="004E6F9C"><w:rPr><w:b/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr><w:t>')
	
	newDocumentVersion = ('<w:t>Version</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="6344" w:type="dxa"/></w:tcPr><w:p w14:paraId="50B5BF77" w14:textId="1FD6419E" w:rsidR="006B7E05" w:rsidRDefault="00A74936" w:rsidP="0030048F"><w:pPr><w:pStyle w:val="TableBody"/></w:pPr><w:r><w:t>{}</w:t></w:r></w:p></w:tc></w:tr><w:tr w:rsidR="006B7E05" w14:paraId="71CFD25C" w14:textId="77777777" w:rsidTr="004E6F9C"><w:tc><w:tcPr><w:tcW w:w="2976" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="17365D" w:themeFill="text2" w:themeFillShade="BF"/></w:tcPr><w:p w14:paraId="6E4BA623" w14:textId="77777777" w:rsidR="006B7E05" w:rsidRPr="004E6F9C" w:rsidRDefault="006B7E05" w:rsidP="00683DBF"><w:pPr><w:pStyle w:val="TableBody"/><w:rPr><w:b/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr></w:pPr><w:r w:rsidRPr="004E6F9C"><w:rPr><w:b/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr><w:t>Authors</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="6344" w:type="dxa"/></w:tcPr><w:p w14:paraId="67318533" w14:textId="3A21D30E" w:rsidR="006B7E05" w:rsidRDefault="006B7E05" w:rsidP="003D63C0"><w:pPr><w:pStyle w:val="TableBody"/></w:pPr><w:r><w:t>{} {}</w:t></w:r></w:p></w:tc></w:tr><w:tr w:rsidR="006B7E05" w14:paraId="3FAA004A" w14:textId="77777777" w:rsidTr="004E6F9C"><w:tc><w:tcPr><w:tcW w:w="2976" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="17365D" w:themeFill="text2" w:themeFillShade="BF"/></w:tcPr><w:p w14:paraId="4CC615A6" w14:textId="77777777" w:rsidR="006B7E05" w:rsidRPr="004E6F9C" w:rsidRDefault="006B7E05" w:rsidP="00683DBF"><w:pPr><w:pStyle w:val="TableBody"/><w:rPr><w:b/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr></w:pPr><w:r w:rsidRPr="004E6F9C"><w:rPr><w:b/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr><w:t>'.format(version, authorFirstName, authorLastName))
	
	#for the Revision History table
	oldRevisionHistoryXML = ('<w:t>Version</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="5386" w:type=\"dxa\"/><w:shd w:val=\"clear\" w:color=\"auto\" w:fill="17365D" w:themeFill=\"text2\" w:themeFillShade=\"BF\"/></w:tcPr><w:p w14:paraId="7291966F" w14:textId="77777777" w:rsidR="006B7E05" w:rsidRPr="004E6F9C" w:rsidRDefault="006B7E05" w:rsidP="00CA11DC"><w:pPr><w:pStyle w:val=\"TableBody\"/><w:rPr><w:b/><w:color w:val=\"FFFFFF\" w:themeColor=\"background1\"/></w:rPr></w:pPr><w:r w:rsidRPr="004E6F9C"><w:rPr><w:b/><w:color w:val=\"FFFFFF\" w:themeColor=\"background1\"/></w:rPr><w:t>Summary of Change</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="1666" w:type=\"dxa\"/><w:shd w:val=\"clear\" w:color=\"auto\" w:fill="17365D" w:themeFill=\"text2\" w:themeFillShade=\"BF\"/></w:tcPr><w:p w14:paraId="56450AF2" w14:textId="77777777" w:rsidR="006B7E05" w:rsidRPr="004E6F9C" w:rsidRDefault="006B7E05" w:rsidP="00CA11DC"><w:pPr><w:pStyle w:val=\"TableBody\"/><w:rPr><w:b/><w:color w:val=\"FFFFFF\" w:themeColor=\"background1\"/></w:rPr></w:pPr><w:r w:rsidRPr="004E6F9C"><w:rPr><w:b/><w:color w:val=\"FFFFFF\" w:themeColor=\"background1\"/></w:rPr><w:t>Author</w:t></w:r></w:p></w:tc></w:tr>')
	
	newRevisionHistoryXML = ('<w:t>Version</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w=\"5386\" w:type=\"dxa\"/><w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"17365D\" w:themeFill=\"text2\" w:themeFillShade=\"BF\"/></w:tcPr><w:p w14:paraId=\"7291966F\" w14:textId=\"77777777\" w:rsidR=\"006B7E05\" w:rsidRPr=\"004E6F9C\" w:rsidRDefault=\"006B7E05\" w:rsidP=\"00CA11DC\"><w:pPr><w:pStyle w:val=\"TableBody\"/><w:rPr><w:b/><w:color w:val=\"FFFFFF\" w:themeColor=\"background1\"/></w:rPr></w:pPr><w:r w:rsidRPr=\"004E6F9C\"><w:rPr><w:b/><w:color w:val=\"FFFFFF\" w:themeColor=\"background1\"/></w:rPr><w:t>Summary of Change</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w=\"1666\" w:type=\"dxa\"/><w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"17365D\" w:themeFill=\"text2\" w:themeFillShade=\"BF\"/></w:tcPr><w:p w14:paraId=\"56450AF2\" w14:textId=\"77777777\" w:rsidR=\"006B7E05\" w:rsidRPr=\"004E6F9C\" w:rsidRDefault=\"006B7E05\" w:rsidP=\"00CA11DC\"><w:pPr><w:pStyle w:val=\"TableBody\"/><w:rPr><w:b/><w:color w:val=\"FFFFFF\" w:themeColor=\"background1\"/></w:rPr></w:pPr><w:r w:rsidRPr=\"004E6F9C\"><w:rPr><w:b/><w:color w:val=\"FFFFFF\" w:themeColor=\"background1\"/></w:rPr><w:t>Author</w:t></w:r></w:p></w:tc></w:tr><w:tr w:rsidR=\"006B7E05\" w14:paraId=\"7C7865BD\" w14:textId=\"77777777\" w:rsidTr=\"002910C7\"><w:tc><w:tcPr><w:tcW w:w=\"1275\" w:type=\"dxa\"/></w:tcPr><w:p w14:paraId=\"73A3813A\" w14:textId=\"49D133BD\" w:rsidR=\"006B7E05\" w:rsidRDefault=\"0001446D\" w:rsidP=\"00075B80\"><w:pPr><w:pStyle w:val=\"TableBody\"/></w:pPr><w:r><w:t>{}</w:t></w:r><w:r w:rsidR=\"00AB1F98\"><w:t>/{}</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w=\"993\" w:type=\"dxa\"/></w:tcPr><w:p w14:paraId=\"62A185BB\" w14:textId=\"3B692DCB\" w:rsidR=\"006B7E05\" w:rsidRDefault=\"00AB1F98\" w:rsidP=\"00CA11DC\"><w:pPr><w:pStyle w:val=\"TableBody\"/></w:pPr><w:r><w:t>1.1</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w=\"5386\" w:type=\"dxa\"/></w:tcPr><w:p w14:paraId=\"699433EB\" w14:textId=\"28DEF8B1\" w:rsidR=\"006B7E05\" w:rsidRDefault=\"00A74936\" w:rsidP=\"002910C7\"><w:pPr><w:pStyle w:val=\"TableBody\"/></w:pPr><w:r><w:t xml:space=\"preserve\"> </w:t></w:r><w:r><w:t xml:space=\"preserve\">{}</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w=\"1666\" w:type=\"dxa\"/></w:tcPr><w:p w14:paraId=\"7598A82B\" w14:textId=\"098BA85D\" w:rsidR=\"006B7E05\" w:rsidRDefault=\"00A74936\" w:rsidP=\"00CA11DC\"><w:pPr><w:pStyle w:val=\"TableBody\"/></w:pPr><w:r><w:t xml:space=\"preserve\">{} </w:t></w:r><w:proofErr w:type=\"spellStart\"/><w:r><w:t>{}</w:t></w:r><w:proofErr w:type=\"spellEnd\"/></w:p></w:tc></w:tr>').format(editDate, editYear, updateReason, authorFirstName, authorLastName)
	
	######################################################################################################################
	#
	# Function to edit the files
	#
	######################################################################################################################
	

	for item in listFiles:
		print (item)
		#extract to a given location
		subprocess.call("7za x -o\"{}\" -y \"{}\{}\"".format(extractDir, oldDocPath, item), shell= True)
		
		#read the extracted files into memory and make the replacments	
		with open('{}\word\document.xml'.format(extractDir), 'r') as file:
			
			readFile = file.read()
			
			#edit the Document Information and Revision Histroy
			readFile = readFile.replace(oldDocumentVersion, newDocumentVersion)
			readFile = readFile.replace(oldRevisionHistoryXML, newRevisionHistoryXML)
			
			
			#edit the Source OS information
			
			#catch documents with older 2012 OS captures
			readFile = readFile.replace(oldSourceOS2012, newSourceOS)
			
			#replace all the other OS and package info
			readFile = readFile.replace(oldSourceXP, newSourceXP)
			readFile = readFile.replace(oldSourceOS2013, newSourceOS)
			readFile = readFile.replace(oldUpdatePackages, newUpdatePackages)
			readFile = readFile.replace(oldPatchDay, newPatchDay)
			readFile = readFile.replace(oldPatchDate, newPatchDate)
			
			#hack to remove the th / st from the date 
			readFile = readFile.replace('<w:t>th</w:t>', '')
			
			#edit the software versions
			
			readFile = readFile.replace(adobeFlashOld, adobeFlashNew)
			readFile = readFile.replace(adobeReaderOld, adobeReaderNew)
			readFile = readFile.replace(adobeShockwaveOld, adobeShockwaveNew)
			readFile = readFile.replace(mcafeeFrameWorkOld, mcafeeFrameWorkNew)
			readFile = readFile.replace(mcafeeAVOld, mcafeeAVNew)
			readFile = readFile.replace(landeskOld, landeskNew)
			
			
			#write the files back out
			with open('{}\\word\document.xml'.format(extractDir), 'w') as file:	
			
				(directory, fileName) = os.path.split(oldDocPath)
				file.write(readFile)
				
			#re-archive the files as a docx file in a different location, using the original filename
			subprocess.call("7za a -tzip \"c:/test/newDocs/{}\" \"c:/extract/\*\" ".format(item), shell= True)		
		
		

if __name__ =="__main__":
	main()
