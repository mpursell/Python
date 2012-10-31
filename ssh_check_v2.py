#!/usr/bin/env PYTHON

#Script to pull IPs from the /var/log/auth.log.x log files to allow easy identification and blocking
#Tested with Python 2.7 on Ubuntu 12.04
#Amended from sshcheck.py to only output ALL: CIDR BLOCK ready for the hosts.deny file.
#This version of the script will ONLY identify those IPs in the auth.log that have route: information in the WHOIS output.  All other IPs are ignored. 
#Michael Pursell 2012

import re, sys 
from subprocess import call, check_output
from os import environ

def main():
	
	usr = environ['HOME']
	print("\n****AUTHENTICATION LOG FILE PARSER****\n")
	print("This script look up IPs found in the /var/log/auth.log file and run a WHOIS lookup \nto find the CIDR block.  It will then attmept to output them in a format ready for the hosts.deny file\nOutput can be found in the {}/ssh_check.log file\n".format(usr)) 
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
        addresses = re.findall("\d+\.\d+\.\d+\.\d+", readfile)
	addr_list = set(addresses) #turn the list into a set to remove duplicate entries
	addr_total = len(addr_list)
	usr = environ['HOME']	
	
	with open("{}/ssh_check.log".format(usr),'w')as log:


		#iterate over the searchlist set
		for addr in addr_list:

			#use check output to search WHOIS output line by line for the CIDR block
			route = ''.join(line for line in check_output(["whois", addr]).splitlines(True)if "route: " in line)
			
			#if else block to iterate over searches for route that come up blank
			if route == '':
				continue
			else:
				#define regex searches for the ip and CIDR block
				ip = '.'.join(re.findall("\d+\.\d+\.\d+\.\d+", route))
				cidr = ''.join(re.findall("\/\d\d\s", route))
				print("\nALL: {}{}".format(ip, cidr))
				
				#if else to catch 'good' ip blocks and skip writing them to the log file
				if ip != '0.0.0.0':	#ENTER GOOD IP BLOCKS HERE
					log.write("ALL: {}{}".format(ip, cidr))
				else:
					continue
	
	
if __name__=="__main__":
	main()

