import json
import urllib.parse
import urllib.request
import sqlite3
from typing import Any, cast
from utils.helper import console
import utils.setcount as setcount
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

API_KEY = '5047c0ecb7625ed2dd03f1c35845d35a'
MUSICGRAPH_BASE = 'http://api.musicgraph.com/api/v2'
LYRIC_API_BASE = 'http://lyric-api.herokuapp.com/api/find/'

def fetch_artist_genre(artname: str) -> str | None:
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

def ensure_genre_in_db(cur: sqlite3.Cursor, genre: str) -> None:
	cur.execute('SELECT name FROM genre')
	genname = cur.fetchall()
	if not any(gn[0] == genre for gn in genname):
		cur.execute('INSERT INTO genre(name) VALUES(?)', (genre, ))

def insert_artist(cur: sqlite3.Cursor, artname: str) -> None:
	cur.execute('INSERT INTO artist(name) VALUES(?)', (artname, ))

def fetch_albums(artname: str) -> list[dict[str, Any]]:
	url = f"{MUSICGRAPH_BASE}/album/search?"
	params = urllib.parse.urlencode({'api_key': API_KEY, 'artist_name': artname})
	data = urllib.request.urlopen(url + params).read()
	js = json.loads(data)
	return [d for d in js['data'] if d.get('product_form') == 'album']

def insert_album(cur: sqlite3.Cursor, album: dict[str, Any], artid: int) -> None:
	cur.execute(
		'INSERT INTO album(name, artist_id, year, trackcount) VALUES(?,?,?,?)',
		(album['title'], artid, album.get('release_year'), album.get('number_of_tracks'))
	)

def fetch_album_tracks(album_id: str) -> list[dict[str, Any]]:
	url = f"{MUSICGRAPH_BASE}/album/{album_id}/tracks?"
	params = urllib.parse.urlencode({'api_key': API_KEY})
	data = urllib.request.urlopen(url + params).read()
	js = json.loads(data)
	return cast(list[dict[str, Any]], js['data'])

def fetch_lyrics(artname: str, track_title: str) -> str:
	url = LYRIC_API_BASE + urllib.parse.quote(f"{artname}/{track_title}")
	try:
		lyr = json.loads(urllib.request.urlopen(url).read())
		return cast(str, lyr.get('lyric', ''))
	except Exception:
		return ''

def insert_track(cur: sqlite3.Cursor, track: dict[str, Any], album_title: str, genre: str, artname: str) -> None:
	cur.execute('SELECT id FROM album WHERE name=?', (album_title,))
	albid_row = cur.fetchone()
	if not albid_row:
		return
	albid = albid_row[0]

	cur.execute('SELECT id FROM genre WHERE name=?', (genre,))
	genid_row = cur.fetchone()
	if not genid_row:
		return
	genid = genid_row[0]

	dur = int(track.get('duration', 0))
	time = f"{dur // 60}:{dur % 60}"
	lyrics = fetch_lyrics(artname, track['title'])
	cur.execute(
		'INSERT INTO track(name, lyrics, album_id, length, genre_id) VALUES(?,?,?,?,?)',
		(track['title'], lyrics, albid, time, genid)
	)

def update(artname: str, cur: sqlite3.Cursor) -> None:
	"""
	Updates the database with information about the given artist.
	"""
	genre = fetch_artist_genre(artname)
	if not genre:
		console.print(f"[bold red]Error:[/bold red] Genre not found for artist: {artname}")
		return
	
	ensure_genre_in_db(cur, genre)
	insert_artist(cur, artname)
	
	albums = fetch_albums(artname)
	total_tracks = sum(int(a.get('number_of_tracks', 0)) for a in albums)

	with Progress(
		BarColumn(),
		TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
		TimeRemainingColumn(),
		console=console
	) as progress:
		task = progress.add_task(f"Downloading discography for {artname}...", total=total_tracks)

		for album in albums:
			try:
				cur.execute('SELECT id FROM artist WHERE name=?', (artname,))
				artid_row = cur.fetchone()
				if not artid_row:
					continue
				artid = artid_row[0]
				insert_album(cur, album, artid)
				tracks = fetch_album_tracks(album['id'])
				for track in tracks:
					try:
						insert_track(cur, track, album['title'], genre, artname)
					except Exception:
						pass
					progress.update(task, advance=1)
			except Exception:
				continue
				
	setcount.albcounter(cur)
	setcount.songcounter(cur)