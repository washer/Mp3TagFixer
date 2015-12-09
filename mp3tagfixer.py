# Tool to create id3 tags for all mp3 files in folder from filename data.

# TODO:
# file names should be split only by spaces and underscores

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os
import sys
import re

songfiles = []
albumname_matches = 0
artistname_matches = 0
tag_year = False;
tag_genre = False;

#print EasyID3.valid_keys.keys() # prints all valid tags that can be edited with EasyID3

if not len(sys.argv) == 2:
	sys.exit("You must execute the script with 1 command line argument, containing the path to the folder containing mp3 files.\n"
		+ "Example: python mp3tagfixer.py /home/<username>/music/<artistname>/<albumname>")


print 'Welcome to mp3 tag fixer.\n'
file_path = sys.argv[1]
artist = raw_input('name of artist: ')
album = raw_input('name of album: ')
year = raw_input('year of release (optional): ')
genre = raw_input('genre of album (optional): ')

if artist is "" or album is "":
	sys.exit("You must provide artist and album name. Script ending.")

if year is not "":
	tag_year = True
if genre is not "":
	tag_genre = True

for root, dirs, files in os.walk(file_path):
	for file in files:
		if file.endswith(".mp3"):
			songfiles.append(file)
			if album.upper().lower() in file.upper().lower():
				albumname_matches += 1
			if artist.upper().lower() in file.upper().lower():
				artistname_matches += 1

songfiles.sort()

# Different implementations to be tested. Maybe to be chosen with command line argument?

# First implementation splits string by spaces & underscores,
# so it fails if there is no space or underscore between words or numbers.

for song in songfiles:
	audio = MP3(file_path + "/" + song, ID3=EasyID3)
	title_str = ""
	word_count = 0;

	# change splitting so that it only splits on spaces and underscores
	song_parts = re.split("\W+|_", song) # splits http://stackoverflow.com/questions/1059559/python-split-strings-with-multiple-delimiters
	for part in song_parts:
		number_ok = True
		if part.startswith(tuple('0123456789')): 
			for x in part:
				if not x.isdigit():
					number_ok = False
			if number_ok:
				if len(part) > 2:
					continue
				else:
					# SET TRACK NO TO part
					audio["tracknumber"] = part
		else:
			word = ""
			word_count += 1
			if 'mp3' in part:
				idx = part.find('mp3')
				word = part[:idx]
			else:
				word = part
			if albumname_matches > 1:
				if part.upper().lower() == album.upper().lower():
					continue
			if artistname_matches > 1:
				if part.upper().lower() == artist.upper().lower():
					continue
			if word_count > 1:
				title_str = title_str + " " + word.title()
			else:
				title_str = title_str + word.title()

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