import sqlite3
import os
import addart
import albums

def art_browse(ch0, flag, cur, conn):		
	while True:
		os.system('cls')
		if flag==1: break
		print '===================ARTISTS===================== \n\n'
		print 'Artists: \n\n'
		cur.execute('''select id, name from artist''')
		nm1=cur.fetchall()
		for artname in nm1:
			print artname[0],'->', artname[1],'\n\n'
		print '\n\na-> Add Artist\n\n'	
		print 'b-> Back\n\n'
		print 'm-> Main\n\n' 
		ch1= raw_input('Enter Choice: ')
		if ch1=='a':
			os.system('cls')
			add1=raw_input('Enter Artist Name: ')
			addart.update(add1,cur)
			conn.commit()
			print '\nb-> Back\n\n'
			print 'm-> Main\n\n'
			add2= raw_input('Enter Choice: ')
			if add2=='b':
				break
			elif add2=='m':
				flag=1
		elif ch1=='b':
			break
		elif ch1=='m':
			flag=1	
		cur.execute('''select name from artist where id=?''',(ch1, ))
		nm2=cur.fetchone()

		flag=albums.alb_browse(ch0, nm2, ch1, flag, cur)
	return flag
