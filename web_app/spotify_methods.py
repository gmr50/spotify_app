import os
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import spotipy.util as util 
from flask import Flask, render_template, request, redirect, Blueprint
import random
import datetime 
import csv





def prompt_token_flask(user_id):




    username = user_id


    

    scope = 'user-top-read playlist-modify-public'
    client_id_saved = os.environ.get("CLIENT_ID", "Oops, please set env var called 'CLIENT_ID'")
    client_secret_saved = os.environ.get("CLIENT_SECRET", "Oops, please set env var called  'CLIENT_SECRET")
    redirect_uri_saved = os.environ.get("REDIRECT_URL", "http://localhost:5000/callback/")
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

    sp.trace = False

    playlists = sp.user_playlists(username)

    n=1
    
    array_list = [] 
    id_array = []

    
    for item_get in playlists['items']:

        namestr = item_get['name']
        playlist_item = item_get['id']



        array_list = [namestr, playlist_item]
        id_array.append(array_list)

        n = n+ 1


    return id_array


def add_playlist_for_seed(input, playlists_list):
    
    playlists_list.append(input)

    
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
        id_array.append(item['id'])

    return id_array



def build_playlist(tracks, token):
    sp = spotipy.Spotify(auth=token)

    tracks = random.sample(tracks, len(tracks))

    #for large seed lists, incorporates 4 tracks instead of 3 for each recommended song
    if(len(tracks)>200):
        n = 4
    else:
        n = 3

    
    x = 0
    #https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    sublist = [tracks[i * n:(i + 1) * n] for i in range((len(tracks) + n - 1) // n )] 


    rec_list = []


    #75 is the maximum size of a playlist
    limit = 0
    if(len(sublist) < 75):
        limit = len(sublist)
    else:
        limit = 75


    while x < limit:

        recomends = sp.recommendations(seed_tracks=list(sublist[x]), limit=2)
        rec_list.append(recomends['tracks'][0]['id'])
        x = x+1

    loopagain = False

    if limit < 75:
        limit  = 75 - len(sublist)
        loopagain = True
        #gives a new limit allowing tracks to be added up until the 74 track limit

    x = 0

    if loopagain:
        while x < min(limit,len(sublist)):

            recomends = sp.recommendations(seed_tracks=list(sublist[x]), limit=2)
            #adds the second returned recommendation
            rec_list.append(recomends['tracks'][1]['id'])
            x = x+1



    return(rec_list)


def execute_playlist(token, username, recommendations, playlist_name, description):



    now = datetime.datetime.now()
    timestring = now.strftime("%H//%M//%S//%f")
    print(timestring)
    sp = spotipy.Spotify(auth=token)

    playlist_name = ("GMR HIST MCHN: " + playlist_name + " " + timestring)
 
    #creates playlist
    #https://github.com/plamere/spotipy/blob/master/examples/create_playlist.py
    description = str(description)

    description1 = description[0:300]
    print("description debug: " + description)
    #playlists = sp.user_playlist_create(username, playlist_name, public = True, description = description1)
    playlists = sp.user_playlist_create(username, playlist_name, public = True)

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


def read_tracks_from_csv():

    csv_filepath = os.path.normpath(os.getcwd()) + "/web_app/csv_files/tracks.csv"

    #https://therenegadecoder.com/code/how-to-check-if-a-file-exists-in-python/
    exists = os.path.isfile(csv_filepath)

    print(csv_filepath)


    with open(csv_filepath, "r") as csv_file:
        reader = csv.reader(csv_file)
        csv_list = []
        for row in reader:

            #making sure extraneous characters are not added
            row = str(row)
            row = row[2:-2]
            csv_list.append(row)


        if(len(csv_list)==0):
            print("empty")

        else:
            print("not empty")

    return csv_list



def write_tracks_to_csv(tracks_list):

    csv_filepath = os.path.normpath(os.getcwd()) + "/web_app/csv_files/tracks.csv"

    try:
        with open(csv_filepath, "w") as csv_file: # "w" means "open the file for writing"
            writer = csv.writer(csv_file)
            for track in tracks_list:
                writer.writerow([str(track)])

    except:
        print("no csv file to write to")

    success = True

    return success


def clear_tracks_csv():
    print("clearing tracks")
    csv_filepath = os.path.normpath(os.getcwd()) + "/web_app/csv_files/tracks.csv"
    csv = open(csv_filepath, "w")
    csv.truncate()
    csv.close()

    cleared = True

    return cleared

def check_login(token,user_id):
    sp = spotipy.Spotify(auth=token)

    me = sp.current_user()

    if(me['id'] != user_id):
        return False
    else:
        return True




if __name__ == "__main__":
    print("main")
