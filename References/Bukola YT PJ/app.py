import flask
from dotenv import load_dotenv
import os
import requests
import base64


# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_USR = os.getenv('SPOTIFY_USER')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


# App setting
app = flask.Flask(__name__)



# Spotify Authorization setting
redirect_uri = 'http://localhost:3000'
scope = 'playlist-read-private playlist-modify-private playlist-modify-public'
spotify_auth_url = f'https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&scope={scope}'



@app.route('/authorize')
def authorize():

    

    return flask.redirect(authorize)
