import sys

import vocals
import music
import graphics

artist = sys.argv[1]

original_lyrics, symbol_lyrics = vocals.get_lyric_strings(artist)

Ticker = graphics.TickerView(original_lyrics, symbol_lyrics)
Ticker.run()

if __name__ == '__main__':
