# Tool to create id3 tags for all mp3 files in folder from filename data.
# As of now fails when proper song title contains underscores and numbers.

# TODO:
# Check for multiple word names of artist and album
# Make genre-tagging work

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os
import sys
import re

songfiles = []
albumname_matches = 0
artistname_matches = 0
album_words = 0
artist_words = 0
tag_year = False
tag_genre = False

#print EasyID3.valid_keys.keys() # prints all valid tags that can be edited with EasyID3

if not len(sys.argv) == 2:
	sys.exit("You must execute the script with 1 command line argument, containing the path to the folder containing mp3 files.\n"
		+ "Example: python mp3tagfixer.py /home/<username>/music/<artistname>/<albumname>")

# User input:

print 'Welcome to mp3 tag fixer.\n'
file_path = sys.argv[1]
artist = raw_input('name of artist: ')
album = raw_input('name of album: ')
year = raw_input('year of release (optional): ')
genre = raw_input('genre of album (optional): ')

# Exit if user did not provide artist or album names

if artist is "" or album is "":
	sys.exit("You must provide artist and album name. Script ending.")

# count words in album and artist name

album_words = len(re.findall(r'\w+', album))
artist_words = len(re.findall(r'\w+', artist))

# Check if user inputtet genre and year
if year is not "":
	tag_year = True
if genre is not "":
	tag_genre = True

# Find all mp3 files in dir and sort them by filename.
# TODO: Replace ugly flags using count
for root, dirs, files in os.walk(file_path):
	for file in files:
		if file.endswith(".mp3"):
			album_match_found = False # flags used to identify is matches already found (ugly, but works)
			artist_match_found = False
			songfiles.append(file)
			if album.upper().lower() in file.upper().lower(): # checks if 
				albumname_matches += 1
				album_match_found = True
			temp_album = album.replace(' ','_')
			#print "checking if album name in format: " + temp_album.upper().lower() + " is in " + file.upper().lower()
			if not album_match_found:
				if temp_album.upper().lower() in file.upper().lower():
					albumname_matches += 1
			if artist.upper().lower() in file.upper().lower():
				artistname_matches += 1
				artist_match_found = True
			temp_artist = artist.replace(' ','_')
			#print "checking if artist name in format: " + temp_artist.upper().lower() + " is in " + file.upper().lower()
			if not artist_match_found:
				if temp_artist.upper().lower() in file.upper().lower():
					artistname_matches += 1


songfiles.sort()

print "artistname_matches: " + str(artistname_matches) + ", albumname_matches: " + str(albumname_matches) + ", artist_words: " + str(artist_words) + ", album_words: " + str(album_words) 

# Different implementations to be tested. Maybe to be chosen with command line argument?

# First implementation splits string by spaces & underscores,
# so it fails if there is no space or underscore between words or numbers.

for song in songfiles:
	audio = MP3(file_path + "/" + song, ID3=EasyID3)
	title_str = ""
	word_count = 0;

	# song_parts = re.split("\W+|_", song) # splits http://stackoverflow.com/questions/1059559/python-split-strings-with-multiple-delimiters
	song_parts = song.replace('_',' ').split() # split strings with underscore and space as delimeter
	for part in song_parts:
		number_ok = True
		if part.startswith(tuple('0123456789')): # determine if part of string is track number of something else to be discarded
			for x in part:
				if not x.isdigit():
					number_ok = False
			if number_ok:
				if len(part) > 2:
					continue
				else:
					# SET TRACK NO TO part
					audio["tracknumber"] = part
		else: # parse part of string that is not a number and decide what to do with it
			word = ""
			word_count += 1
			if 'mp3' in part: # check if part contains suffix, if so remove it.
				idx = part.find('.mp3')
				word = part[:idx]
			else:
				word = part 
			if albumname_matches > 0: # check if word is artist or album name in filename. If so, discard.
				if word.upper().lower() == album.upper().lower():
					continue
				if album_words > 1:
					print "checking if word " + word.upper().lower() + " is in album name " + album.upper().lower()
					if word.upper().lower() in album.upper().lower():
						print "found that word " + word + " is in album name, and should be discarded"
						continue

			if artistname_matches > 0:
				if word.upper().lower() == artist.upper().lower():
					continue
				if artist_words > 1:
					print "checking if word " + word.upper().lower() + " is in artist name " + artist.upper().lower()
					if word.upper().lower() in artist.upper().lower():
						continue
			# append word to title title string if appropriate
			if word_count > 1:
				title_str = title_str + " " + word.title()
			else:
				title_str = title_str + word.title()

	# add tags to file and save
	audio["artist"] = u"" + artist
	audio["album"] = u"" + album
	audio["title"] = u"" + title_str
	if tag_genre:
		audio["genre"] = genre
	if tag_year:
		audio["date"] = year
	audio.save(v1=2)
	audio.save()

sys.exit("Done editing files. Please check files for errors and correct if necessary.")