# stock-lyrics
This program makes a simple ticker display of song lyrics. The original lyrics are displayed above a set of lyrics made by matching each word with the closest symbol on the NYSE or NASDAQ.

This program was created during Bitcamp 2016 at UMD.

![screenshot](http://i.imgur.com/ReNNTkS.png)

## Requirements
This program runs with Python 2.7

If you have pip installed, you may install the required modules with

```Python
  pip install -r requirements.text
```

Pygame will likely require that you seek out a binary or refer to your distribution's package manager.

## Usage

Simply run the script with python. Supply and artist name in all lowercase letters with hyphens in place of spaces.

```python
python ./stock-lyrics.py <artist-name>
```

To run a test case for the graphics that doesn't pull lyrics.
```python
python ./stock-lyrics.py -t
```
