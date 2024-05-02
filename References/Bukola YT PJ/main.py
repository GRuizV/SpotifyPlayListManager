import json
import spotify_helper
from datetime import datetime


# CONSTANTS
TOKENS_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Bukola YT PJ\tokens.json'


#MESSAGE VARIABLES
now = datetime.now()
timestamp = now.strftime("%d/%m/%Y %H:%M:%S")


# GREETING AND FIRST CONTACT
print('''
\nHey! Welcome to the Spotify Playlist Manager app.
      
    Thanks for your preference for our service, 

*** Before anything else, a little heads-up ***
        
    If this is your first time using the app or did you revoke the authorization
    of the app from spotify, please go to the flask_app file and start the server
    to receive the authorization code necessary to make changes in the playlists on your behalf.
      
Ok. Now, let's get going...
      
''')


greeting_response = input(f'[{timestamp}] - Is this your first time using the app or did you revoke authorization from spotify priorly? (Y/N)\n').upper()

# Input handling
while greeting_response not in ('Y', 'N'):
    print(f'\n[{timestamp}] - Sorry, invalid answer...')
    greeting_response = input(f'\n[{timestamp}] - Is this your first time using the app or did you revoke authorization from spotify priorly? (Y/N)\n').upper()




# IF AUTHORIZATION IS NEEDED
if greeting_response == 'Y':    

    code = spotify_helper.SpotifyHelper.authorize()
    token, refresh_token = spotify_helper.SpotifyHelper.get_token(code=code)

    print(f'''\n[{timestamp}] - Great! Apparently we got everything we need to continue...''')

    # Here will continue with the Main menu.




# IF AUTHORIZATION IS NOT NEEDED
with open(TOKENS_JSON_FILE_PATH) as f:
    data = json.load(f)
    token = data['access_token']

    if token is None:
        print(f'\n[{timestamp}] - Oops!')
        raise Exception('''No token was found, please go back and authorize the app (reset the app and answer 'Y' to the first question in the Men)''')

print(f'''\n[{timestamp}] - Great! Apparently we got everything we need to continue...\n''')

print(f'''\n[{timestamp}] - Now, we are just refreshing the access token to make sure this session won't have any issues later...\n''')

old_access_token = data['access_token']
old_refresh_token = data['refresh_token']

new_access_token, new_refresh_token = spotify_helper.SpotifyHelper.refresh_token(data['refresh_token'])

if not new_refresh_token or not new_refresh_token:
    print(f'\n[{timestamp}] - Oops!')
    raise Exception('Something went wrong resfreshing the tokens.')
 
print(f'''[{timestamp}] - Now with refreshed tokens, we can start now managing your playlist''')

# Here will continue with the Main menu.



# Now that we made sure we have a code to work with...
# 1. Include a timestamp in the prompt messages.
# 2. After having a token, go back to Bukola's pj to keep learning.












