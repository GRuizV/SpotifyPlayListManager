from dotenv import load_dotenv
import os
import json, requests, base64


# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_AUTH_SCOPE = 'playlist-read-private%20playlist-modify-private%20playlist-modify-public'
TOKENS_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Bukola YT PJ\tokens.json'


class SpotifyHelper:

    @classmethod
    def authorize(cls):

        print(f'''\n- Alright, so in order for us to manage your playlist, the first thing we need is to get an authorization code from Spotify,
    and to do so, one necessary step is to have the flask_app (server) running because it will receive the code.
        
        Now, with the server up and running, please go to the link below and authorize the access for this app into your Spotify Account

    Link: https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SPOTIFY_AUTH_SCOPE}\n''')


        greeting_response = input('Let us know when you completed the authorization process by typing any key or typing exit to close the app: ').casefold()

        if greeting_response == 'exit':
            print('\nClosing down... (Remember to shut down the server!)')

        else:
            with open(TOKENS_JSON_FILE_PATH, 'r') as f:

                try:
                    tokens_contents = json.load(f)
                    code = tokens_contents.get('code')
                    
                    if code is not None:

                        print('\n   - Fantastic! we got the code, now we can proceed...\n')
                        return code

                    else:
                        print(f'''\n  ERROR: Apparently we didn't receive a code!''')
                        raise Exception(f'''\n  ERROR: Apparently we didn't receive a code!''')

                except Exception as e:
                    raise Exception(f'''\n  ERROR -{e}-: Apparently we didn't receive a code!''')


    @classmethod
    def get_token(cls, code):

        try:
            # POST Request setting
            url = 'https://accounts.spotify.com/api/token'
            headers = {'Authorization': 'Basic ' + base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}
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
            
            # Saving the updated tokens in the JSON file
            with open(TOKENS_JSON_FILE_PATH, 'w') as f:
                json.dump({'access_token': access_token}, f)
                json.dump({'refresh_token': refresh_token}, f)

            return access_token, refresh_token
        
        except requests.exceptions.RequestException as e:
            print(f'ERROR FETCHING TOKEN: {e}')
            return None, None


    @classmethod
    def refresh_token(cls, refresh_token):

        try:
            # POST Request setting
            url = 'https://accounts.spotify.com/api/token'
            headers = {'Authorization': 'Basic ' + base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }

            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status() # Raise exception for HTTP errors
            auth_data = response.json()
            access_token = auth_data['access_token']
            # Note: 'refresh_token' may not always be returned in refresh token requests
            refresh_token = auth_data.get('refresh_token',refresh_token)
            
            # Saving the updated tokens in the JSON file
            with open(TOKENS_JSON_FILE_PATH, 'w') as f:
                json.dump({'access_token': access_token}, f)
                json.dump({'refresh_token': refresh_token}, f)

            return access_token, refresh_token
    
        except requests.exceptions.RequestException as e:
            print(f'ERROR FETCHING TOKEN: {e}')
            return None, None


