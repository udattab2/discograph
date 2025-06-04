import sqlite3

def albcounter(cur):
	cur.execute('''select * from album''')
	lst=cur.fetchall()
	count=1
	for i in lst:
		if i[5] is None:
			s=sum(1 for j in lst if i[2]==j[2])
			if count<=s:
				cur.execute('''update album set album_no=? where id=?''',(count, i[0]))
				if count==s:
					count=1
				else:
					count=count+1

def songcounter(cur):
	cur.execute('''select * from track''')
	lst=cur.fetchall()
	count=1
	for i in lst:
		if i[5] is None:
			s=sum(1 for j in lst if i[2]==j[2])
			if count<=s:
				cur.execute('''update track set song_no=? where id=?''',(count, i[0]))
				if count==s:
					count=1
				else:
					count=count+1