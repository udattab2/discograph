import sqlite3
import os

def lyr_show(nm6, flag, cur):
	while True:
		os.system('cls')
		if flag==1: break
		print('===============',nm6[0],'===============\n\n')
		cur.execute('''select name from genre where id=?''',(nm6[3], ))
		nm6g=cur.fetchone()
		cur.execute('''select name, artist_id from album where id=?''', (nm6[2], ))
		nm6a=cur.fetchone()
		cur.execute('''select name from artist where id=?''',(nm6a[1], ))
		nm6b=cur.fetchone()
		print('Length: ',nm6[1],'\n\n')
		print('Artist: ',nm6b[0],'\n\n')
		print('Album: ', nm6a[0],'\n\n')
		print('Genre: ', nm6g[0],'\n\n')
		print('Lyrics:\n', nm6[4],'\n\n')
		print('\n\nb-> Back\n\n')
		print('m-> Main\n\n')
		nav1=input('Enter Choice: ')
		if nav1=='b': break
		elif nav1=='m':
			flag=1
	return flag