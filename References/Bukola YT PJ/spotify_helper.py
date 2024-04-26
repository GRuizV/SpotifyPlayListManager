from dotenv import load_dotenv
import os
import json
import requests
import base64
import time

# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'
TOKEN_FILE = 'tokens.json'
SPOTIFY_AUTH_SCOPE = 'playlist-read-private%20playlist-modify-private%20playlist-modify-public'


# Global variables for storing tokens
tokens = {}



class SpotifyHelper:

    @classmethod
    def load_tokens(cls):
        
        global tokens

        if os.path.exist(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as file:
                tokens = json.load(file)

    @classmethod
    def save_tokens(cls):
        
        global tokens

        with open(TOKEN_FILE, 'w') as file:
            json.dump(tokens, file)


    @classmethod
    def authorization(cls):
        
        auth_url = f'https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SPOTIFY_AUTH_SCOPE}'
        print(f'Please authorize the app by visiting the following URL:\n{auth_url}')

        # Wait for the user to authorize the app and obtain the authorization code
        # Ask the App for the code retrieve after the authorization happens
        # Handling an error if the response is not the expected.
        # This function should return the code received.





    @classmethod
    def get_token(cls, code):

        global tokens

        # Exchange the authorization code for an access token and refresh token
        code = input('Enter the authorization code: ')
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization': 'Basic ' + base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
                
        response = requests.post(url, headers=headers, data=data)
        auth_data = response.json()
        access_token = auth_data['access_token']
        refreshed_token = auth_data['refresh_token']
        expires_in = auth_data['expires_in']


    @classmethod
    def is_token_valid(cls):
        global access_token, expires_in

        if access_token is None or expires_in is None:
            return False

        # Check if the access token is expired
        expiration_time = time.time() + expires_in
        if expiration_time < time.time() + 60:  # Check if the token will expire in the next 60 seconds
            return False

        return True


    @classmethod
    def refresh_token(cls):
        global access_token, refreshed_token, expires_in

        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization': 'Basic ' + base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refreshed_token
        }

        response = requests.post(url, headers=headers, data=data)

        auth_data = response.json()
        access_token = auth_data['access_token']
        expires_in = auth_data['expires_in']

        return access_token

