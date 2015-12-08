# Tool to create id3 tags for all mp3 files in folder from filename data.

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os
import sys

if not len(sys.argv) == 2:
	sys.exit("You must execute the script with 1 command line argument, containing the path to the folder containing mp3 files.\n"
		+ "Example: python mp3tagfixer.py /home/<username>/music/<artistname>/<albumname>")


print 'Welcome to mp3 tag fixer.\n'
file_path = sys.argv[1]
artist = raw_input('name of artist: ')
album = raw_input('name of album: ')
year = raw_input('year of release (optional')
songfiles = []

#print album + ', by ' + artist

#for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
for root, dirs, files in os.walk(file_path):
	for file in files:
		if file.endswith(".mp3"):
			songfiles.append(file)

songfiles.sort()
#print songfiles

# Different implementations to be tested. Maybe to be chosen with command line argument?

# First implementation splits string by spaces, so fails if there is no space between words or numbers.
# Alo as of now cannot handle if string also contains album or artist name

for song in songfiles:
	audio = MP3(song, ID3=EasyID3)
	#audio.pprint()
	title_str = ""
	word_count = 0;

	song_parts = song.split()
	#print song_parts
	for part in song_parts:
		number_ok = True
		
		if part.startswith(tuple('0123456789')): 
			for x in part:
				if not x.isdigit():
					number_ok = False
			if number_ok:
				# SET TRACK NO TO part
				audio["tracknumber"] = part
		else:
			word = ""
			word_count += 1
			if 'mp3' in part:
				idx = part.find('.mp3')
				word = part[:idx]
			else:
				word = part

			if word_count > 1:
				title_str = title_str + " " + word.title()
			else:
				title_str = title_str + word.title()

	audio["artist"] = u"" + artist
	audio["album"] = u"" + album
	audio["title"] = u"" + title_str
	audio.save()
	print artist + ", " + album + ", " + title_str

		#if part == album or part == artist: FIND A WAY TO CHECK IF ALL SONGS CONTAIN SAME TEXT - maybe loop and count?
			#song_parts.remove(part)



# Pain in the ass safety mode,

#for song in songfiles:
	#if(song.startswith(tuple('0123456789'))):
	#	for i in range (0, len(song)):
		#	if(!song[i].isdigit()):

		#	if(song[i] != )

print "Done editing files. Please check files for errors and correct if necessary."