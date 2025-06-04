import sqlite3
import os
import utils.lyrics as lyrics
from utils.helper import clear_screen

def track_browse(nm4, flag, cur):		
	while True:
		clear_screen()
		if flag==1: break
		print('===============',nm4[0],'===============\n\n')
		print('Year of Release: ', nm4[2],'\n\n')
		print('No. of Tracks: ',nm4[1],'\n\n')
		print('Tracklist: \n\n')
		cur.execute('''select song_no, name from track where album_id=?''',(nm4[3], ))
		nm5=cur.fetchall()
		for trackname in nm5:
			print(trackname[0],'->',trackname[1],'\n\n')
		print('\n\nb-> Back\n\n')
		print('m-> Main\n\n')
		ch3= input('Enter Choice: ')
		if ch3=='b':
			break
		elif ch3=='m':
			flag=1	
		else:	
			cur.execute('''select name, length, album_id, genre_id, lyrics from track where album_id=? and song_no=?''',(nm4[3],ch3, ))
			nm6=cur.fetchone()
		flag=lyrics.lyr_show(nm6, flag, cur)
	return flag
	
def track_src(trackres, flag, cur):
	while True:
		clear_screen()
		if flag==1: break
		print('===============SEARCH RESULTS===============\n\n')
		for trackname in trackres:
			print(trackname[0],'->',trackname[1],'\n\n')
		print('\n\nb-> Back\n\n')
		print('m-> Main\n\n')
		ch3= input('Enter Choice: ')
		if ch3=='b':
			break
		elif ch3=='m':
			flag=1	
		else:
			cur.execute('''select name, length, album_id, genre_id, lyrics from track where id=?''', (ch3, ))
			nm6=cur.fetchone()
		flag=lyrics.lyr_show(nm6, flag, cur)
	return flag	