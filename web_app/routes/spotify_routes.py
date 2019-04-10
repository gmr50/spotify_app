
from flask import Blueprint, request, render_template, jsonify, flash, redirect #, url_for

spotify_routes = Blueprint("spotify_routes", __name__)


@spotify_routes.route("/")
def index():
    print("VISITING THE INDEX PAGE")
    #return "You have visited the homepage"
    return render_template("index.html")



# GET /hello
# GET /hello?name=Polly
@spotify_routes.route("/hello")
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

@spotify_routes.route("/login")
def Login(name=None):
    print("requesting login page!***")

    return render_template("login.html")




@spotify_routes.route("/login/create")
def Execute(name=None):
    print("im Executing login script!!!")
    print("ps")



    username = "gmr0678"

    scope = 'user-top-read playlist-modify-private'
    client_id_saved = os.environ.get("CLIENT_ID", "Oops, please set env var called 'CLIENT_ID'")
    client_secret_saved = os.environ.get("CLIENT_SECRET", "Oops, please set env var called  'CLIENT_SECRET")
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



    print(token)

    return redirect("/login")

    app.run(debug=True)
