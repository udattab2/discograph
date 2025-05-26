from utils.helper import clear_screen
import utils.tracks as tracks

def src(flag, cur):
	clear_screen()
	print('===============SEARCH===============\n\n')
	srchstr=input('Search For: ')
	cur.execute('''select * from track where name=?''',(srchstr, ))
	trackres=cur.fetchall()
	flag=tracks.track_src(trackres, flag, cur)