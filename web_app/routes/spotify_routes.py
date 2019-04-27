
from flask import Blueprint, request, render_template, jsonify, flash, redirect #, url_for

spotify_routes = Blueprint("spotify_routes", __name__)




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
