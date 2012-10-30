#!/usr/bin/env PYTHON

#Script to pull IPs from the /var/log/auth.log.x log files to allow easy identification and blocking
#Tested with Python 2.7 on Ubuntu 12.04
#Michael Pursell 2012

import re, sys 
from subprocess import call

def main():
	
	print("\n****AUTHENTICATION LOG FILE PARSER****\n")
	print("This script will list the IP addresses found in the /var/log/auth.log output them in a format ready for the hosts.deny file\n") 
	question = raw_input("Please enter 'y' to continue with the default, or 'n' to enter a new filename:  ")

	if question == "y":
		with open('/var/log/auth.log') as file:
			readfile = file.read()
			search(readfile)
		print("****  List of potential scumbags complete!  ****\n")
	elif question == "n":
		filename = raw_input("Enter a file name:  ")
		with open(filename) as file:
			readfile = file.read()
			search(readfile)
		print("****  List of potential scumbags complete!  ****\n")
	else:
		print("You must enter either y or n!")
		sys.exit()


#function to search the passed in readfile for a regex that matches IP addresses
def search(readfile):
        search = re.findall("\d+\.\d+\.\d+.\d+", readfile)
	searchlist = set(search) #turn the list into a set to remove duplicate entries
	searchtotal = len(searchlist)	

	#iterate over the searchlist set
	for item in searchlist:
		
		#If else block to catch known good IPs and print them differently to avoid denying them
		if item == "0.0.0.0" or item == "8.8.8.8":
			continue
		else:
			print("\nALL: {} ".format(item)) #outputs in the right format for hosts.deny
			country = call("whois "+item+" |grep country", shell=True)#find the country from WHOIS if poss
			route = call("whois "+item+"|grep route: ", shell = True)#find the CIDR block is poss
			print("\n-----------------------------------------------------------")
		

	
	print("\nThere are {} IPs in the list\n".format(searchtotal))

	

if __name__=="__main__":
	main()
