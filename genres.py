import sqlite3
import os
import albums

def gen_browse(ch0, flag, cur):		
	while True:
		os.system('cls')
		if flag==1: break
		print('===============GENRES===============\n\n')
		cur.execute('''select * from genre''')
		gr1=cur.fetchall()
		for genrename in gr1:
			print(genrename[0],'->',genrename[1],'\n\n')
		print('b-> Back\n\n')
		print('m-> Main\n\n')
		ch4=input('Enter Choice: ')
		if ch4=='b': break
		elif ch4=='m':
			flag=1
		cur.execute('''select name from genre where id=?''',(ch4, ))
		gr2=cur.fetchone()
		
		flag=albums.alb_browse(ch0, gr2, ch4, flag, cur)
	return flag