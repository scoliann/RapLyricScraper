import os
from selenium import webdriver


def setup():

	# Create twitterHistories folder if it does not already exist
	if not os.path.isdir('scrapedRapLyrics'):
		os.makedirs('scrapedRapLyrics')

def openPage(url):

	# Open webdriver
	driver = webdriver.Chrome()
	driver.get(url)

	# Return driver
	return driver


def scrollToBottom(driver):

	# Scroll down to the bottom of the page
	atBottom = 0
	while True:

		# Get the number of songs before the scroll
		numSongsOnPageBeforeScroll = len(driver.find_elements_by_class_name('song_title'))

		# Scroll down
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Get the number of songs on the screen after the scroll
		numSongsOnPageAfterScroll = len(driver.find_elements_by_class_name('song_title'))

		# Check if the bottom of the page has been reached
		if numSongsOnPageBeforeScroll == numSongsOnPageAfterScroll:
			atBottom += 1

			# If atBottom reaches 100, consider the bottom of the page to be reached
			if atBottom == 100:
				return
		else:
			# If the bottom of the page has not be reached, reset atBottom
			atBottom = 0


def getSongList(driver):

	# Create list of links for songs on page
	allSongs = driver.find_elements_by_class_name(' song_link')
	songList = []
	for song in allSongs:
		songLink = song.get_attribute('href')
		songList.append(songLink)

	# Return song list
	return songList


def getSongLyrics(songList):

	# Create list of links for songs on page
	songList = getSongList(driver)

	# For every song in the list, navigate to the page and get lyrics
	for songLink in songList:

		try:

			# Get the link and navigate to that page
			driver.get(songLink)

			# Get all lyrics for song and save to file
			lyrics = driver.find_elements_by_class_name('referent')
			songTitle = songLink.split('/')[-1]
			text_file = open('scrapedRapLyrics/' + songTitle + '.txt', "a")
			for lyricLine in lyrics:
				cleanedLine = lyricLine.text.encode('ascii', 'ignore')
				text_file.write(cleanedLine + '\n')
			text_file.close()

			# Print progress
			print str(songTitle)

		except:
			continue


if __name__ == "__main__":

	# Create required folders to save tweets
	setup()

	# Open new browser window
	driver = openPage('http://genius.com/tags/rap/all')

	# Scroll to the bottom of the page
	scrollToBottom(driver)

	# Get and save the song lyrics
	getSongLyrics(driver)

 





		
	
