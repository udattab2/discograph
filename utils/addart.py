import json
import urllib.parse
import urllib.request
import sqlite3
from utils.helper import clear_screen
import utils.setcount as setcount
import os

API_KEY = '5047c0ecb7625ed2dd03f1c35845d35a'
MUSICGRAPH_BASE = 'http://api.musicgraph.com/api/v2'
LYRIC_API_BASE = 'http://lyric-api.herokuapp.com/api/find/'

def fetch_artist_genre(artname):
	"""
	Fetches the main genre of an artist using the MusicGraph API.

	Args:
		artname (str): The name of the artist to search for.

	Returns:
		str or None: The main genre of the artist if found, otherwise None.

	Raises:
		URLError: If there is a problem with the network request.
		JSONDecodeError: If the response cannot be decoded as JSON.

	Note:
		Requires the global variables MUSICGRAPH_BASE and API_KEY to be defined.
	"""
	url = f"{MUSICGRAPH_BASE}/artist/search?"
	params = urllib.parse.urlencode({'api_key': API_KEY, 'name': artname})
	data = urllib.request.urlopen(url + params).read()
	js = json.loads(data)
	return js['data'][0]['main_genre'] if js['data'] else None

def ensure_genre_in_db(cur, genre):
	cur.execute('SELECT name FROM genre')
	genname = cur.fetchall()
	if not any(gn[0] == genre for gn in genname):
		cur.execute('INSERT INTO genre(name) VALUES(?)', (genre, ))

def insert_artist(cur, artname):
	cur.execute('INSERT INTO artist(name) VALUES(?)', (artname, ))

def fetch_albums(artname):
	url = f"{MUSICGRAPH_BASE}/album/search?"
	params = urllib.parse.urlencode({'api_key': API_KEY, 'artist_name': artname})
	data = urllib.request.urlopen(url + params).read()
	js = json.loads(data)
	return [d for d in js['data'] if d.get('product_form') == 'album']

def insert_album(cur, album, artid):
	cur.execute(
		'INSERT INTO album(name, artist_id, year, trackcount) VALUES(?,?,?,?)',
		(album['title'], artid, album.get('release_year'), album.get('number_of_tracks'))
	)

def fetch_album_tracks(album_id):
	url = f"{MUSICGRAPH_BASE}/album/{album_id}/tracks?"
	params = urllib.parse.urlencode({'api_key': API_KEY})
	data = urllib.request.urlopen(url + params).read()
	js = json.loads(data)
	return js['data']

def fetch_lyrics(artname, track_title):
	url = LYRIC_API_BASE + urllib.parse.quote(f"{artname}/{track_title}")
	try:
		lyr = json.loads(urllib.request.urlopen(url).read())
		return lyr.get('lyric', '')
	except:
		return ''

def insert_track(cur, track, album_title, genre, artname):
	cur.execute('SELECT id FROM album WHERE name=?', (album_title,))
	albid = cur.fetchone()
	cur.execute('SELECT id FROM genre WHERE name=?', (genre,))
	genid = cur.fetchone()
	dur = int(track.get('duration', 0))
	time = f"{dur // 60}:{dur % 60}"
	lyrics = fetch_lyrics(artname, track['title'])
	cur.execute(
		'INSERT INTO track(name, lyrics, album_id, length, genre_id) VALUES(?,?,?,?,?)',
		(track['title'], lyrics, albid[0], time, genid[0])
	)

def update(artname, cur):
	"""
	Updates the database with information about the given artist.
	This function performs the following steps:
	1. Fetches the genre for the specified artist. If not found, prints a message and returns.
	2. Ensures the genre exists in the database.
	3. Inserts the artist into the database.
	4. Fetches all albums for the artist.
	5. For each album:
		a. Inserts the album into the database.
		b. Fetches all tracks for the album.
		c. Inserts each track into the database, updating progress on the screen.
	6. After processing all albums and tracks, prints a completion message.
	7. Updates album and song counters in the database.
	Args:
		artname (str): The name of the artist to update in the database.
		cur (sqlite3.Cursor): The database cursor used for executing SQL commands.
	Returns:
		None
	"""
	genre = fetch_artist_genre(artname)
	if not genre:
		print(f"Genre not found for artist: {artname}")
		return
	
	ensure_genre_in_db(cur, genre)
	
	insert_artist(cur, artname)
	
	albums = fetch_albums(artname)
	total_tracks = sum(int(a.get('number_of_tracks', 0)) for a in albums)
	count = 0

	for album in albums:
		try:
			cur.execute('SELECT id FROM artist WHERE name=?', (artname,))
			artid = cur.fetchone()[0]
			insert_album(cur, album, artid)
			tracks = fetch_album_tracks(album['id'])
			for track in tracks:
				try:
					insert_track(cur, track, album['title'], genre, artname)
				except Exception:
					continue
				clear_screen()
				print('Adding Artist: ', artname)
				print('\n\n=====Updating Database=====')
				count += 1
				perc = (float(count) / float(total_tracks)) * 100.00 if total_tracks else 100
				print('\n\n Downloading...  ', perc, '%')
		except Exception:
			continue
	clear_screen()
	print(artname, ' Added!')
	setcount.albcounter(cur)
	setcount.songcounter(cur)