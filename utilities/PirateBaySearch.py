#! /usr/bin/env python

# Script to read in torrent search titles from a text file,
# search the PirateBay for the titles, grab the first* magnet links for each title
# start the torrent using transmission-remote.
# optional last function removes and replaces the input text file with a blank one - 
# useful if the script runs regularly as a cron job (prevents repeat downloads of the torrents).  Read-write access will be needed to the path if this function is used. 

# *the script literally grabs the first magnet link that matches the search term, it 	
# makes no effort to check for seeders / leechers etc. 

# script requires your input file path and transmission creds.

# each line in the input file will be read in as a new search term. 

# torrents will be downloaded to the download directory set in your transmission client

# tested on Raspbian and Python 2.7 

# requires transmission-remote and Python mechanize.  

import mechanize, subprocess, os
from sys import argv

# **** SET THESE VARIABLES ****
textFilePath = ''
transmissionUser = ''
transmissionPass = ''
PirateBayAddress = ''


def PirateBaySearch(inputList[]):

# function provides the browser operations required to search the Pirate Bay

	# set some variables we know we'll need
	urlPrefix = PirateBayAddress

	# try block to catch argv errors from not entering a search term at the command line
	try:
		
		# list to hold our magnet links
		finalLinks = []
		
		
		
		# loop through all our search terms in the list provided as an argument
		for argument in range(0,len(inputList)): 
			#list to hold search results
			results = []
			
			search = inputList[argument]
			

			# some output to pretty it up if running the script manually
			# OPTIONAL
			#print '\n\nSearching for: {}\n----------------\n'.format(search)
			
			# create the browser object
			browser = mechanize.Browser()

			# ignore the robots.txt file and pass a user-agent string that imitates Chrome
			browser.set_handle_robots(False)
			browser.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36')]
			browser.open("http://thepiratebeach.eu")


			# grab the form.  nr=0 means number 0, i.e the first form on the page
			browser.select_form(nr=0)

			# put our terms into the search form and submit it	
			browser.form['q'] = search
			response = browser.submit()
			
			

			# get the links back from the submission and append them to the list 
			# after checking that our search term appears somewhere in the link text
			for link in browser.links():
				# check for the first characters of search in the link text 
				if search in link.text:
					results.append((link))
					#print link.text, link.url
			
			
			# # we'll only try to follow the results of the search if
			# # we have something in our results list.  
			# for result in results:
				# if not result:
					# results.remove(result)
			
				# grab the first link out of our results set
				followedLink = browser.follow_link(results[0])
				
				# get the url of the link object, then open a browser to that link		
				browser.open(followedLink.geturl())
				
				# find the magnet link from a list of links
				for link in browser.links():
					if link.url != None:
						if 'magnet' in link.url:
							finalLinks.append(link.url)
						
							# some output to pretty it up if running the script manually
							# OPTIONAL
							#print link.url
		
			else:
				continue
				
				
		
		
		return finalLinks	
		
				
	except IndexError:
		pass
	
		# some output to pretty it up if running the script manually
		# OPTIONAL
		#print '\n\nYou need to enter a term to search the Pirate Bay.'
	
	
		
def Transmission(urlList):

# function shells out the commands to transmission-remote to add the magent links
	
	for magnetUrl in urlList:
		if magnetUrl != None:
			subprocess.call('transmission-remote -n {}:{} -a {}'.format(tranmissionUser, transmissionPass, magnetUrl), shell=True)
	else:
		continue

		

		
def ReadFile():
	
# function reads the input file

	inputList = []
	
	try:
		os.path.exists(textFilePath)
		
		with open(textFilePath) as inputFile:
			inputLines = inputFile.read().splitlines()
			
			for line in inputLines:
				inputList.append(line)
						
			
		return inputList
		
	except IOError:
		print 'Input file "{}" was not found.  Check the path and permissions. \nExiting'.format(textFilePath)
		exit()
	except TypeError:
		pass
	

def ReplaceFile():

# function removes the input file, then replaces it with a blank one

	subprocess.call("rm {}".format(textFilePath), shell=True)
	subprocess.call('touch {}'.format(textFilePath), shell=True)


def main():

	Transmission(PirateBaySearch(ReadFile()))
	ReplaceFile()

if __name__=="__main__":
	main()










