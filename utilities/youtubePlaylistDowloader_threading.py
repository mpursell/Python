# Get the list of vids in a youtube playlist and download them with youtube-dl
# First efforts at threading / async execution

# plug the inital playlist url into the initialUrl variable and your Google API auth key into authKey

#! /usr/bin/env python

import subprocess, urllib2, threading


exeLocation = ''
authKey = ''
initialUrl = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=PLUl4u3cNGP62K2DjQLRxDNRi0z2IRWnNh&key='.format(authKey)
videoList = []

	
def browser(url):

	# open the initial playlist url
	responseJson = urllib2.urlopen(url)
	
	for result in responseJson:
	
		# get the nextPageToken so that we can add it to the tokenised url and get the next pages of the
		# playlist 
		if 'nextPageToken' in result:
			#print result[19:][:6]
			
			# trim the result - it comes back as "nextPageToken : {token number}"
			# as we're only interested in the number we want to trim the string
			token = result[19:][:6]
			
			# add our next page token to the playlist URL
			tokenisedUrl = 'https://www.googleapis.com/youtube/v3/playlistItems?pageToken={}&part=snippet&playlistId=PLUl4u3cNGP62K2DjQLRxDNRi0z2IRWnNh&key={}'.format(token, authKey)
			
			# call browser() recursively to use all our next page tokens and get video id results
			# for all pages
			browser_t = threading.Thread(browser(tokenisedUrl))
			browser_t.start()
			
			# non-threaded execution for testing
			#browser(tokenisedUrl)
			
		if 'videoId' in result:
			#print result[17:][:11]
			videoId = result[17:][:11]
			videoList.append('https://www.youtube.com/watch?v={}'.format(videoId))
	
	
def main():

	(browser(initialUrl))
	
	try:
		for video in videoList:
			print video
			t = threading.Thread(subprocess.call('{} {}'.format(exeLocation, video)))
			#t = threading.Thread(print ('{} {}').format(exeLocation, video))
			t.start()
			
	except IOError:
		print "Check the location of the youtube-dl executable"
	
		
	

if __name__=="__main__":
	main()


