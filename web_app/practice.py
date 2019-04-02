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
cache_path = os.path.normpath(os.getcwd()) + "/caches/.cache-" + username

print(cache_path)

print(spotipy.VERSION)

token = util.prompt_for_user_token(
		username=username,
		scope=scope,
		client_id=client_id_saved,
		client_secret=client_secret_saved,
		redirect_uri=redirect_uri_saved,
		cache_path = cache_path)
print(token)

if token:
	sp = spotipy.Spotify(auth=token)

print(token)