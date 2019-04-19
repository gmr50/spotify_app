import os
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
import spotipy.util as util 
from flask import Flask, render_template, request, redirect, Blueprint



def prompt_for_user_token_override(username, scope=None, client_id = None,
        client_secret = None, redirect_uri = None, cache_path = None):
    ''' prompts the user to login if necessary and returns
        the user token suitable for use with the spotipy.Spotify 
        constructor
        Parameters:
         - username - the Spotify username
         - scope - the desired scope of the request
         - client_id - the client id of your app
         - client_secret - the client secret of your app
         - redirect_uri - the redirect URI of your app
         - cache_path - path to location to save tokens
    '''

    if not client_id:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')

    if not client_secret:
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    if not redirect_uri:
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    if not client_id:
        print('''
            You need to set your Spotify API credentials. You can do this by
            setting environment variables like so:
            export SPOTIPY_CLIENT_ID='your-spotify-client-id'
            export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
            export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
            Get your credentials at     
                https://developer.spotify.com/my-applications
        ''')
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    cache_path = cache_path or ".cache-" + username
    sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=scope, cache_path=cache_path)

    # try to get a valid token for this user, from the cache,
    # if not in the cache, the create a new (this will send
    # the user to a web page where they can authorize this app)

    token_info = sp_oauth.get_cached_token()

    if not token_info:
        print('''
            User authentication requires interaction with your
            web browser. Once you enter your credentials and
            give authorization, you will be redirected to
            a url.  Paste that url you were directed to to
            complete the authorization.
        ''')
        auth_url = sp_oauth.get_authorize_url()
        print(auth_url + "**************")
        try:
            import webbrowser
            webbrowser.open(auth_url)
            print("Opened %s in your browser" % auth_url)
        except:
            print("Please navigate here: %s" % auth_url)


        print()
        print()

        #os.environ['sp_oauth'] = sp_oauth



        #try:
             #response = webbrowser.get(auth_url)
           

        #except NameError:

             #response = webbrowser.get(auth_url)
            
        #     response = input("Enter the URL you were redirected to: ")


    #     code = sp_oauth.parse_response_code(response)
    #     token_info = sp_oauth.get_access_token(code)
    # # Auth'ed API request
    # if token_info:
    #     return token_info['access_token']
    # else:
    #     return None

    #     print("success!")

    #session['spotify_auth'] = sp_oauth

    return sp_oauth




def prompt_token_flask():

 
    username = "gmr0678"
    

    scope = 'user-top-read playlist-modify-private'
    client_id_saved = os.environ.get("CLIENT_ID", "Oops, please set env var called 'CLIENT_ID'")
    client_secret_saved = os.environ.get("CLIENT_SECRET", "Oops, please set env var called  'CLIENT_SECRET")
    redirect_uri_saved = "http://localhost:5000/callback/"
    path = (os.path.normpath(os.getcwd()) + "web_app/caches/.cache-" + username)


    return SpotifyOAuth(
        client_id=client_id_saved,
        client_secret=client_secret_saved,
        redirect_uri=redirect_uri_saved,
        scope='user-top-read playlist-modify-private',
        cache_path=path
    )



def get_user_playlists(token):

    username = "gmr0678"

    passed_token = token 

    sp = spotipy.Spotify(auth=passed_token)

    #print(inspect.getsource(sp.current_user_top_tracks()))

    sp.trace = False

    playlists = sp.user_playlists(username)

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




if __name__ == "__main__":
    print("main")
