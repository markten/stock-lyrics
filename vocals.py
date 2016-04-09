from tswift import Artist
import random
import csv
from gtts import gTTS
from fuzzywuzzy import fuzz

def fetch_lyrics(artist_name):
	
	artist = Artist(artist_name)
	artist.load()
	song = random.choice(artist.songs)
	song.load()
	print song.lyrics
	
	return song.lyrics.split()
	
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
		return ''
			
	
def generate_symbol_lyrics(artist):
	
	symbols = load_symbols('./symbols.csv')
	lyrics = fetch_lyrics(artist)
	
	symbol_lyrics = ''
	
	for word in lyrics:
		symbol_lyrics = symbol_lyrics + ' ' + match_symbol(word, symbols)
		
	print symbol_lyrics
		
	return symbol_lyrics
	
def generate_vocals_file(artist):
	
	symbol_lyrics = generate_symbol_lyrics(artist)
	tts = gTTS(text=symbol_lyrics, lang='en')
	tts.save("test.mp3")
	
