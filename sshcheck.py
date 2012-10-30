#!/usr/bin/env PYTHON

#Script to pull IPs from the /var/log/auth.log.x log files to allow easy identification and blocking
#Tested with Python 2.7 on Ubuntu 12.04
#Michael Pursell 2012

import re



def main():
	
	print("\n****AUTHENTICATION ATTEMPTS SCRIPT****\n")
	print("This script will list the IP addresses found in the /var/log/auth.log by default and output them in a format ready for your hosts.deny file\n") 
	string = raw_input("Please enter 'y' to continue with the default, or 'n' to enter a new filename:  ")

	if string == "y":
		file = open("/var/log/auth.log")
		readfile = file.read()
		search(readfile)
		file.close()
		print("****  List of potential scumbags complete!  ****\n")
	elif string == "n":
		filename = raw_input("Enter a file name:  ")
		file = open(filename)
		readfile = file.read()
		search(readfile)
		file.close()
		print("****  List of potential scumbags complete!  ****\n")
	else:
		print("You must enter either y or n!")


#function to search the passed in readfile for a regex that matches IP addresses
def search(readfile):
        search = re.findall("\d+\.\d+\.\d+.\d+", readfile)
	searchlist = list(set(search)) #turn the list into a set to remove duplicate entries
	searchtotal = len(searchlist)
        
	#set start positions for a couple of variables
	x = 0
	item = searchlist[x]
	
	#increment position in the searchlist while x is below the number of results in the list
	while x < searchtotal: 
		item = searchlist[x]
		
		##If else block to catch known good IPs and print them differently to avoid denying them
		if item == str("0.0.0.0"):
			print("MY IP")
			x = x +1		
		elif item ==str("8.8.8.8"):
			print("GOOGLE DNS")
			x = x+1
		else:
			print("ALL: "+searchlist[x])
			x = x+1
	total = str(searchtotal)
	print("\nThere are "+total+" IPs in the list\n")
	

if __name__=="__main__":
	main()
