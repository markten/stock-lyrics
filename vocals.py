import os
from tswift import Artist
import random
import csv
import wave
import subprocess
from fuzzywuzzy import fuzz

TIME_FILE = 'timefile.txt'

def fetch_lyrics(artist_name):
	
	artist = Artist(artist_name)
	artist.load()
	song = random.choice(artist.songs)
	song.load()
	print song.lyrics
	
	return song.lyrics.split('\n')
	
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
		return ''
			
	
def generate_symbol_lyrics(artist):
	
	symbols = load_symbols('./symbols.csv')
	lyrics = fetch_lyrics(artist)
	
	symbol_lyrics = ''
	
	for line in lyrics:
		words = line.split()
		
		for word in words:
			
			symbol = match_symbol(word, symbols)
			
			if word:
				symbol_lyrics = symbol_lyrics + ' ' + symbol
		
		symbol_lyrics += '\n'
		
	print symbol_lyrics
		
	return symbol_lyrics

def generate_vocal_files(artist):
	
	symbol_lyrics = generate_symbol_lyrics(artist)
	
	total_time = 0
	
	audio_file = wave.open('audiofile.wav', 'w')
	
	for index, word in enumerate(symbol_lyrics.split()):
		
		# Generate wav files for each word
		filename = str(index)+'.wav'
		subprocess.call(['espeak', '-w', filename, word])
		
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
		
		os.remove(filename)
		
		total_time += word_time
		
	audio_file.close()
			
			
		
		
	
