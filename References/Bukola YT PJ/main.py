import requests
import base64
import json
import spotify_helper
import time

# CONSTANTS
TOKENS_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Bukola YT PJ\tokens.json'



# GREETING AND FIRST CONTACT

print('''
\nHey! Welcome to the Spotify Playlist Manager app.
Thanks for your preference for our service, 

Before anything else, a little heads-up:
        
    If this is your first time using the app or did you revoke the authorization
    of the app from spotify, please go to the flask_app file and start the server
    to receive the authorization code necessary to make changes in the playlists on your behalf.
      
Ok. Now, let's get going...
      
'''
)

greeting_response = input('- Is this your first time using the app or did you revoke authorization from spotify priorly? (Y/N)\n').upper()

while greeting_response not in ('Y', 'N'):
    print('\nSorry, invalid answer...')
    greeting_response = input('\n- Is this your first time using the app or did you revoke authorization from spotify priorly? (Y/N)\n').upper()


if greeting_response == 'Y':
    
    print(f'''\n- Alright, so in order for us to manage your playlist, the first thing we need is to get an authorization code from Spotify,
and to do so, one necessary step is to have the flask_app (server) running because it will receive the code.
    
    Now, with the server up and running, please go to the link below and authorize the access for this app into your Spotify Account

Link: https://accounts.spotify.com/authorize?client_id={spotify_helper.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={spotify_helper.REDIRECT_URI}&scope={spotify_helper.SPOTIFY_AUTH_SCOPE}\n''')


    greeting_response = input('Let us know when you completed the authorization process by typing any key or typing exit to close the app: ').casefold()

    if greeting_response == 'exit':
        print('\nClosing down... (Remember to shut down the server!)')

    else:
        with open(TOKENS_JSON_FILE_PATH, 'r') as f:

            try:
                tokens_contents = json.load(f)
                code = tokens_contents.get('code')
                print('\n   - Fantastic! we got the code, now we can proceed...\n')

            except Exception as e:
                raise Exception(f'\n  - Apparently we have not received a code')
            
                

# Now that we made sure we have a code to work with...

# 1. Understand how the tokens works and implement the token requesting and refreshing
# 2. After having a token, go back to Bukola's pj to keep learning.












