import sys

import lyrics
import graphics

if __name__ == '__main__':
	artist = sys.argv[1]

	if artist == '-t':
		original_lyrics = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST '
		symbol_lyrics = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST '
		song_title = 'Test Song'
		song_artist = 'Test Artist'
	else:
		song_title, song_artist, song_lyrics = lyrics.fetch_artist_song(artist)
		original_lyrics, symbol_lyrics = lyrics.get_lyric_strings(song_lyrics)

	Ticker = graphics.TickerView(original_lyrics, symbol_lyrics, song_title, song_artist)
	Ticker.run()
