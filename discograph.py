import sqlite3
import os
import addart
import artists
import srch
import genres

conn=sqlite3.connect('test2.db')
cur=conn.cursor()


while True:
	flag=0
	os.system('cls')
	print '===============DISCOGRAPH=============== \n\n'
	print 'Explore By: \n\n'
	print '1-> Artists \n\n'
	print '2-> Genre \n\n'
	print '\n\ns-> Search \n\n'
	print '\n\ne-> Exit\n\n'
	ch0=raw_input('Enter Choice: ')
	if ch0=='e': 
		os.system('cls')
		break
	elif ch0=='s':
		srch.src(flag, cur)
	elif ch0=='1':
		artists.art_browse(ch0, flag, cur, conn)	
	elif ch0=='2':
		genres.gen_browse(ch0, flag, cur)

cur.close()	