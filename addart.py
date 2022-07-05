import json
import urllib
import sqlite3
import setcount
import os

def update(artname,cur):
	
	url='http://api.musicgraph.com/api/v2/artist/search?'
	url1=url+urllib.urlencode({'api_key':'5047c0ecb7625ed2dd03f1c35845d35a','name':artname})
	data0=urllib.urlopen(url1).read()
	js0=json.loads(data0)
	genre=js0['data'][0]['main_genre']
	cur.execute('''select name from genre''')
	genname=cur.fetchall()
	flag=0
	for gn in genname:
		if gn[0]==genre:
			flag=1
	if flag!=1:
		cur.execute('''insert into genre(name) values(?)''', (genre, ))
	
	cur.execute('''insert into artist(name) values(?)''',(artname, ))
	
	sum=0
	count=0
	url='http://api.musicgraph.com/api/v2/album/search?'
	url1=url+urllib.urlencode({'api_key':'5047c0ecb7625ed2dd03f1c35845d35a','artist_name':artname})
	data=urllib.urlopen(url1).read()
	js=json.loads(data)
	for d in js['data']:
			if d['product_form']=='album':
				sum=sum+int(d['number_of_tracks'])
	
	url='http://api.musicgraph.com/api/v2/album/search?'
	url1=url+urllib.urlencode({'api_key':'5047c0ecb7625ed2dd03f1c35845d35a','artist_name':artname})
	data=urllib.urlopen(url1).read()
	js=json.loads(data)
	for d in js['data']:
		try:
			if d['product_form']=='album':
				cur.execute('''select id from artist where name=?''', (artname, ))
				artid=cur.fetchone()
				cur.execute('''insert into album(name, artist_id, year, trackcount) values(?,?,?,?)''',(d['title'], artid[0], d['release_year'], d['number_of_tracks'] ))
				trackurl='http://api.musicgraph.com/api/v2/album/'+d['id']+'/tracks?'
				url2=trackurl+urllib.urlencode({'api_key':'5047c0ecb7625ed2dd03f1c35845d35a'})
				list=urllib.urlopen(url2).read()
				js1=json.loads(list)
				for t in js1['data']:
					cur.execute('''select id from album where name=?''', (d['title'], ))
					albid=cur.fetchone()
					cur.execute('''select id from genre where name=?''', (genre, ))
					genid=cur.fetchone()
					dur= int(t['duration'])
					time=str(dur/60)+':'+str(dur%60)
					serviceurl='http://lyric-api.herokuapp.com/api/find/'
					try:
						url3=serviceurl+urllib.pathname2url(artname+'/'+t['title'])
						lyr=json.loads(urllib.urlopen(url3).read())
						cur.execute('''Insert into track(name, lyrics, album_id, length, genre_id) values(?,?,?,?,?)''',(t['title'],lyr['lyric'],albid[0],time, genid[0]))						
					except:						
						continue
					os.system('cls')
					print('Adding Artist: ',artname)
					print('\n\n=====Updating Database=====')
					count=count+1
					perc=(float(count)/float(sum))*100.00
					print('\n\n Downloading...  ', perc, '%')	
		except:
			continue
	os.system('cls')
	print(artname, ' Added!')			
	setcount.albcounter(cur)
	setcount.songcounter(cur)