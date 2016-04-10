import os, sys, string
from tswift import Artist
import random
import csv
from fuzzywuzzy import fuzz

SYMBOL_FILE = './symbols.csv'

def fetch_artist_song(artist_name):
	try:
		artist = Artist(artist_name)
		artist.load()
		song = random.choice(artist.songs)
		song.load()

		return song._title, artist_name, song.lyrics
	except:
		print "Unable to find artist. Please enter artist name in lowercase with hyphens to denote spaces."
		sys.exit(1)

def load_symbols(symbol_file):

	symbols = []
	companies = []

	with open(symbol_file, 'rb') as symbol_file:
		reader = csv.reader(symbol_file, delimiter=',')

		for row in reader:
			symbols.append(row[0])
			companies.append(row[1])

	return symbols

def match_symbol(word, symbols):

	max_distance = 0
	max_index = None

	for index, symbol in enumerate(symbols):
		distance = fuzz.token_sort_ratio(word, symbol)

		if distance > max_distance:
			max_distance = distance
			max_index = index

	if max_index:
		return symbols[max_index]
	else:
		return None

def generate_symbol_lyrics(original_lyrics, symbols):

	symbols = load_symbols(SYMBOL_FILE)

	symbol_lyrics = ''

	original_lyrics = original_lyrics.translate(string.maketrans("",""), string.punctuation)

	for line in original_lyrics.split('\n'):
		words = line.split()

		for word in words:
			symbol = match_symbol(word, symbols)
			if symbol:
				symbol_lyrics = symbol_lyrics + ' ' + symbol

		symbol_lyrics += '\n'

	return symbol_lyrics

def get_lyric_strings(original_lyrics):

	print "Getting lyric strings..."

	original_lyrics_clean = ''
	symbol_lyrics_clean = ''

	print "\tloading symbols..."
	symbols = load_symbols(SYMBOL_FILE)

	print "\tgenerating symbol lyrics (long wait)..."
	symbol_lyrics = generate_symbol_lyrics(original_lyrics, symbols)

	print "\tcleaning strings..."
	for word in original_lyrics.split():
		original_lyrics_clean += (word + ' ')

	for word in symbol_lyrics.split():
		symbol_lyrics_clean += (word + ' ')

	original_lyrics_clean = original_lyrics_clean.upper()
	symbol_lyrics_clean = symbol_lyrics_clean.upper()

	print "Done."

	return original_lyrics_clean, symbol_lyrics_clean
