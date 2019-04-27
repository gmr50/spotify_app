import os
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import spotipy.util as util 
from flask import Flask, render_template, request, redirect, Blueprint
import random
import datetime 





def prompt_token_flask(user_id):




    username = user_id

    

    scope = 'user-top-read playlist-modify-public'
    client_id_saved = os.environ.get("CLIENT_ID", "Oops, please set env var called 'CLIENT_ID'")
    client_secret_saved = os.environ.get("CLIENT_SECRET", "Oops, please set env var called  'CLIENT_SECRET")
    redirect_uri_saved = "http://localhost:5000/callback/"
    path = (os.path.normpath(os.getcwd()) + "/web_app/caches/.cache-" + username)



    return SpotifyOAuth(
        client_id=client_id_saved,
        client_secret=client_secret_saved,
        redirect_uri=redirect_uri_saved,
        scope=scope,
        cache_path=path
    )



def get_user_playlists(token, user_id):

    username = user_id

    passed_token = token 

    sp = spotipy.Spotify(auth=passed_token)

    #print(inspect.getsource(sp.current_user_top_tracks()))

    sp.trace = False

    playlists = sp.user_playlists(username)

    n=1
    
    array_list = [] 
    id_array = []

    
    #print("Which playlist would you like to pick?")
    for item_get in playlists['items']:

        #namestr = item_get['items']['name']
        #tracksstr = item_get['items']['tracks']
        namestr = item_get['name']
        playlist_item = item_get['id']
        #print(str(n) + ' ' + namestr + ' ' + playlist_item)


        array_list = [namestr, playlist_item]
        id_array.append(array_list)

        n = n+ 1


    #print(id_array)



    return id_array


def add_playlist_for_seed(input, playlists_list):
    
    playlists_list.append(input)

    print(playlists_list)
    return playlists_list



def add_tracks_for_seed(username, selected_playlist, token):
    tracks_list = []


    sp = spotipy.Spotify(auth=token)
    playlist_tracks = sp.user_playlist_tracks(username,selected_playlist)

    for track in playlist_tracks['items']:
        tracks_list.append(track['track']['id'])

    return tracks_list



def add_top_tracks_for_seed(track_range, token):

    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_tracks(time_range=track_range, limit=50)
    id_array = []

    
    for i, item in enumerate(results['items']):
        print(i, item['name'], '//', item['artists'][0]['name'])
        id_array.append(item['id'])

    return id_array



def build_playlist(tracks, token):
    sp = spotipy.Spotify(auth=token)

    tracks = random.sample(tracks, len(tracks))

    n = 3
    x = 0
    #https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    sublist = [tracks[i * n:(i + 1) * n] for i in range((len(tracks) + n - 1) // n )] 


    rec_list = []

    while x < len(sublist):

        recomends = sp.recommendations(seed_tracks=list(sublist[x]), limit=3)
        #pprint.pprint(recomends)
    

        rec_list.append(recomends['tracks'][0]['id'])
        print(recomends['tracks'][0]['name'])
        rec_list.append(recomends['tracks'][1]['id'])

        
        x = x+1
    return(rec_list)


def execute_playlist(token, username, recommendations, playlist_name):



    now = datetime.datetime.now()
    timestring = now.strftime("%H//%M//%S//%f")
    print(timestring)
    sp = spotipy.Spotify(auth=token)

    playlist_name = ("GMR HIST MCHN: " + playlist_name + " " + timestring)
    playlist_description = ("GMR's HISTORY MACHINE working project playlist")
    print(playlist_name)
    #creates playlist
    #https://github.com/plamere/spotipy/blob/master/examples/create_playlist.py
    playlists = sp.user_playlist_create(username, playlist_name, public = True, description = playlist_description)


    playlist_id = playlists['id']


    sp.user_playlist_add_tracks(username, playlist_id, recommendations, position=None)

    message = "success"
    return message

def playlist_unfollow(user, token):


    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(user)
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




    message = "nothing deleted"
    if(len(gmr_id) > 2):

        gmr_id[-1]
        sp.user_playlist_unfollow(user, gmr_id[-1])
        message = "deleted"



    return message



def strip_selection(selection):

    selection = selection.replace("'","")
    selection = selection.strip('[')
    selection = selection.strip(']')
    selection = selection.split(', ')

    return selection



if __name__ == "__main__":
    print("main")
