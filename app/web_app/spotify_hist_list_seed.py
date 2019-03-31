
import os
import sys
import json
import spotipy
import webbrowser
import pprint
import spotipy.util as util
import pprint as pprint
import pandas
import numpy

import random
from datetime import datetime

#https://www.youtube.com/watch?v=jz6mBRJXVoY
username = sys.argv[1]



scope = 'user-top-read playlist-modify-private'
client_id_saved = "ec76592c5f224effa7107e833904173f"
client_secret_saved = "b45382aebfb547e889b07368fabf93aa"
redirect_uri_saved = "https://www.google.com/"


print(spotipy.VERSION)

token = util.prompt_for_user_token(
		username=username,
		scope=scope,
		client_id=client_id_saved,
		client_secret=client_secret_saved,
		redirect_uri=redirect_uri_saved)

if token:
	sp = spotipy.Spotify(auth=token)

	#print(inspect.getsource(sp.current_user_top_tracks()))

	sp.trace = False

	playlists = sp.user_playlists(username)
	#pprint.pprint(playlists)


	
	print(type(playlists))
	
	for item_get in playlists['items']:

		#namestr = item_get['items']['name']
		#tracksstr = item_get['items']['tracks']
		namestr = item_get['name']
		trackstr = item_get['id']
		print(namestr + ' ' + trackstr)


	



	#0u7NLX1XNKcqF2pdXxBD60
	playlist_tracks = sp.user_playlist_tracks(username,'0u7NLX1XNKcqF2pdXxBD60')
	pprint.pprint(playlist_tracks)


	#[items][track][id]

	track_list = []

	for track in playlist_tracks['items']:
		track_list.append(track['track']['id'])


	print(track_list)


	results_search_song = track_list
	# ranges = ['short_term']
	# results_search_song = []
	# results_search_artist = []
	# for range in ranges:
	# 	#print("range:", range)
	# 	results = sp.current_user_top_tracks(time_range=range, limit=50)

	# 	#pprint.pprint(results)

	# 	#[items][id]
	
	# 	for i, item in enumerate(results['items']):
	# 		#print(i, item['name'], '//', item['artists'][0]['name'])
	# 		results_search_song.append(item['id'])
	# 	print()

		#print(results_search_song)



	#*****************fix rec list array argument for length in recs array************
	
	upper_limit = int((len(results_search_song))-20)
		#print("upper limit")
		#print(upper_limit)
	x = 0

	upper_limit = round(upper_limit * 2)


	results_search_song = random.sample(results_search_song, len(results_search_song))
	#sublist = numpy.arrange(results_search_song)
	sublist = numpy.array_split(results_search_song, upper_limit, axis = 0)
	#pprint.pprint(sublist)


	print(sublist)


	

	rec_list = []

	
	

	#['tracks'][1]['id']
	while x < upper_limit:

		recomends = sp.recommendations(seed_tracks=list(sublist[x]), limit=3)
		#pprint.pprint(recomends)
	

		rec_list.append(recomends['tracks'][1]['id'])
		rec_list.append(recomends['tracks'][2]['id'])

		print("loop")
		x = x+1


	

else:
	print("Authorization failed")


# scope = "playlist-modify-public"
# token = util.prompt_for_user_token(
#       username=username,
#       scope=scope,
#       client_id=client_id_saved,
#       client_secret=client_secret_saved,
#       redirect_uri=redirect_uri_saved)


# print("Beginning Authorization #2: ")

if token:

	now = datetime.now()
	timestring = now.strftime("%H//%M//%S//%f")
	print(timestring)


	playlist_name = ("GMR HIST MCHN: " + timestring)
	playlist_description = ("GMR's HISTORY MACHINE working project playlist")
	print(playlist_name)
	#creates playlist
	#https://github.com/plamere/spotipy/blob/master/examples/create_playlist.py
	playlists = sp.user_playlist_create(username, playlist_name, public = False, description = playlist_description)
	pprint.pprint(playlists)

	playlist_id = playlists['id']


	results_search_song = (results_search_song[0:35])
	results_search_song = random.sample(results_search_song, len(results_search_song))


	tracks = rec_list

	sp.user_playlist_add_tracks(username, playlist_id, tracks, position=None)

		#results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
else: 
	print("Authorization failed")



