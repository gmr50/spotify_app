
from flask import Blueprint, request, render_template
from web_app.spotify_methods import prompt_for_user_token_override


import os
import sys
import spotipy
import spotipy.util as util
import dotenv
import webbrowser
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
    print("ps")



    username = "gmr0678"
    print(os.path.normpath(os.getcwd()))

    scope = 'user-top-read playlist-modify-private'
    client_id_saved = os.environ.get("CLIENT_ID", "Oops, please set env var called 'CLIENT_ID'")
    client_secret_saved = os.environ.get("CLIENT_SECRET", "Oops, please set env var called  'CLIENT_SECRET")
    redirect_uri_saved = "http://localhost:5000/callback/"
    cache_path = os.path.normpath(os.getcwd()) + "web_app/caches/.cache-" + username


    #response = request.META.get('PATH_INFO')    
    #print(response)

    token = prompt_for_user_token_override(
    username=username,
    scope=scope,
    client_id=client_id_saved,
    client_secret=client_secret_saved,
    redirect_uri=redirect_uri_saved,
    cache_path = cache_path)

    print("next step")


    

   

    if token:
        sp = spotipy.Spotify(auth=token)



    print("token " + str(token))

    return (print("success"))


    app.run(debug=True)


@home_routes.route("/callback/")
def Callback(code=None):

    #need to pass sp_oauth to this method

    #sp_oauth = os.environ['sp_oauth']

    #sp_oauth = session.get('spotify_auth', None)

    print("callback runnning")
    dict(request.args)

    if "code" in request.args:
        auth_code = request.args["code"]
        print(auth_code)
    else:
        message = "Hello World"

    print("callback authcode: " + auth_code)
    token_info = sp_oauth.get_access_token(auth_code)
    # Auth'ed API request
    if token_info:
        return token_info['access_token']
    else:
        return None

        print("success!**")






