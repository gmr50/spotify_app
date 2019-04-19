
from flask import Blueprint, request, render_template, redirect, session
#from web_app.spotify_methods import prompt_for_user_token_override
from web_app.spotify_methods import prompt_token_flask, get_user_playlists




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


@home_routes.route("/login/create/")
def Execute(code=None):
    print("im Executing login script!!!")

    username_hard = "gmr0678"
    auth_url = prompt_token_flask().get_authorize_url() #> 'https://accounts.spotify.com/authorize?client_id=_____&response_type=code&redirect_uri=________&scope=playlist-modify-private+playlist-read-private'
    return redirect(auth_url)

    app.run(debug=True)


# callback flow adapted from: https://github.com/s2t2/playlist-service-py/pull/4/files#diff-7c81558911feacb797d9b980aec726d6
@home_routes.route("/callback/")
def Callback(code=None):


    #gets authorization code from url
    print("SPOTIFY CALLBACK")
    print("REQUEST PARAMS:", dict(request.args))

    if "code" in request.args:
        code = request.args["code"]
        print("CODE:", code)

        sp_oauth = prompt_token_flask()
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

@home_routes.route("/builder/")
def SeedBuilder():

    try:
        builder_token = session.get('token_var', None)
    except:
        print("failed to get session variable")

    if(builder_token):

        get_user_playlists(builder_token)
        return render_template("builder.html")




    else:
        print("no token")

