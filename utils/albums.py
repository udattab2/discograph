import sqlite3
import os
import tracks

def alb_browse(ch0, nm2, ch1, flag, cur):
	while True:
		os.system('cls')
		if flag==1: break
		print('===============',nm2[0],'===============\n\n')
		print('Albums: \n\n')
		
		if ch0=='1':
			cur.execute('''select album_no, name from album where artist_id=? order by album_no''',(ch1, ))
		elif ch0=='2':
			cur.execute('''select distinct(album.name), album.id from album join track on album.id=track.album_id where track.genre_id=? order by album_no''', (ch1, ))
		nm3=cur.fetchall()
		for albname in nm3:
			try:
				if ch0=='1':
					print(albname[0],'->',albname[1],'\n\n')
				elif ch0=='2':
					print(albname[1],'->',albname[0],'\n\n')	
			except:
				continue		
		print('\n\nb-> Back\n\n')
		print('m-> Main\n\n')	
		ch2= input('Enter Choice: ')
		if ch2=='b':
			break	
		elif ch2=='m':
				flag=1	
		else:
			if ch0=='1':
				cur.execute('''select name, trackcount, year, id from album where artist_id=? and album_no=?''',(ch1, ch2, ))
			elif ch0=='2':
				cur.execute('''select name, trackcount, year, id from album where id=?''', (ch2, ))
			nm4= cur.fetchone()
		
		flag=tracks.track_browse(nm4, flag, cur)
	return flag