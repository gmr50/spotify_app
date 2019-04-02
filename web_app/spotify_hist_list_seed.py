
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

	n=1
	

	id_array = []

	
	print("Which playlist would you like to pick?")
	for item_get in playlists['items']:

		#namestr = item_get['items']['name']
		#tracksstr = item_get['items']['tracks']
		namestr = item_get['name']
		playlist_item = item_get['id']
		print(str(n) + ' ' + namestr + ' ' + playlist_item)
		id_array.append(playlist_item)
		n = n+ 1


	

	track_list = []

	user_input_validation = True


	while user_input_validation:

		print("Which playlist?")
		playlist_selection = input()
		playlist_selection = int(playlist_selection)

		if(playlist_selection > len(id_array) or playlist_selection < 0):
			print("Please input a valid number")
		else:

			selected_playlist = id_array[playlist_selection - 1]
			playlist_tracks = sp.user_playlist_tracks(username,selected_playlist)

			for track in playlist_tracks['items']:
				track_list.append(track['track']['id'])



			print("Would you like to add another playlist to seed? Press Y")
			user_input = input()
			if(user_input != 'Y'):
				user_input_validation = False 





	

	#0u7NLX1XNKcqF2pdXxBD60
	

	#[items][track][id]

	

	





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

	n = 3
	#sublist = results_search_song.push(results_search_song.splice(0, 3));
	#https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
	sublist = [results_search_song[i * n:(i + 1) * n] for i in range((len(results_search_song) + n - 1) // n )] 
	#sublist = numpy.array_split(results_search_song, upper_limit, axis = 0)
	#pprint.pprint(sublist)


	print(sublist)


	

	rec_list = []

	
	

	#['tracks'][1]['id']
	while x < len(sublist):

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


	playlist_name = ("GMR HIST MCHN: PLAYLIST SEED" + timestring)
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



