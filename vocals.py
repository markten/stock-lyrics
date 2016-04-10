import os
from tswift import Artist
import random
import csv
import wave
import subprocess
from fuzzywuzzy import fuzz

TIME_FILE = 'timefile.txt'
ESPEAK = 'C:\Program Files (x86)\eSpeak\command_line\espeak.exe'
SYMBOL_FILE = './symbols.csv'

def fetch_lyrics(artist_name):

	artist = Artist(artist_name)
	artist.load()
	song = random.choice(artist.songs)
	song.load()

	original_lyrics = song.lyrics

	#print "### ORIGINAL LYRICS ###\n"
	#print original_lyrics
	#print "#######################\n\n\n"

	return original_lyrics

def load_symbols(symbol_file):

	symbols = []
	companies = []

	with open(symbol_file, 'rb') as symbol_file:
		reader = csv.reader(symbol_file, delimiter=',')

		for row in reader:
			symbols.append(row[0])
			companies.append(row[1])

	#print symbols
	return symbols


def match_symbol(word, symbols):

	max_distance = 0
	max_index = None

	word.lower()

	for index, symbol in enumerate(symbols):
		distance = fuzz.token_sort_ratio(word, symbol)

		if distance > max_distance:
			max_distance = distance
			max_index = index
		#print distance, symbol

	if max_index:
		return symbols[max_index]
	else:
		print "BAD: [" + word +"]"
		return None


def generate_symbol_lyrics(original_lyrics, symbols):

	symbols = load_symbols(SYMBOL_FILE)

	symbol_lyrics = ''

	for line in original_lyrics.split('\n'):
		words = line.split()

		for word in words:
			symbol = match_symbol(word, symbols)
			if symbol:
				symbol_lyrics = symbol_lyrics + ' ' + symbol

		symbol_lyrics += '\n'

	#print "#### SYMBOL LYRICS ####\n"
	#print symbol_lyrics
	#print "#######################\n\n\n"

	return symbol_lyrics

def get_lyric_strings(artist):

	original_lyrics_flat = ''
	symbol_lyrics_flat = ''

	original_lyrics = fetch_lyrics(artist)
	symbols = load_symbols(SYMBOL_FILE)

	symbol_lyrics = generate_symbol_lyrics(original_lyrics, symbols)

	for word in original_lyrics.split():
		original_lyrics_flat += (word + ' ')

	for word in symbol_lyrics.split():
		symbol_lyrics_flat += (word + ' ')

	return original_lyrics_flat, symbol_lyrics_flat

def generate_vocal_files(artist):

	symbol_lyrics = generate_symbol_lyrics(artist)

	total_time = 0

	audio_file = wave.open('audiofile', 'w')

	for index, word in enumerate(symbol_lyrics.split()):

		# Generate wav files for each word
		filename = str(index)+'.wav'
		subprocess.call([ESPEAK, '-w', filename, word])

		with open(TIME_FILE, 'a') as time_file:
			time_file.writelines(str(total_time))

		# Find length in seconds of each word and append sound data to output file
		wav_file = wave.open(filename, 'r')
		num_frames = wav_file.getnframes()
		fs = wav_file.getframerate()
		word_time = num_frames / float(fs)

		if index == 0:
			audio_file.setparams(wav_file.getparams())
		audio_file.writeframes(wav_file.readframes(num_frames))

		wav_file.close()
		os.remove(filename)

		total_time += word_time

	audio_file.close()
