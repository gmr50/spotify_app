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
import csv

from spotify_methods import read_tracks_from_csv, clear_tracks_csv

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


print("trying to delete tracks")
clear_tracks_csv()














