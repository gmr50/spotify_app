REQUIREMENTS:

  + Create an environment, upgrade to latest version of Python, if using conda: `conda install python==3.7`

  + Install the requirements file: `pip install -r requirements.txt`

  + Upgrade to the latest version of Spotipy: `pip install git+https://github.com/plamere/spotipy.git --upgrade`

+ Set your environment variables: `CLIENT_ID` and `CLIENT_SECRET`, from the Spotify API. Configure your Spotify API application by adding the redirect URI of "http://localhost:5000/callback/".

+++++++++++++++++++++++++++++

Activate with: `FLASK_APP=web_app flask run`

Open browser, navigate to localhost:5000


++++++++++++++++++++++++++++++

Testing

Install pytest: `pip install pytest`

Enter `pytest` in the commandline, the testing file is found at web_app/test_spotify.py
