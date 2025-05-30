import sqlite3
import utils.artists as artists
import utils.srch as srch
import utils.genres as genres
from utils.helper import clear_screen


def discograph():
	"""
	Main function to run the discograph application.	
	This function initializes the SQLite database connection,
	begins a cursor session, and provides a menu for the user to explore the discography tool.
	"""
	conn=sqlite3.connect('test2.db')
	cur=conn.cursor()


	while True:
		flag=0
		clear_screen()
		print('===============DISCOGRAPH=============== \n\n')
		print('Explore By: \n\n')
		print('1-> Artists \n\n')
		print('2-> Genre \n\n')
		print('\n\ns-> Search \n\n')
		print('\n\ne-> Exit\n\n')
		ch0=input('Enter Choice: ')
		if ch0=='e': 
			clear_screen()
			break
		elif ch0=='s':
			srch.src(flag, cur)
		elif ch0=='1':
			artists.art_browse(ch0, flag, cur, conn)	
		elif ch0=='2':
			genres.gen_browse(ch0, flag, cur)

	cur.close()	

if __name__ == "__main__":
	discograph()
