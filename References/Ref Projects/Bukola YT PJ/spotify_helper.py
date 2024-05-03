from dotenv import load_dotenv
import os
import json, requests, base64
from datetime import datetime, timedelta


# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_AUTH_SCOPE = 'playlist-read-private%20playlist-modify-private%20playlist-modify-public'
TOKENS_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Ref Projects\Bukola YT PJ\tokens.json'

#MESSAGE VARIABLES
now = datetime.now()
timestamp = now.strftime("%d/%m/%Y %H:%M:%S")


# The class definition (Any operation with spotify will be handled here)
class SpotifyHelper:

    @classmethod
    def authorize(cls):

        '''This function collects the authorization code from the flask server when the user gives its approval'''


        print(f'''\n[{timestamp}] - Alright, so in order for us to manage your playlists, the first thing we need is to get an authorization code from Spotify,
    and to do so, one necessary step is to have the flask_app (server) running because it will receive the code.
        
        Now, with the server up and running, please go to the link below and authorize the access for this app into your Spotify Account

    Link: https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SPOTIFY_AUTH_SCOPE}\n''')


        confirmation_response = input(f'''[{timestamp}] - Let us know when you completed the authorization process by typing any key or typing 'exit' to close the app: ''').casefold()

        if confirmation_response == 'exit':
            print(f'\n[{timestamp}] - Closing down... (Remember to shut down the server!)')

            # ***HERE NEEDS TO BE A CLOSING FUNCTION TO STOP THE APP.

        else:
            with open(TOKENS_JSON_FILE_PATH) as f:
              
                data = json.load(f)
                code = data['code']
                
                if code is not None:

                    print(f'\n[{timestamp}] - Fantastic! we got the code, now we can proceed...\n')
                    return code

                else:
                    print(f'\n[{timestamp}] - Oops!')
                    raise Exception(f'''\n  ERROR: Apparently we didn't receive a code!''')



    @classmethod
    def get_token(cls, code):

        '''This function request a token just after the authorization code is received, with a token and a refresh token no further authorization is needed to work'''

        try:
            # POST Request setting
            url = 'https://accounts.spotify.com/api/token'
            headers = {'Authorization': f'Basic {base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}'}
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI
            }
            
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status() # Raise exception for HTTP errors
            auth_data = response.json()
            access_token = auth_data['access_token']
            refresh_token = auth_data['refresh_token']
            expiration_time = datetime.now() + timedelta(seconds=3600)
            expiration_time_str = expiration_time.isoformat()+'Z'
            
            # Opening the tokens.json file to save the tokens
            with open(TOKENS_JSON_FILE_PATH) as f:
                data = json.load(f)

            # Saving the updated tokens in the JSON file
            with open(TOKENS_JSON_FILE_PATH, 'w') as f:
                data['access_token'] = access_token
                data['refresh_token'] = refresh_token
                data['expiration_time'] = expiration_time_str
                json.dump(data, f, indent=2)

            return access_token, refresh_token
        
        except requests.exceptions.RequestException as e:
            print(f'\n[{timestamp}] - ERROR FETCHING TOKEN: {e}')
            return None, None


    @classmethod
    def refresh_token(cls, refresh_token):

        '''This function request a new token with a refresh token parameter, to keep working without having to ask for the user's authorization again'''


        try:
            # POST Request setting
            url = 'https://accounts.spotify.com/api/token'
            headers = {'Authorization': f'Basic {base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}'}
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }

            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status() # Raise exception for HTTP errors
            auth_data = response.json()
            access_token = auth_data['access_token']
            # Note: 'refresh_token' may not always be returned in refresh token requests
            refresh_token = auth_data.get('refresh_token', refresh_token)
            expiration_time = datetime.now() + timedelta(seconds=3600)
            expiration_time_str = expiration_time.isoformat()+'Z'
            
            # Opening the tokens.json file to save the tokens
            with open(TOKENS_JSON_FILE_PATH) as f:
                data = json.load(f)

            # Saving the updated tokens in the JSON file
            with open(TOKENS_JSON_FILE_PATH, 'w') as f:
                data['access_token'] = access_token
                data['refresh_token'] = refresh_token
                data['expiration_time'] = expiration_time_str
                json.dump(data, f, indent=2)
                
            return access_token, refresh_token
             
        except requests.exceptions.RequestException as e:
            print(f'\n[{timestamp}] - ERROR FETCHING TOKEN: {e}')
            return None, None


