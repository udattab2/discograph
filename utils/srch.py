import sqlite3
import utils.tracks as tracks
import os

def src(flag, cur):
	os.system('cls')
	print('===============SEARCH===============\n\n')
	srchstr=input('Search For: ')
	cur.execute('''select * from track where name=?''',(srchstr, ))
	trackres=cur.fetchall()
	flag=tracks.track_src(trackres, flag, cur)