#Script to open docx files, replace given software versions, and re-package the docx file.
#Requires the 7za command line tool in the Python directory
#Tested on Windows 7 with Python 2.7
#Michael Pursell 2013


import os, subprocess


def main():

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

	for item in listFiles:
		print (item)
		#extract to a given location
		subprocess.call("7za x -o\"{}\" -y \"{}\{}\"".format(extractDir, oldDocPath, item), shell= True)
		
		#read the extracted files into memory and do the replacments	
		with open('{}\word\document.xml'.format(extractDir), 'r') as file:
			
			readFile = file.read()
			
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
