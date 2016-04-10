import os
from tswift import Artist
import random
import csv
from fuzzywuzzy import fuzz

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
