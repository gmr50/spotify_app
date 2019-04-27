
from flask import Blueprint, request, render_template, redirect, session, url_for, flash
#from web_app.spotify_methods import prompt_for_user_token_override
from web_app.spotify_methods import prompt_token_flask, get_user_playlists, add_playlist_for_seed, add_tracks_for_seed, add_top_tracks_for_seed, build_playlist, execute_playlist, playlist_unfollow


import spotipy

# import os
# import sys
# import spotipy
# import spotipy.util as util
# import dotenv
# import webbrowser
from spotipy.oauth2 import SpotifyOAuth


home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    print("VISITING THE INDEX PAGE")
    #return "You have visited the homepage"


    #declaring session variable to send playlist seeds to
    playlists_list = []
    tracks_list = []
    session['playlists_list'] = playlists_list
    session['tracks_list'] = tracks_list


    return render_template("index.html")

# GET /hello
# GET /hello?  
@home_routes.route("/hello")
def hello(name=None):
    print("VISITING THE HELLO PAGE")
    print("REQUEST PARAMS:", dict(request.args))


    if "name" in request.args:
        name = request.args["name"]
        message = f"Hello, {name}"
    else:
        message = "Hello World"

    #return message
    return render_template("hello.html", message=message)

@home_routes.route("/login")
def Login(name=None):
    print("requesting login page!*****")

    return render_template("login.html")




@home_routes.route("/login/create/", methods = ['GET', 'POST'])
def Execute(username=None):
    print("im Executing login script!!!")

    #user_id = request.values.get('username')

    #user_id = "gmr0678"

    username = request.args["username"]
    print(username)

    session['username'] = username

    auth_url = prompt_token_flask(username).get_authorize_url() #> 'https://accounts.spotify.com/authorize?client_id=_____&response_type=code&redirect_uri=________&scope=playlist-modify-private+playlist-read-private'
    return redirect(auth_url)

    app.run(debug=True)


# callback flow adapted from: https://github.com/s2t2/playlist-service-py/pull/4/files#diff-7c81558911feacb797d9b980aec726d6
@home_routes.route("/callback/")
def Callback(code=None):

    #user_id = "gmr0678"
    user_id = session.get('username', None)

    #gets authorization code from url
    print("SPOTIFY CALLBACK")
    print("REQUEST PARAMS:", dict(request.args))

    if "code" in request.args:
        code = request.args["code"]
        print("CODE:", code)

        sp_oauth = prompt_token_flask(user_id)
        token_info = sp_oauth.get_access_token(code)
        print("TOKEN INFO:", token_info)
        token = token_info["access_token"]
        print("ACCESS TOKEN:", token)

        session['token_var'] = token


        

        return redirect("/builder")
    else:
        message = "OOPS, UNABLE TO GET CODE"
        print(message)
        return message



@home_routes.route("/builder/", methods=['POST','GET'])
def seedbuilder():


    ranges = [['short term', 'short_term'], ['medium term', 'medium_term'], ['long term', 'long_term']]

    #user_id = "gmr0678"
    user_id = session.get('username', None)

    try:
        builder_token = session.get('token_var', None)
    except:
        print("failed to get session variable")

    if(builder_token):

        user_playlists = get_user_playlists(builder_token, user_id)

        return render_template("builder.html", playlists = user_playlists, ranges = ranges)




    else:
        print("no token")
        return render_template("no_token.html")



@home_routes.route("/builder_redirect/", methods=['GET'])
def redirect_builder():
    
    session['tracks_list'] = []

    return redirect("/builder/")



@home_routes.route("/builder/addseed/", methods=['POST'])
def AddSeed():


    try:
        token = session.get('token_var', None)
    except:
        print("failed to get session variable")


    selected_playlist_tracks = []
    selection = request.form.get('playlist_seed')

    user_id = session.get('username', None)

    tracks_list = session.get('tracks_list', None)
    selected_playlist_tracks = add_tracks_for_seed(user_id, selection, token)
    tracks_list = tracks_list + selected_playlist_tracks
    session['tracks_list'] = tracks_list
    print(tracks_list)

    #playlist_tracks = sp.user_playlist_tracks(user_id,selection)


    # playlists_list = session.get('playlists_list', None)
    # playlists_list = add_playlist_for_seed(selection, playlists_list)

    # session['playlists_list'] = playlists_list
    # print(playlists_list)


    return redirect('/builder/')





@home_routes.route("/builder/addtoptracksseed/", methods = ['POST'])
def add_top_tracks():

    tracks_list = session.get('tracks_list', None)

    try:
        token = session.get('token_var', None)
    except:
        print("failed to get session variable")

    selection = request.form.get('term_seed')
    print(selection)

    tracks_list = tracks_list + add_top_tracks_for_seed(selection, token)
    session['tracks_list'] = tracks_list
    print(tracks_list)



    return redirect('/builder/')



@home_routes.route("/builder/create_playlist/")
def playlist_builder():
    
    try:
        token = session.get('token_var', None)
    except:
        print("failed to get session variable")


    tracks_list = session.get('tracks_list', None)
    print("in flash route")


    if(tracks_list == []):
        flash('You need to add tracks to seed! Get planting!')
        return redirect("/builder/")
    else:
        recommendations = build_playlist(tracks_list, token)
        session['recommendations'] = recommendations
        print(recommendations)

        return redirect("/builder/create_playlist/name_tree")





@home_routes.route("/builder/create_playlist/name_tree")
def name_playlist():

    return render_template("plant_tree.html")






@home_routes.route("/builder/create_playlist/thank_you", methods=['GET','POST'])
def thank_you(playlist_name = None):

    try:
        token = session.get('token_var', None)
    except:
        print("failed to get session variable")



    playlist_name = request.args["playlist_name"]
    username = session.get('username', None)
    recommendations = session.get('recommendations', None)

    #still need to get playlistname


    #playlist_name = request.values.get('playlist_name') 
    print(playlist_name)

    message = execute_playlist(token, username, recommendations, playlist_name)
    print(message)
    message = playlist_unfollow(username, token)
    print(message)





    return render_template("thank_you.html")





#Nnot working
@home_routes.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

