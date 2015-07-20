#! /usr/bin/python

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
from bs4 import BeautifulSoup

# SET THESE VARIABLES

textFilePath = ''
transmissionUser = ''
transmissionPass = ''
pirateBayAddress = ''

# global list 
searchTermsToRetry = []


def PirateBaySearch(inputList):


	# try block to catch argv errors from not entering a search term at the command line
	try:
		
		# list to hold our magnet links
		finalLinks = []

		# loop through all our search terms that we present as command line
		# parameters
		for argument in range(0,len(inputList)): 
			search = inputList[argument]
			
			results = []		
			

			# some output to pretty it up if running the script manually
			# OPTIONAL
			print '\n\nSearching for: {}\n----------------\n'.format(search)
			
			# create the browser object
			browser = mechanize.Browser()

			# ignore the robots.txt file and pass a user-agent string that imitates a real browser
			browser.set_handle_robots(False)
			browser.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36')]
			browser.open(pirateBayAddress)


			# grab the form	nr=0 means number 0, i.e the first form on the page
			browser.select_form(nr=0)

			# put our terms into the search form and submit it	
			# double quotes around the search string are necessary to 
			# prevent thePirateBay from returning links of similar, but not
			# identical name. 
			browser.form['q'] = "\"" + search + "\""
			response = browser.submit()
			data = response.get_data()
				
			# use BeautifulSoup to find when no results are found
			# uses the text "0 found" in the h2 tags on the results page.
			soup = BeautifulSoup(data, "html.parser")
			h2 = soup.find('h2')
			
			for i in h2:
				if '0 found' in i:
					# if there are 0 results found, append it to a list for
					# use in the replaceFile function.

					searchTermsToRetry.append(search)
				else:
					continue
	
			# get the links back from the submission and append them to the list 
			# after checking that our search term appears somewhere in the link text
			
			for link in browser.links():

				if search in link.text:
					results.append((link))
					#print link.text, link.url
				else:
					continue
	
				# grab the first link out of our results set
				followedLink = browser.follow_link(results[0])

				# get the url of the link object, then open a browser to that link		
				browser.open(followedLink.geturl())
			
				# find the magnet link from a list of links
				for link in browser.links():
					if link.url != '':
						if 'magnet' in link.url:
							print link.url
							finalLinks.append(link.url)
						else:
							continue
		
		
		return finalLinks
		
		
				
	except IndexError, TypeError:
		
		pass	
		# some output to pretty it up if running the script manually
			# OPTIONAL
		#print '\n\nYou need to enter a term to search the Pirate Bay.\n\nScript should be used as such: \n\npython scriptname.py "search term"'
	
	
		
def Transmission(urlList):

# function takes a list of magnet urls and runs transmission-remote to add the trackers	
	try:
		for magnetUrl in urlList:
			if magnetUrl != None:
				subprocess.call('transmission-remote -n {}:{} -a {}'.format(transmissionUser, transmissionPass, magnetUrl), shell=True)
	except TypeError:
		
		pass
		
def readFile():
	
# function reads the list of search items in the text file. 	
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
	
def replaceFile(listOfTermsToRetry):

# function removes the input file, then replaces it with a blank one

	for i in listOfTermsToRetry:
		print 'Retrying: {}'.format(i)

	subprocess.call("rm {}".format(textFilePath), shell=True)
	subprocess.call('touch {}'.format(textFilePath), shell=True)	
	
	with open(textFilePath, 'w') as torrentFile:
		for retryItem in listOfTermsToRetry:
			torrentFile.write(retryItem +"\r\n")


def main():

	Transmission(PirateBaySearch(readFile()))
	replaceFile(searchTermsToRetry)

if __name__=="__main__":
	main()

















