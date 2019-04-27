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
import dotenv


import random
from datetime import datetime
import json
#https://www.youtube.com/watch?v=jz6mBRJXVoY
username = "gmr0678"



scope = 'user-top-read playlist-modify-private playlist-modify-public'
#client_id_saved = os.environ.get("CLIENT_ID", "Oops, please set env var called 'CLIENT_ID'")
client_id_saved = "ec76592c5f224effa7107e833904173f"
client_secret_saved = "b45382aebfb547e889b07368fabf93aa"
redirect_uri_saved = "https://www.google.com/"
cache_path = os.path.normpath(os.getcwd()) + "/caches/.cache-" + username




token = util.prompt_for_user_token(
		username=username,
		scope=scope,
		client_id=client_id_saved,
		client_secret=client_secret_saved,
		redirect_uri=redirect_uri_saved,
		cache_path = cache_path)

if token:
	sp = spotipy.Spotify(auth=token)








playlists = sp.user_playlists(username)
name_array = [] 
id_array = []
x = 0
for item in playlists["items"]:

	name_array.append(item["name"])
	id_array.append(item["id"])


gmr_list = []
gmr_id = []

for item, id_code in zip(name_array, id_array):
	result = item.startswith("GMR HIST MCHN")
	if(result):
		gmr_list.append(item)
		gmr_id.append(id_code)



print(gmr_list)
print(gmr_id)


if(len(gmr_id) > 2):

	gmr_id[-1]
	sp.user_playlist_unfollow(username, gmr_id[-1])









