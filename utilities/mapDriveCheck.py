#!/usr/ENV PYTHON

# Script to check for existence of a directory on remote shares.
# If the directory exists, provide an option to remove it. 
# Michael Pursell 2014

import os, subprocess


def main():

	prompt = raw_input("Enter a directory name to search for: ")
	captureFolder = "\\" + prompt #add the escaped slash to the folder name
	shareList = ["","",""] #list of arbitrary share names

	
	for share in shareList:
		pathCheck(share, captureFolder) #check the path's existence, map the drive and offer a prompt to delete if it does exist. 
	
		subprocess.call("net use x: /d /YES", shell=True, stdout=subprocess.PIPE) #clean up mapped drive after each iteration over the share list so the drive letter is available again
		
		
		
		
def pathCheck(sharename, folder):


	if sharename == "": #check which share name we're dealing with
		user = "" #provide appropriate credentials for mapping a drive
		passwd = ""
		path = '"\\\\<path without leading slashes>"' #path that corresponds to this share name for the drive mapping
		
		mapDrive(path, user, passwd, sharename, folder) #call mapDrive to set up the mapping
				
	elif sharename == "":
		user = ""
		passwd = ""
		path = '"\\\\<path without leading slashes>"'
		
		mapDrive(path, user, passwd, sharename, folder)
		
	else:
		print("Share not recognised")

		
def mapDrive(pathToMap, credUser, credPass, nameOfShare, dir):		
	try:
		subprocess.call("net use x: {} {} /user:{}".format(pathToMap, credPass, credUser), shell=True, stdout=subprocess.PIPE) #map the drive, suppressing output
	except:
		print("Can't map drive to {}\n".format(nameOfShare))
		
	if os.path.exists('x:\\'+ dir):
		print(nameOfShare + " exists") 
		pathRemove(nameOfShare, dir) #if the folder exists, give the option to remove it by calling pathRemove
	else:
		print(nameOfShare + " doesn't exist")
		
		
		
		
def pathRemove(namedShare, directory):

	confirm = raw_input('Do you want to remove {} from {}? (y/n):  '.format(directory, namedShare))
	
	if confirm == 'y':
		subprocess.call('rmdir /S /Q x:\\{}'.format(directory),shell=True, stdout=subprocess.PIPE)
		print('Removed')
	else:
		print('')
			
		
		
if __name__ == "__main__":
	main()
