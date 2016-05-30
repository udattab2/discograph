import sqlite3
import tracks
import os

def src(flag, cur):
	os.system('cls')
	print '===============SEARCH===============\n\n'
	srchstr=raw_input('Search For: ')
	cur.execute('''select * from track where name=?''',(srchstr, ))
	trackres=cur.fetchall()
	flag=tracks.track_src(trackres, flag, cur)